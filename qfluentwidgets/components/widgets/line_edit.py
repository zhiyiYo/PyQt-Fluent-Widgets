# coding: utf-8
from typing import List, Union

from PyQt6.QtCore import QSize, Qt, QRectF, pyqtSignal, QPoint, QTimer, QEvent, QAbstractItemModel, pyqtProperty
from PyQt6.QtGui import QPainter, QPainterPath, QIcon, QColor, QAction
from PyQt6.QtWidgets import (QApplication, QHBoxLayout, QLineEdit, QToolButton, QTextEdit,
                             QPlainTextEdit, QCompleter, QStyle, QWidget, QTextBrowser)


from ...common.style_sheet import FluentStyleSheet, themeColor
from ...common.icon import isDarkTheme, FluentIconBase, drawIcon
from ...common.icon import FluentIcon as FIF
from ...common.font import setFont
from .tool_tip import ToolTipFilter
from .menu import LineEditMenu, TextEditMenu, RoundMenu, MenuAnimationType, IndicatorMenuItemDelegate
from .scroll_bar import SmoothScrollDelegate


class LineEditButton(QToolButton):
    """ Line edit button """

    def __init__(self, icon: Union[str, QIcon, FluentIconBase], parent=None):
        super().__init__(parent=parent)
        self._icon = icon
        self._action = None
        self.isPressed = False
        self.setFixedSize(31, 23)
        self.setIconSize(QSize(10, 10))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName('lineEditButton')
        FluentStyleSheet.LINE_EDIT.apply(self)

    def setAction(self, action: QAction):
        self._action = action
        self._onActionChanged()

        self.clicked.connect(action.trigger)
        action.toggled.connect(self.setChecked)
        action.changed.connect(self._onActionChanged)

        self.installEventFilter(ToolTipFilter(self, 700))

    def _onActionChanged(self):
        action = self.action()
        self.setIcon(action.icon())
        self.setToolTip(action.toolTip())
        self.setEnabled(action.isEnabled())
        self.setCheckable(action.isCheckable())
        self.setChecked(action.isChecked())

    def action(self):
        return self._action

    def setIcon(self, icon: Union[str, FluentIconBase, QIcon]):
        self._icon = icon
        self.update()

    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing |
                               QPainter.RenderHint.SmoothPixmapTransform)

        iw, ih = self.iconSize().width(), self.iconSize().height()
        w, h = self.width(), self.height()
        rect = QRectF((w - iw)/2, (h - ih)/2, iw, ih)

        if self.isPressed:
            painter.setOpacity(0.7)

        if isDarkTheme():
            drawIcon(self._icon, painter, rect)
        else:
            drawIcon(self._icon, painter, rect, fill='#656565')


class LineEdit(QLineEdit):
    """ Line edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._isClearButtonEnabled = False
        self._completer = None  # type: QCompleter
        self._completerMenu = None  # type: CompleterMenu
        self._isError = False

        self.leftButtons = []   # type: List[LineEditButton]
        self.rightButtons = []  # type: List[LineEditButton]

        self.setProperty("transparent", True)
        FluentStyleSheet.LINE_EDIT.apply(self)
        self.setFixedHeight(33)
        self.setAttribute(Qt.WidgetAttribute.WA_MacShowFocusRect, False)
        setFont(self)

        self.hBoxLayout = QHBoxLayout(self)
        self.clearButton = LineEditButton(FIF.CLOSE, self)

        self.clearButton.setFixedSize(29, 25)
        self.clearButton.hide()

        self.hBoxLayout.setSpacing(3)
        self.hBoxLayout.setContentsMargins(4, 4, 4, 4)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addWidget(self.clearButton, 0, Qt.AlignmentFlag.AlignRight)

        self.clearButton.clicked.connect(self.clear)
        self.textChanged.connect(self.__onTextChanged)
        self.textEdited.connect(self.__onTextEdited)

    def isError(self):
        return self._isError

    def setError(self, isError: bool):
        if isError == self.isError():
            return

        self._isError = isError
        self.update()

    def focusedBorderColor(self):
        if not self.isError():
            return themeColor()

        return QColor("#ff99a4") if isDarkTheme() else QColor("#c42b1c")

    def setClearButtonEnabled(self, enable: bool):
        self._isClearButtonEnabled = enable
        self._adjustTextMargins()

    def isClearButtonEnabled(self) -> bool:
        return self._isClearButtonEnabled

    def setCompleter(self, completer: QCompleter):
        self._completer = completer

    def completer(self):
        return self._completer

    def addAction(self, action: QAction, position=QLineEdit.ActionPosition.TrailingPosition):
        QWidget.addAction(self, action)

        button = LineEditButton(action.icon())
        button.setAction(action)
        button.setFixedWidth(29)

        if position == QLineEdit.ActionPosition.LeadingPosition:
            self.hBoxLayout.insertWidget(len(self.leftButtons), button, 0, Qt.AlignmentFlag.AlignLeading)
            if not self.leftButtons:
                self.hBoxLayout.insertStretch(1, 1)

            self.leftButtons.append(button)
        else:
            self.rightButtons.append(button)
            self.hBoxLayout.addWidget(button, 0, Qt.AlignmentFlag.AlignRight)

        self._adjustTextMargins()

    def addActions(self, actions, position=QLineEdit.ActionPosition.TrailingPosition):
        for action in actions:
            self.addAction(action, position)

    def _adjustTextMargins(self):
        left = len(self.leftButtons) * 30
        right = len(self.rightButtons) * 30 + 28 * self.isClearButtonEnabled()
        m = self.textMargins()
        self.setTextMargins(left, m.top(), right, m.bottom())

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        self.clearButton.hide()

    def focusInEvent(self, e):
        super().focusInEvent(e)
        if self.isClearButtonEnabled():
            self.clearButton.setVisible(bool(self.text()))

    def __onTextChanged(self, text):
        """ text changed slot """
        if self.isClearButtonEnabled():
            self.clearButton.setVisible(bool(text) and self.hasFocus())

    def __onTextEdited(self, text):
        if not self.completer():
            return

        if self.text():
            QTimer.singleShot(50, self._showCompleterMenu)
        elif self._completerMenu:
            self._completerMenu.close()

    def setCompleterMenu(self, menu):
        """ set completer menu

        Parameters
        ----------
        menu: CompleterMenu
            completer menu
        """
        menu.activated.connect(self._completer.activated)
        self._completerMenu = menu

    def _showCompleterMenu(self):
        if not self.completer() or not self.text():
            return

        # create menu
        if not self._completerMenu:
            self.setCompleterMenu(CompleterMenu(self))

        # add menu items
        self.completer().setCompletionPrefix(self.text())
        changed = self._completerMenu.setCompletion(self.completer().completionModel())
        self._completerMenu.setMaxVisibleItems(self.completer().maxVisibleItems())

        # show menu
        if changed:
            self._completerMenu.popup()

    def contextMenuEvent(self, e):
        menu = LineEditMenu(self)
        menu.exec(e.globalPos())

    def paintEvent(self, e):
        super().paintEvent(e)
        if not self.hasFocus():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        m = self.contentsMargins()
        path = QPainterPath()
        w, h = self.width()-m.left()-m.right(), self.height()
        path.addRoundedRect(QRectF(m.left(), h-10, w, 10), 5, 5)

        rectPath = QPainterPath()
        rectPath.addRect(m.left(), h-10, w, 8)
        path = path.subtracted(rectPath)

        painter.fillPath(path, self.focusedBorderColor())


class CompleterMenu(RoundMenu):
    """ Completer menu """

    activated = pyqtSignal(str)

    def __init__(self, lineEdit: LineEdit):
        super().__init__()
        self.items = []
        self.lineEdit = lineEdit

        self.view.setViewportMargins(0, 2, 0, 6)
        self.view.setObjectName('completerListWidget')
        self.view.setItemDelegate(IndicatorMenuItemDelegate())
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.installEventFilter(self)
        self.setItemHeight(33)

    def setCompletion(self, model: QAbstractItemModel):
        """ set the completion model """
        items = []
        for i in range(model.rowCount()):
            for j in range(model.columnCount()):
                items.append(model.data(model.index(i, j)))

        if self.items == items and self.isVisible():
            return False

        self.setItems(items)
        return True

    def setItems(self, items: List[str]):
        """ set completion items """
        self.view.clear()

        self.items = items
        self.view.addItems(items)

        for i in range(self.view.count()):
            item = self.view.item(i)
            item.setSizeHint(QSize(1, self.itemHeight))

    def _onItemClicked(self, item):
        self._hideMenu(False)
        self.__onItemSelected(item.text())

    def eventFilter(self, obj, e: QEvent):
        if e.type() != QEvent.Type.KeyPress:
            return super().eventFilter(obj, e)

        # redirect input to line edit
        self.lineEdit.event(e)
        self.view.event(e)

        if e.key() == Qt.Key.Key_Escape:
            self.close()
        if e.key() in [Qt.Key.Key_Enter, Qt.Key.Key_Return] and self.view.currentRow() >= 0:
            self.__onItemSelected(self.view.currentItem().text())
            self.close()

        return super().eventFilter(obj, e)

    def __onItemSelected(self, text):
        self.lineEdit.setText(text)
        self.activated.emit(text)

    def popup(self):
        """ show menu """
        if not self.items:
            return self.close()

        # adjust menu size
        p = self.lineEdit
        if self.view.width() < p.width():
            self.view.setMinimumWidth(p.width())
            self.adjustSize()

        # determine the animation type by choosing the maximum height of view
        x = -self.width()//2 + self.layout().contentsMargins().left() + p.width()//2
        y = p.height() - self.layout().contentsMargins().top() + 2
        pd = p.mapToGlobal(QPoint(x, y))
        hd = self.view.heightForAnimation(pd, MenuAnimationType.FADE_IN_DROP_DOWN)

        pu = p.mapToGlobal(QPoint(x, 7))
        hu = self.view.heightForAnimation(pu, MenuAnimationType.FADE_IN_PULL_UP)

        if hd >= hu:
            pos = pd
            aniType = MenuAnimationType.FADE_IN_DROP_DOWN
        else:
            pos = pu
            aniType = MenuAnimationType.FADE_IN_PULL_UP

        self.view.adjustSize(pos, aniType)

        # update border style
        self.view.setProperty('dropDown', aniType == MenuAnimationType.FADE_IN_DROP_DOWN)
        self.view.setStyle(QApplication.style())
        self.view.update()

        self.adjustSize()
        self.exec(pos, aniType=aniType)

        # remove the focus of menu
        self.view.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        p.setFocus()


class SearchLineEdit(LineEdit):
    """ Search line edit """

    searchSignal = pyqtSignal(str)
    clearSignal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.searchButton = LineEditButton(FIF.SEARCH, self)

        self.hBoxLayout.addWidget(self.searchButton, 0, Qt.AlignmentFlag.AlignRight)
        self.setClearButtonEnabled(True)
        self.setTextMargins(0, 0, 59, 0)

        self.searchButton.clicked.connect(self.search)
        self.clearButton.clicked.connect(self.clearSignal)

    def search(self):
        """ emit search signal """
        text = self.text().strip()
        if text:
            self.searchSignal.emit(text)
        else:
            self.clearSignal.emit()

    def setClearButtonEnabled(self, enable: bool):
        self._isClearButtonEnabled = enable
        self.setTextMargins(0, 0, 28*enable+30, 0)


class EditLayer(QWidget):
    """ Edit layer """

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        parent.installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.parent() and e.type() == QEvent.Type.Resize:
            self.resize(e.size())

        return super().eventFilter(obj, e)

    def paintEvent(self, e):
        if not self.parent().hasFocus():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        m = self.contentsMargins()
        path = QPainterPath()
        w, h = self.width()-m.left()-m.right(), self.height()
        path.addRoundedRect(QRectF(m.left(), h-10, w, 10), 5, 5)

        rectPath = QPainterPath()
        rectPath.addRect(m.left(), h-10, w, 7.5)
        path = path.subtracted(rectPath)

        painter.fillPath(path, themeColor())


class TextEdit(QTextEdit):
    """ Text edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layer = EditLayer(self)
        self.scrollDelegate = SmoothScrollDelegate(self)
        FluentStyleSheet.LINE_EDIT.apply(self)
        setFont(self)

    def contextMenuEvent(self, e):
        menu = TextEditMenu(self)
        menu.exec(e.globalPos())


class PlainTextEdit(QPlainTextEdit):
    """ Plain text edit """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layer = EditLayer(self)
        self.scrollDelegate = SmoothScrollDelegate(self)
        FluentStyleSheet.LINE_EDIT.apply(self)
        setFont(self)

    def contextMenuEvent(self, e):
        menu = TextEditMenu(self)
        menu.exec(e.globalPos())


class TextBrowser(QTextBrowser):
    """ Text browser """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layer = EditLayer(self)
        self.scrollDelegate = SmoothScrollDelegate(self)
        FluentStyleSheet.LINE_EDIT.apply(self)
        setFont(self)

    def contextMenuEvent(self, e):
        menu = TextEditMenu(self)
        menu.exec(e.globalPos())


class PasswordLineEdit(LineEdit):
    """ Password line edit """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.viewButton = LineEditButton(FIF.VIEW, self)

        self.setEchoMode(QLineEdit.EchoMode.Password)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.NoContextMenu)
        self.hBoxLayout.addWidget(self.viewButton, 0, Qt.AlignmentFlag.AlignRight)
        self.setClearButtonEnabled(False)

        self.viewButton.installEventFilter(self)
        self.viewButton.setIconSize(QSize(13, 13))
        self.viewButton.setFixedSize(29, 25)

    def setPasswordVisible(self, isVisible: bool):
        """ set the visibility of password """
        if isVisible:
            self.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.setEchoMode(QLineEdit.EchoMode.Password)

    def isPasswordVisible(self):
        return self.echoMode() == QLineEdit.EchoMode.Normal

    def setClearButtonEnabled(self, enable: bool):
        self._isClearButtonEnabled = enable

        if self.viewButton.isHidden():
            self.setTextMargins(0, 0, 28*enable, 0)
        else:
            self.setTextMargins(0, 0, 28*enable + 30, 0)

    def setViewPasswordButtonVisible(self, isVisible: bool):
        """ set the visibility of view password button """
        self.viewButton.setVisible(isVisible)

    def eventFilter(self, obj, e):
        if obj is not self.viewButton or not self.isEnabled():
            return super().eventFilter(obj, e)

        if e.type() == QEvent.Type.MouseButtonPress:
            self.setPasswordVisible(True)
        elif e.type() == QEvent.Type.MouseButtonRelease:
            self.setPasswordVisible(False)

        return super().eventFilter(obj, e)

    def inputMethodQuery(self, query: Qt.InputMethodQuery):
        # Disable IME for PasswordLineEdit
        if query == Qt.InputMethodQuery.ImEnabled:
            return False
        else:
            return super().inputMethodQuery(query)

    passwordVisible = pyqtProperty(bool, isPasswordVisible, setPasswordVisible)