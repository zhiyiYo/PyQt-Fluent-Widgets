# coding:utf-8
from typing import Iterable, List, Tuple, Union

from PyQt6.QtCore import Qt, pyqtSignal, QSize, QRectF, QPointF, QPoint, QEvent
from PyQt6.QtGui import QAction, QPainter, QColor, QFont, QHoverEvent, QPainterPath
from PyQt6.QtWidgets import QLayoutItem, QWidget, QFrame, QHBoxLayout, QApplication

from ...common.font import setFont
from ...common.icon import FluentIcon, Icon, Action
from ...common.style_sheet import isDarkTheme
from .menu import RoundMenu, MenuAnimationType
from .button import TransparentToggleToolButton
from .tool_tip import ToolTipFilter
from .flyout import FlyoutViewBase, Flyout


class CommandButton(TransparentToggleToolButton):
    """ Command button

    Constructors
    ------------
    * CommandButton(`parent`: QWidget = None)
    * CommandButton(`icon`: QIcon | str | FluentIconBase = None, `parent`: QWidget = None)
    """

    def _postInit(self):
        super()._postInit()
        self.setCheckable(False)
        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
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
        if self.isIconOnly():
            return QSize(36, 34) if self.isTight() else QSize(48, 34)

        # get the width of text
        tw = self.fontMetrics().boundingRect(self.text()).width()

        style = self.toolButtonStyle()
        if style == Qt.ToolButtonStyle.ToolButtonTextBesideIcon:
            return QSize(tw + 47, 34)
        if style == Qt.ToolButtonStyle.ToolButtonTextOnly:
            return QSize(tw + 32, 34)

        return QSize(tw + 32, 50)

    def isIconOnly(self):
        if not self.text():
            return True

        return self.toolButtonStyle() in [Qt.ToolButtonStyle.ToolButtonIconOnly, Qt.ToolButtonStyle.ToolButtonFollowStyle]

    def _drawIcon(self, icon, painter, rect):
        pass

    def text(self):
        return self._text

    def setText(self, text: str):
        self._text = text
        self.update()

    def setAction(self, action: QAction):
        self._action = action
        self._onActionChanged()

        self.clicked.connect(action.trigger)
        action.toggled.connect(self.setChecked)
        action.changed.connect(self._onActionChanged)

        self.installEventFilter(CommandToolTipFilter(self, 700))

    def _onActionChanged(self):
        action = self.action()
        self.setIcon(action.icon())
        self.setText(action.text())
        self.setToolTip(action.toolTip())
        self.setEnabled(action.isEnabled())
        self.setCheckable(action.isCheckable())
        self.setChecked(action.isChecked())

    def action(self):
        return self._action

    def paintEvent(self, e):
        super().paintEvent(e)

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing |
                               QPainter.RenderHint.SmoothPixmapTransform)

        if not self.isChecked():
            painter.setPen(Qt.GlobalColor.white if isDarkTheme() else Qt.GlobalColor.black)
        else:
            painter.setPen(Qt.GlobalColor.black if isDarkTheme() else Qt.GlobalColor.white)

        if not self.isEnabled():
            painter.setOpacity(0.43)
        elif self.isPressed:
            painter.setOpacity(0.63)

        # draw icon and text
        style = self.toolButtonStyle()
        iw, ih = self.iconSize().width(), self.iconSize().height()

        if self.isIconOnly():
            y = (self.height() - ih) / 2
            x = (self.width() - iw) / 2
            super()._drawIcon(self._icon, painter, QRectF(x, y, iw, ih))
        elif style == Qt.ToolButtonStyle.ToolButtonTextOnly:
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.text())
        elif style == Qt.ToolButtonStyle.ToolButtonTextBesideIcon:
            y = (self.height() - ih) / 2
            super()._drawIcon(self._icon, painter, QRectF(11, y, iw, ih))

            rect = QRectF(26, 0, self.width() - 26, self.height())
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, self.text())
        elif style == Qt.ToolButtonStyle.ToolButtonTextUnderIcon:
            x = (self.width() - iw) / 2
            super()._drawIcon(self._icon, painter, QRectF(x, 9, iw, ih))

            rect = QRectF(0, ih + 13, self.width(), self.height() - ih - 13)
            painter.drawText(rect, Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop, self.text())


class CommandToolTipFilter(ToolTipFilter):
    """ Command tool tip filter """

    def _canShowToolTip(self) -> bool:
        return super()._canShowToolTip() and self.parent().isIconOnly()


class MoreActionsButton(CommandButton):
    """ More action button """

    def _postInit(self):
        super()._postInit()
        self.setIcon(FluentIcon.MORE)

    def sizeHint(self):
        return QSize(40, 34)

    def clearState(self):
        self.setAttribute(Qt.WidgetAttribute.WA_UnderMouse, False)
        e = QHoverEvent(QEvent.Type.HoverLeave, QPointF(-1, -1), QPointF())
        QApplication.sendEvent(self, e)


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
    """ Command menu """

    def __init__(self, parent=None):
        super().__init__("", parent)
        self.setItemHeight(32)
        self.view.setIconSize(QSize(16, 16))


class CommandBar(QFrame):
    """ Command bar """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._widgets = []  # type: List[QWidget]
        self._hiddenWidgets = []  # type: List[QWidget]
        self._hiddenActions = []  # type: List[QAction]

        self._menuAnimation = MenuAnimationType.DROP_DOWN
        self._toolButtonStyle = Qt.ToolButtonStyle.ToolButtonIconOnly
        self._iconSize = QSize(16, 16)
        self._isButtonTight = False
        self._spacing = 4

        self.moreButton = MoreActionsButton(self)
        self.moreButton.clicked.connect(self._showMoreActionsMenu)
        self.moreButton.hide()

        setFont(self, 12)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

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

    def insertAction(self, before: QAction, action: QAction):
        if before not in self.actions():
            return

        index = self.actions().index(before)
        button = self._createButton(action)
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

    def removeAction(self, action: QAction):
        if action not in self.actions():
            return

        for w in self.commandButtons:
            if w.action() is action:
                self._widgets.remove(w)
                w.hide()
                w.deleteLater()
                break

        self.updateGeometry()

    def removeWidget(self, widget: QWidget):
        if widget not in self._widgets:
            return

        self._widgets.remove(widget)
        self.updateGeometry()

    def removeHiddenAction(self, action: QAction):
        if action in self._hiddenActions:
            self._hiddenActions.remove(action)

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

    def setIconSize(self, size: QSize):
        if size == self._iconSize:
            return

        self._iconSize = size
        for w in self.commandButtons:
            w.setIconSize(size)

    def iconSize(self):
        return self._iconSize

    def resizeEvent(self, e):
        self.updateGeometry()

    def _createButton(self, action: QAction):
        """ create command button """
        button = CommandButton(self)
        button.setAction(action)
        button.setToolButtonStyle(self.toolButtonStyle())
        button.setTight(self.isButtonTight())
        button.setIconSize(self.iconSize())
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

        self.setFixedHeight(max(w.height() for w in self._widgets))
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
            widget.move(x, (h - widget.height()) // 2)
            x += (widget.width() + self.spacing())

        # show more actions button
        if self._hiddenActions or len(visibles) < len(self._widgets):
            self.moreButton.show()
            self.moreButton.move(x, (h - self.moreButton.height()) // 2)

        for widget in self._widgets[len(visibles):]:
            widget.hide()
            self._hiddenWidgets.append(widget)

    def _visibleWidgets(self) -> List[QWidget]:
        """ return the visible widgets in layout """
        # have enough spacing to show all widgets
        if self.suitableWidth() <= self.width():
            return self._widgets

        w = self.moreButton.width()
        for index, widget in enumerate(self._widgets):
            w += widget.width()
            if index > 0:
                w += self.spacing()

            if w > self.width():
                break

        return self._widgets[:index]

    def suitableWidth(self):
        widths = [w.width() for w in self._widgets]
        if self._hiddenActions:
            widths.append(self.moreButton.width())

        return sum(widths) + self.spacing() * max(len(widths) - 1, 0)

    def resizeToSuitableWidth(self):
        self.setFixedWidth(self.suitableWidth())

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

    def isMenuDropDown(self):
        return self._menuAnimation == MenuAnimationType.DROP_DOWN

    def _showMoreActionsMenu(self):
        """ show more actions menu """
        self.moreButton.clearState()

        actions = self._hiddenActions.copy()

        for w in reversed(self._hiddenWidgets):
            if isinstance(w, CommandButton):
                actions.insert(0, w.action())

        menu = CommandMenu(self)
        menu.addActions(actions)

        x = -menu.width() + menu.layout().contentsMargins().right() + \
            self.moreButton.width() + 18
        if self._menuAnimation == MenuAnimationType.DROP_DOWN:
            y = self.moreButton.height()
        else:
            y = -5

        pos = self.moreButton.mapToGlobal(QPoint(x, y))
        menu.exec(pos, aniType=self._menuAnimation)


class CommandViewMenu(CommandMenu):
    """ Command view menu """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.view.setObjectName('commandListWidget')

    def setDropDown(self, down: bool, long=False):
        self.view.setProperty('dropDown', down)
        self.view.setProperty('long', long)
        self.view.setStyle(QApplication.style())
        self.view.update()


class CommandViewBar(CommandBar):
    """ Command view bar """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMenuDropDown(True)

    def setMenuDropDown(self, down: bool):
        """ set the animation direction of more actions menu """
        if down:
            self._menuAnimation = MenuAnimationType.FADE_IN_DROP_DOWN
        else:
            self._menuAnimation = MenuAnimationType.FADE_IN_PULL_UP

    def isMenuDropDown(self):
        return self._menuAnimation == MenuAnimationType.FADE_IN_DROP_DOWN

    def _showMoreActionsMenu(self):
        self.moreButton.clearState()

        actions = self._hiddenActions.copy()

        for w in reversed(self._hiddenWidgets):
            if isinstance(w, CommandButton):
                actions.insert(0, w.action())

        menu = CommandViewMenu(self)
        menu.addActions(actions)

        # adjust the shape of view
        view = self.parent()  # type: CommandBarView
        view.setMenuVisible(True)

        # adjust the shape of menu
        menu.closedSignal.connect(lambda: view.setMenuVisible(False))
        menu.setDropDown(self.isMenuDropDown(), menu.view.width() > view.width()+5)

        # adjust menu size
        if menu.view.width() < view.width():
            menu.view.setFixedWidth(view.width())
            menu.adjustSize()

        x = -menu.width() + menu.layout().contentsMargins().right() + \
            self.moreButton.width() + 18
        if self.isMenuDropDown():
            y = self.moreButton.height()
        else:
            y = -13
            menu.setShadowEffect(0, (0, 0), QColor(0, 0, 0, 0))
            menu.layout().setContentsMargins(12, 20, 12, 8)

        pos = self.moreButton.mapToGlobal(QPoint(x, y))
        menu.exec(pos, aniType=self._menuAnimation)


class CommandBarView(FlyoutViewBase):
    """ Command bar view """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.bar = CommandViewBar(self)
        self.hBoxLayout = QHBoxLayout(self)

        self.hBoxLayout.setContentsMargins(6, 6, 6, 6)
        self.hBoxLayout.addWidget(self.bar)
        self.hBoxLayout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetMinAndMaxSize)

        self.setButtonTight(True)
        self.setIconSize(QSize(14, 14))

        self._isMenuVisible = False

    def setMenuVisible(self, isVisible):
        self._isMenuVisible = isVisible
        self.update()

    def addWidget(self, widget: QWidget):
        self.bar.addWidget(widget)

    def setSpaing(self, spacing: int):
        self.bar.setSpaing(spacing)

    def spacing(self):
        return self.bar.spacing()

    def addAction(self, action: QAction):
        return self.bar.addAction(action)

    def addActions(self, actions: Iterable[QAction]):
        self.bar.addActions(actions)

    def addHiddenAction(self, action: QAction):
        self.bar.addHiddenAction(action)

    def addHiddenActions(self, actions: List[QAction]):
        self.bar.addHiddenActions(actions)

    def insertAction(self, before: QAction, action: QAction):
        return self.bar.insertAction(before, action)

    def addSeparator(self):
        self.bar.addSeparator()

    def insertSeparator(self, index: int):
        self.bar.insertSeparator(index)

    def removeAction(self, action: QAction):
        self.bar.removeAction(action)

    def removeWidget(self, widget: QWidget):
        self.bar.removeWidget(widget)

    def removeHiddenAction(self, action: QAction):
        self.bar.removeAction(action)

    def setToolButtonStyle(self, style: Qt.ToolButtonStyle):
        self.bar.setToolButtonStyle(style)

    def toolButtonStyle(self):
        return self.bar.toolButtonStyle()

    def setButtonTight(self, isTight: bool):
        self.bar.setButtonTight(isTight)

    def isButtonTight(self):
        return self.bar.isButtonTight()

    def setIconSize(self, size: QSize):
        self.bar.setIconSize(size)

    def iconSize(self):
        return self.bar.iconSize()

    def setFont(self, font: QFont):
        self.bar.setFont(font)

    def setMenuDropDown(self, down: bool):
        self.bar.setMenuDropDown(down)

    def suitableWidth(self):
        m = self.contentsMargins()
        return m.left() + m.right() + self.bar.suitableWidth()

    def resizeToSuitableWidth(self):
        self.bar.resizeToSuitableWidth()
        self.setFixedWidth(self.suitableWidth())

    def actions(self):
        return self.bar.actions()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        path = QPainterPath()
        path.setFillRule(Qt.FillRule.WindingFill)
        path.addRoundedRect(QRectF(self.rect().adjusted(1, 1, -1, -1)), 8, 8)

        if self._isMenuVisible:
            y = self.height() - 10 if self.bar.isMenuDropDown() else 1
            path.addRect(1, y, self.width() - 2, 9)

        painter.setBrush(
            QColor(40, 40, 40) if isDarkTheme() else QColor(248, 248, 248))
        painter.setPen(
            QColor(56, 56, 56) if isDarkTheme() else QColor(233, 233, 233))
        painter.drawPath(path.simplified())
