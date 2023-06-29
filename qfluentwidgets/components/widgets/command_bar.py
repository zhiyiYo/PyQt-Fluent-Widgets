# coding:utf-8
from typing import Iterable, List, Tuple, Union

from PyQt5.QtCore import Qt, pyqtSignal, QSize, QRectF, QRect, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QColor, QFont
from PyQt5.QtWidgets import QAction, QLayoutItem, QWidget, QFrame

from ...common.font import setFont
from ...common.icon import FluentIcon, Icon, Action
from ...common.style_sheet import isDarkTheme
from .menu import RoundMenu, MenuAnimationType
from .button import TransparentToggleToolButton


class CommandButton(TransparentToggleToolButton):
    """ Command button """

    def _postInit(self):
        super()._postInit()
        self.setCheckable(False)
        self.setToolButtonStyle(Qt.ToolButtonIconOnly)
        setFont(self, 12)

        self._text = ''
        self._action = None
        self._isTight = False

    def setTight(self, isTight: bool):
        self._isTight = isTight
        self.update()

    def isTight(self):
        return self._isTight

    def sizeHint(self) -> QSize:
        style = self.toolButtonStyle()

        if style in [Qt.ToolButtonIconOnly, Qt.ToolButtonFollowStyle] or not self.text():
            return QSize(40, 34) if self.isTight() else QSize(48, 34)

        # get the width of text
        tw = self.fontMetrics().width(self.text())

        if style == Qt.ToolButtonTextBesideIcon:
            return QSize(tw + 47, 34)
        if style == Qt.ToolButtonTextOnly:
            return QSize(tw + 32, 34)

        return QSize(tw + 32, 50)

    def _drawIcon(self, icon, painter, rect):
        pass

    def text(self):
        return self._text

    def setText(self, text: str):
        self._text = text
        self.update()

    def setAction(self, action: QAction):
        self._action = action
        self.clicked.connect(action.trigger)
        action.toggled.connect(self._onActionToggled)

    def _onActionToggled(self, isChecked: bool):
        self.setCheckable(True)
        self.setChecked(isChecked)

    def action(self):
        return self._action

    def paintEvent(self, e):
        super().paintEvent(e)

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)

        if not self.isChecked():
            painter.setPen(Qt.white if isDarkTheme() else Qt.black)
        else:
            painter.setPen(Qt.black if isDarkTheme() else Qt.white)

        # draw icon and text
        style = self.toolButtonStyle()
        iw, ih = self.iconSize().width(), self.iconSize().height()

        if style in [Qt.ToolButtonIconOnly, Qt.ToolButtonFollowStyle] or not self.text():
            y = (self.height() - ih) / 2
            x = (self.width() - iw) / 2
            super()._drawIcon(self._icon, painter, QRectF(x, y, iw, ih))
        elif style == Qt.ToolButtonTextOnly:
            painter.drawText(self.rect(), Qt.AlignCenter, self.text())
        elif style == Qt.ToolButtonTextBesideIcon:
            y = (self.height() - ih) / 2
            super()._drawIcon(self._icon, painter, QRectF(11, y, iw, ih))

            rect = QRectF(26, 0, self.width() - 26, self.height())
            painter.drawText(rect, Qt.AlignCenter, self.text())
        elif style == Qt.ToolButtonTextUnderIcon:
            x = (self.width() - iw) / 2
            super()._drawIcon(self._icon, painter, QRectF(x, 9, iw, ih))

            rect = QRectF(0, ih + 13, self.width(), self.height() - ih - 13)
            painter.drawText(rect, Qt.AlignHCenter | Qt.AlignTop, self.text())


class MoreActionsButton(CommandButton):
    """ More action button """

    def _postInit(self):
        super()._postInit()
        self.setIcon(FluentIcon.MORE)

    def sizeHint(self):
        return QSize(40, 34)


class CommandSeparator(QWidget):
    """ Command separator """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(9, 34)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setPen(QColor(255, 255, 255, 21)
                       if isDarkTheme() else QColor(0, 0, 0, 15))
        painter.drawLine(5, 2, 5, self.height() - 2)


class CommandMenu(RoundMenu):

    def __init__(self, parent=None):
        super().__init__("", parent)
        self.setItemHeight(32)
        self.view.setIconSize(QSize(16, 16))


class CommandBar(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._widgets = []  # type: List[QWidget]
        self._hiddenWidgets = []  # type: List[QWidget]
        self._hiddenActions = []  # type: List[QAction]

        self._menuAnimation = MenuAnimationType.DROP_DOWN
        self._toolButtonStyle = Qt.ToolButtonIconOnly
        self._isButtonTight = False
        self._spacing = 4

        self.moreButton = MoreActionsButton(self)
        self.moreButton.clicked.connect(self._showMoreActionsMenu)
        self.moreButton.hide()

        setFont(self, 12)

    def setSpaing(self, spacing: int):
        if spacing == self._spacing:
            return

        self._spacing = spacing
        self.updateGeometry()

    def spacing(self):
        return self._spacing

    def addAction(self, action: QAction):
        """ add action

        Parameters
        ----------
        action: QAction
            the action to add
        """
        if action in self.actions():
            return

        button = self._createButton(action)
        self._insertWidgetToLayout(-1, button)
        super().addAction(action)
        return button

    def addActions(self, actions: Iterable[QAction]):
        for action in actions:
            self.addAction(action)

    def addHiddenAction(self, action: QAction):
        """ add hidden action """
        if action in self.actions():
            return

        self._hiddenActions.append(action)
        self.updateGeometry()
        super().addAction(action)

    def addHiddenActions(self, actions: List[QAction]):
        """ add hidden action """
        for action in actions:
            self.addHiddenAction(action)

    def insertAction(self, before: Union[Action, QAction], action: Union[Action, QAction], checkable=False):
        if before not in self.actions():
            return

        index = self.actions().index(before)
        button = self._createButton(action, checkable)
        self._insertWidgetToLayout(index, button)
        super().insertAction(before, action)
        return button

    def addSeparator(self):
        self.insertSeparator(-1)

    def insertSeparator(self, index: int):
        self._insertWidgetToLayout(index, CommandSeparator(self))

    def addWidget(self, widget: QWidget):
        """ add widget to command bar """
        self._insertWidgetToLayout(-1, widget)

    def setToolButtonStyle(self, style: Qt.ToolButtonStyle):
        """ set the style of tool button """
        if self.toolButtonStyle() == style:
            return

        self._toolButtonStyle = style
        for w in self.commandButtons:
            w.setToolButtonStyle(style)

    def toolButtonStyle(self):
        return self._toolButtonStyle

    def setButtonTight(self, isTight: bool):
        if self.isButtonTight() == isTight:
            return

        self._isButtonTight = isTight

        for w in self.commandButtons:
            w.setTight(isTight)

        self.updateGeometry()

    def isButtonTight(self):
        return self._isButtonTight

    def resizeEvent(self, e):
        self.updateGeometry()

    def _createButton(self, action: QAction):
        """ create command button """
        button = CommandButton(action.icon())
        button.setText(action.text())
        button.setAction(action)
        button.setToolButtonStyle(self.toolButtonStyle())
        button.setTight(self.isButtonTight())
        button.setFont(self.font())
        return button

    def _insertWidgetToLayout(self, index: int, widget: QWidget):
        """ add widget to layout """
        widget.setParent(self)
        widget.show()

        if index < 0:
            self._widgets.append(widget)
        else:
            self._widgets.insert(index, widget)

        self.updateGeometry()

    def minimumSizeHint(self) -> QSize:
        return self.moreButton.size()

    def updateGeometry(self):
        self._hiddenWidgets.clear()
        self.moreButton.hide()

        visibles = self._visibleWidgets()
        x = self.contentsMargins().left()
        h = self.height()

        for widget in visibles:
            widget.show()
            w, h = widget.width(), widget.height()
            widget.move(x, (h - widget.height()) // 2)
            x += (w + self.spacing())

        # show more actions button
        if self._hiddenActions:
            self.moreButton.show()
            self.moreButton.move(x, (h - self.moreButton.height()) // 2)

        for widget in self._widgets[len(visibles):]:
            widget.hide()
            self._hiddenWidgets.append(widget)

    def _visibleWidgets(self) -> List[QLayoutItem]:
        """ return the visible widgets in layout """
        w = 0

        # show more actions if there are hidden actions
        widgets = self._widgets.copy()
        if self._hiddenActions:
            widgets.append(self.moreButton)

        widths = [i.width() for i in widgets]
        total = sum(widths) + w + self.spacing() * max(len(widgets) - 1, 0)

        # have enough spacing to show all widgets
        if total <= self.width():
            return self._widgets

        w += self.moreButton.width()
        for index, widget in enumerate(self._widgets):
            w += widget.width()
            if w > self.width():
                break

        return self._widgets[:index]

    def setFont(self, font: QFont):
        super().setFont(font)
        for button in self.commandButtons:
            button.setFont(font)

    @property
    def commandButtons(self):
        return [w for w in self._widgets if isinstance(w, CommandButton)]

    def setMenuDropDown(self, down: bool):
        """ set the animation direction of more actions menu """
        if down:
            self._menuAnimation = MenuAnimationType.DROP_DOWN
        else:
            self._menuAnimation = MenuAnimationType.PULL_UP

    def _showMoreActionsMenu(self):
        """ show more actions menu """
        actions = self._hiddenActions.copy()

        for w in reversed(self._hiddenWidgets):
            if isinstance(w, CommandButton):
                actions.insert(0, w.action())

        menu = CommandMenu(self)
        menu.addActions(actions)

        x = -menu.width() + menu.layout().contentsMargins().right() + \
            self.moreButton.width() + 5
        if self._menuAnimation == MenuAnimationType.DROP_DOWN:
            y = self.moreButton.height()
        else:
            y = -menu.height() + menu.layout().contentsMargins().bottom()

        pos = self.moreButton.mapToGlobal(QPoint(x, y))
        menu.exec_(pos, aniType=self._menuAnimation)
