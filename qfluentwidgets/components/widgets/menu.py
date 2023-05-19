# coding:utf-8
from enum import Enum
from typing import List, Union

from qframelesswindow import WindowEffect
from PyQt5.QtCore import (QEasingCurve, QEvent, QPropertyAnimation, QObject,
                          Qt, QSize, QRectF, pyqtSignal, QPoint, QTimer, QModelIndex)
from PyQt5.QtGui import QIcon, QColor, QPainter, QPen, QPixmap, QRegion, QCursor, QTextCursor, QHoverEvent
from PyQt5.QtWidgets import (QAction, QApplication, QMenu, QProxyStyle, QStyle,
                             QGraphicsDropShadowEffect, QListWidget, QWidget, QHBoxLayout,
                             QListWidgetItem, QLineEdit, QTextEdit, QStyledItemDelegate, QStyleOptionViewItem)

from ...common.smooth_scroll import SmoothScroll
from ...common.icon import FluentIcon as FIF
from ...common.icon import MenuIconEngine, Action, FluentIconBase, Icon
from ...common.style_sheet import FluentStyleSheet
from ...common.config import isDarkTheme


class CustomMenuStyle(QProxyStyle):
    """ Custom menu style """

    def __init__(self, iconSize=14):
        """
        Parameters
        ----------
        iconSizeL int
            the size of icon
        """
        super().__init__()
        self.iconSize = iconSize

    def pixelMetric(self, metric, option, widget):
        if metric == QStyle.PM_SmallIconSize:
            return self.iconSize

        return super().pixelMetric(metric, option, widget)


class DWMMenu(QMenu):
    """ A menu with DWM shadow """

    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.windowEffect = WindowEffect(self)
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.Popup | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setStyle(CustomMenuStyle())
        FluentStyleSheet.MENU.apply(self)

    def event(self, e: QEvent):
        if e.type() == QEvent.WinIdChange:
            self.windowEffect.addMenuShadowEffect(self.winId())
        return QMenu.event(self, e)



class SubMenuItemWidget(QWidget):
    """ Sub menu item """

    showMenuSig = pyqtSignal(QListWidgetItem)

    def __init__(self, menu, item, parent=None):
        """
        Parameters
        ----------
        menu: QMenu | RoundMenu
            sub menu

        item: QListWidgetItem
            menu item

        parent: QWidget
            parent widget
        """
        super().__init__(parent)
        self.menu = menu
        self.item = item

    def enterEvent(self, e):
        super().enterEvent(e)
        self.showMenuSig.emit(self.item)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        # draw right arrow
        FIF.CHEVRON_RIGHT.render(painter, QRectF(
            self.width()-10, self.height()/2-9/2, 9, 9))


class MenuItemDelegate(QStyledItemDelegate):
    """ Menu item delegate """

    def paint(self, painter, option, index):
        if index.model().data(index, Qt.DecorationRole) != "seperator":
            return super().paint(painter, option, index)

        # draw seperator
        painter.save()

        c = 0 if not isDarkTheme() else 255
        pen = QPen(QColor(c, c, c, 25), 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        rect = option.rect
        painter.drawLine(0, rect.y() + 4, rect.width() + 12, rect.y() + 4)

        painter.restore()


class MenuActionListWidget(QListWidget):
    """ Menu action list widget """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setViewportMargins(0, 6, 0, 6)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTextElideMode(Qt.ElideNone)
        self.setDragEnabled(False)
        self.setMouseTracking(True)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.setIconSize(QSize(14, 14))
        self.setItemDelegate(MenuItemDelegate(self))

        self.smoothScroll = SmoothScroll(self)
        self.setStyleSheet(
            'MenuActionListWidget{font: 14px "Segoe UI", "Microsoft YaHei"}')

    def wheelEvent(self, e):
        self.smoothScroll.wheelEvent(e)
        e.setAccepted(True)

    def insertItem(self, row, item):
        """ inserts menu item at the position in the list given by row """
        super().insertItem(row, item)
        self.adjustSize()

    def addItem(self, item):
        """ add menu item at the end """
        super().addItem(item)
        self.adjustSize()

    def takeItem(self, row):
        """ delete item from list """
        item = super().takeItem(row)
        self.adjustSize()
        return item

    def adjustSize(self):
        size = QSize()
        for i in range(self.count()):
            s = self.item(i).sizeHint()
            size.setWidth(max(s.width(), size.width()))
            size.setHeight(size.height() + s.height())

        # adjust the height of viewport
        ss = QApplication.screenAt(QCursor.pos()).availableSize()
        w, h = ss.width() - 100, ss.height() - 100
        vsize = QSize(size)
        vsize.setHeight(min(h-12, vsize.height()))
        vsize.setWidth(min(w-12, vsize.width()))
        self.viewport().adjustSize()

        # adjust the height of list widget
        m = self.viewportMargins()
        size += QSize(m.left()+m.right()+2, m.top()+m.bottom())
        size.setHeight(min(h, size.height()+3))
        size.setWidth(min(w, size.width()))
        self.setFixedSize(size)

    def setItemHeight(self, height):
        """ set the height of item """
        for i in range(self.count()):
            item = self.item(i)
            item.setSizeHint(item.sizeHint().width(), height)

        self.adjustSize()


class MenuAnimationType(Enum):
    """ Menu animation type """

    NONE = 0
    DROP_DOWN = 1
    PULL_UP = 2


class RoundMenu(QWidget):
    """ Round corner menu """

    closedSignal = pyqtSignal()

    def __init__(self, title="", parent=None):
        super().__init__(parent=parent)
        self._title = title
        self._icon = QIcon()
        self._actions = []  # type: List[QAction]
        self._subMenus = []

        self.isSubMenu = False
        self.parentMenu = None
        self.menuItem = None
        self.lastHoverItem = None
        self.lastHoverSubMenuItem = None
        self.isHideBySystem = True
        self.itemHeight = 28

        self.hBoxLayout = QHBoxLayout(self)
        self.view = MenuActionListWidget(self)

        self.aniManager = None
        self.ani = QPropertyAnimation(self, b'pos', self)
        self.timer = QTimer(self)

        self.__initWidgets()

    def __initWidgets(self):
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint |
                            Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self.timer.setSingleShot(True)
        self.timer.setInterval(400)
        self.timer.timeout.connect(self._onShowMenuTimeOut)

        self.setShadowEffect()
        self.hBoxLayout.addWidget(self.view, 1, Qt.AlignCenter)

        self.hBoxLayout.setContentsMargins(12, 8, 12, 20)
        FluentStyleSheet.MENU.apply(self)

        self.view.itemClicked.connect(self._onItemClicked)
        self.view.itemEntered.connect(self._onItemEntered)

    def setItemHeight(self, height):
        """ set the height of menu item """
        if height == self.itemHeight:
            return

        self.itemHeight = height
        self.view.setItemHeight(height)

    def setShadowEffect(self, blurRadius=30, offset=(0, 8), color=QColor(0, 0, 0, 30)):
        """ add shadow to dialog """
        self.shadowEffect = QGraphicsDropShadowEffect(self.view)
        self.shadowEffect.setBlurRadius(blurRadius)
        self.shadowEffect.setOffset(*offset)
        self.shadowEffect.setColor(color)
        self.view.setGraphicsEffect(None)
        self.view.setGraphicsEffect(self.shadowEffect)

    def _setParentMenu(self, parent, item):
        self.parentMenu = parent
        self.menuItem = item
        self.isSubMenu = True if parent else False

    def adjustSize(self):
        m = self.layout().contentsMargins()
        w = self.view.width() + m.left() + m.right()
        h = self.view.height() + m.top() + m.bottom()
        self.setFixedSize(w, h)

    def icon(self):
        return self._icon

    def title(self):
        return self._title

    def clear(self):
        """ clear all actions """
        for i in range(len(self._actions)-1, -1, -1):
            self.removeAction(self._actions[i])

    def setIcon(self, icon: Union[QIcon, FluentIconBase]):
        """ set the icon of menu """
        if isinstance(icon, FluentIconBase):
            icon = Icon(icon)

        self._icon = icon

    def addAction(self, action: Union[QAction, Action]):
        """ add action to menu

        Parameters
        ----------
        action: QAction
            menu action
        """
        item = self._createActionItem(action)
        self.view.addItem(item)
        self.adjustSize()

    def _createActionItem(self, action, before=None):
        """ create menu action item  """
        if not before:
            self._actions.append(action)
        elif before in self._actions:
            index = self._actions.index(before)
            self._actions.insert(index, action)
        else:
            raise ValueError('`before` is not in the action list')

        item = QListWidgetItem(self._createItemIcon(action), action.text())
        if not self._hasItemIcon():
            w = 40 + self.view.fontMetrics().width(action.text())
        else:
            # add a blank character to increase space between icon and text
            item.setText(" " + item.text())
            w = 60 + self.view.fontMetrics().width(item.text())

        item.setSizeHint(QSize(w, self.itemHeight))
        item.setData(Qt.UserRole, action)
        action.setProperty('item', item)
        action.changed.connect(self._onActionChanged)
        return item

    def _hasItemIcon(self):
        return any(not i.icon().isNull() for i in self._actions+self._subMenus)

    def _createItemIcon(self, w):
        """ create the icon of menu item """
        hasIcon = self._hasItemIcon()
        icon = QIcon(MenuIconEngine(w.icon()))

        if hasIcon and w.icon().isNull():
            pixmap = QPixmap(self.view.iconSize())
            pixmap.fill(Qt.transparent)
            icon = QIcon(pixmap)
        elif not hasIcon:
            icon = QIcon()

        return icon

    def insertAction(self, before: Union[QAction, Action], action: Union[QAction, Action]):
        """ inserts action to menu, before the action before """
        if before not in self._actions:
            return

        beforeItem = before.property('item')
        if not beforeItem:
            return

        index = self.view.row(beforeItem)
        item = self._createActionItem(action, before)
        self.view.insertItem(index, item)
        self.adjustSize()

    def addActions(self, actions: List[Union[QAction, Action]]):
        """ add actions to menu

        Parameters
        ----------
        actions: Iterable[QAction]
            menu actions
        """
        for action in actions:
            self.addAction(action)

    def insertActions(self, before: Union[QAction, Action], actions: List[Union[QAction, Action]]):
        """ inserts the actions actions to menu, before the action before """
        for action in actions:
            self.insertAction(before, action)

    def removeAction(self, action: Union[QAction, Action]):
        """ remove action from menu """
        if action not in self._actions:
            return

        index = self._actions.index(action)
        self._actions.remove(action)
        action.setProperty('item', None)
        item = self.view.takeItem(index)
        item.setData(Qt.UserRole, None)

        # delete widget
        widget = self.view.itemWidget(item)
        if widget:
            widget.deleteLater()

    def setDefaultAction(self, action: Union[QAction, Action]):
        """ set the default action """
        if action not in self._actions:
            return

        index = self._actions.index(action)
        self.view.setCurrentRow(index)

    def addMenu(self, menu):
        """ add sub menu

        Parameters
        ----------
        menu: RoundMenu
            sub round menu
        """
        if not isinstance(menu, RoundMenu):
            raise ValueError('`menu` should be an instance of `RoundMenu`.')

        item, w = self._createSubMenuItem(menu)
        self.view.addItem(item)
        self.view.setItemWidget(item, w)
        self.adjustSize()

    def insertMenu(self, before: Union[QAction, Action], menu):
        """ insert menu before action `before` """
        if not isinstance(menu, RoundMenu):
            raise ValueError('`menu` should be an instance of `RoundMenu`.')

        if before not in self._actions:
            raise ValueError('`before` should be in menu action list')

        item, w = self._createSubMenuItem(menu)
        self.view.insertItem(self.view.row(before.property('item')), item)
        self.view.setItemWidget(item, w)
        self.adjustSize()

    def _createSubMenuItem(self, menu):
        self._subMenus.append(menu)

        item = QListWidgetItem(self._createItemIcon(menu), menu.title())
        if not self._hasItemIcon():
            w = 60 + self.view.fontMetrics().width(menu.title())
        else:
            # add a blank character to increase space between icon and text
            item.setText(" " + item.text())
            w = 72 + self.view.fontMetrics().width(item.text())

        # add submenu item
        menu._setParentMenu(self, item)
        item.setSizeHint(QSize(w, self.itemHeight))
        item.setData(Qt.UserRole, menu)
        w = SubMenuItemWidget(menu, item, self)
        w.showMenuSig.connect(self._showSubMenu)
        w.resize(item.sizeHint())

        return item, w

    def _showSubMenu(self, item):
        """ show sub menu """
        self.lastHoverItem = item
        self.lastHoverSubMenuItem = item
        # delay 400 ms to anti-shake
        self.timer.stop()
        self.timer.start()

    def _onShowMenuTimeOut(self):
        if self.lastHoverSubMenuItem is None or not self.lastHoverItem is self.lastHoverSubMenuItem:
            return

        w = self.view.itemWidget(self.lastHoverSubMenuItem)

        if w.menu.parentMenu.isHidden():
            return

        pos = w.mapToGlobal(QPoint(w.width()+5, -5))
        w.menu.exec(pos)

    def addSeparator(self):
        """ add seperator to menu """
        m = self.view.viewportMargins()
        w = self.view.width()-m.left()-m.right()

        # add separator to list widget
        item = QListWidgetItem(self.view)
        item.setFlags(Qt.NoItemFlags)
        item.setSizeHint(QSize(w, 9))
        self.view.addItem(item)
        item.setData(Qt.DecorationRole, "seperator")
        self.adjustSize()

    def _onItemClicked(self, item):
        action = item.data(Qt.UserRole)
        if action not in self._actions or not action.isEnabled():
            return

        self._hideMenu(False)

        if not self.isSubMenu:
            action.trigger()
            return

        # close parent menu
        self._closeParentMenu()
        action.trigger()

    def _closeParentMenu(self):
        menu = self
        while menu:
            menu.close()
            menu = menu.parentMenu

    def _onItemEntered(self, item):
        self.lastHoverItem = item
        if not isinstance(item.data(Qt.UserRole), RoundMenu):
            return

        self._showSubMenu(item)

    def _hideMenu(self, isHideBySystem=False):
        self.isHideBySystem = isHideBySystem
        self.view.clearSelection()
        if self.isSubMenu:
            self.hide()
        else:
            self.close()

    def hideEvent(self, e):
        if self.isHideBySystem and self.isSubMenu:
            self._closeParentMenu()

        self.isHideBySystem = True
        e.accept()

    def closeEvent(self, e):
        e.accept()
        self.closedSignal.emit()
        self.view.clearSelection()

    def menuActions(self):
        return self._actions

    def mousePressEvent(self, e):
        if self.childAt(e.pos()) is not self.view:
            self._hideMenu(True)

    def mouseMoveEvent(self, e):
        if not self.isSubMenu:
            return

        # hide submenu when mouse moves out of submenu item
        pos = e.globalPos()
        view = self.parentMenu.view

        # get the rect of menu item
        margin = view.viewportMargins()
        rect = view.visualItemRect(self.menuItem).translated(
            view.mapToGlobal(QPoint()))
        rect = rect.translated(margin.left(), margin.top()+2)
        if self.parentMenu.geometry().contains(pos) and not rect.contains(pos) and \
                not self.geometry().contains(pos):
            view.clearSelection()
            self._hideMenu(False)

    def _onActionChanged(self):
        """ action changed slot """
        action = self.sender()  # type: QAction
        item = action.property('item')  # type: QListWidgetItem
        item.setIcon(self._createItemIcon(action))

        if not self._hasItemIcon():
            item.setText(action.text())
            w = 28 + self.view.fontMetrics().width(action.text())
        else:
            # add a blank character to increase space between icon and text
            item.setText(" " + action.text())
            w = 60 + self.view.fontMetrics().width(item.text())

        item.setSizeHint(QSize(w, self.itemHeight))

        if action.isEnabled():
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        else:
            item.setFlags(Qt.NoItemFlags)

        self.view.adjustSize()
        self.adjustSize()

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        """ show menu

        Parameters
        ----------
        pos: QPoint
            pop-up position

        ani: bool
            Whether to show pop-up animation

        aniType: MenuAnimationType
            menu animation type
        """
        if self.isVisible():
            return

        self.aniManager = MenuAnimationManager.make(self, aniType)
        self.aniManager.exec(pos)

        self.show()

        if self.isSubMenu:
            self.menuItem.setSelected(True)

    def exec_(self, pos: QPoint, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        """ show menu

        Parameters
        ----------
        pos: QPoint
            pop-up position

        ani: bool
            Whether to show pop-up animation

        aniType: MenuAnimationType
            menu animation type
        """
        self.exec(pos, ani, aniType)


class MenuAnimationManager(QObject):
    """ Menu animation manager """

    managers = {}

    def __init__(self, menu: RoundMenu):
        super().__init__()
        self.menu = menu
        self.ani = QPropertyAnimation(menu, b'pos', menu)

        self.ani.setDuration(250)
        self.ani.setEasingCurve(QEasingCurve.OutQuad)
        self.ani.valueChanged.connect(self._onValueChanged)
        self.ani.valueChanged.connect(self._updateMenuViewport)

    def _onValueChanged(self):
        raise NotImplementedError

    def _updateMenuViewport(self):
        self.menu.view.viewport().update()
        self.menu.view.setAttribute(Qt.WA_UnderMouse, True)
        e = QHoverEvent(QEvent.HoverEnter, QPoint(), QPoint(1, 1))
        QApplication.sendEvent(self.menu.view, e)

    def _endPosition(self, pos):
        m = self.menu
        rect = QApplication.screenAt(QCursor.pos()).availableGeometry()
        w, h = m.width() + 5, m.height() + 5
        x = min(pos.x() - m.layout().contentsMargins().left(), rect.right() - w)
        y = min(pos.y() - 4, rect.bottom() - h)
        return QPoint(x, y)

    def _menuSize(self):
        m = self.menu.layout().contentsMargins()
        w = self.menu.view.width() + m.left() + m.right() + 120
        h = self.menu.view.height() + m.top() + m.bottom() + 20
        return w, h

    def exec(self, pos: QPoint):
        self._initAni(pos)

    @classmethod
    def register(cls, name):
        """ register menu animation manager

        Parameters
        ----------
        name: Any
            the name of manager, it should be unique
        """
        def wrapper(Manager):
            if name not in cls.managers:
                cls.managers[name] = Manager

            return Manager

        return wrapper

    @classmethod
    def make(cls, menu: RoundMenu, aniType: MenuAnimationType):
        if aniType not in cls.managers:
            raise ValueError(f'`{aniType}` is an invalid menu animation type.')

        return cls.managers[aniType](menu)


@MenuAnimationManager.register(MenuAnimationType.NONE)
class DummyMenuAnimationManager(MenuAnimationManager):
    """ Dummy menu animation manager """

    def exec(self, pos: QPoint):
        self.menu.move(self._endPosition(pos))


@MenuAnimationManager.register(MenuAnimationType.DROP_DOWN)
class DropDownMenuAnimationManager(MenuAnimationManager):
    """ Drop down menu animation manager """

    def exec(self, pos):
        pos = self._endPosition(pos)
        h = self.menu.height() + 5

        self.ani.setStartValue(pos-QPoint(0, int(h/2)))
        self.ani.setEndValue(pos)
        self.ani.start()

    def _onValueChanged(self):
        w, h = self._menuSize()
        y = self.ani.endValue().y() - self.ani.currentValue().y()
        self.menu.setMask(QRegion(0, y, w, h))


@MenuAnimationManager.register(MenuAnimationType.PULL_UP)
class PullUpMenuAnimationManager(MenuAnimationManager):
    """ Pull up menu animation manager """

    def _endPosition(self, pos):
        m = self.menu
        rect = QApplication.screenAt(QCursor.pos()).availableGeometry()
        w, h = m.width() + 5, m.height()
        x = min(pos.x() - m.layout().contentsMargins().left(), rect.right() - w)
        y = max(pos.y() - h + 15, 4)
        return QPoint(x, y)

    def exec(self, pos):
        pos = self._endPosition(pos)
        h = self.menu.height() + 5

        self.ani.setStartValue(pos+QPoint(0, int(h/2)))
        self.ani.setEndValue(pos)
        self.ani.start()

    def _onValueChanged(self):
        w, h = self._menuSize()
        y = self.ani.endValue().y() - self.ani.currentValue().y()
        self.menu.setMask(QRegion(0, y, w, h))


class EditMenu(RoundMenu):
    """ Edit menu """

    def createActions(self):
        self.cutAct = QAction(
            FIF.CUT.icon(),
            self.tr("Cut"),
            self,
            shortcut="Ctrl+X",
            triggered=self.parent().cut,
        )
        self.copyAct = QAction(
            FIF.COPY.icon(),
            self.tr("Copy"),
            self,
            shortcut="Ctrl+C",
            triggered=self.parent().copy,
        )
        self.pasteAct = QAction(
            FIF.PASTE.icon(),
            self.tr("Paste"),
            self,
            shortcut="Ctrl+V",
            triggered=self.parent().paste,
        )
        self.cancelAct = QAction(
            FIF.CANCEL.icon(),
            self.tr("Cancel"),
            self,
            shortcut="Ctrl+Z",
            triggered=self.parent().undo,
        )
        self.selectAllAct = QAction(
            self.tr("Select all"),
            self,
            shortcut="Ctrl+A",
            triggered=self.parent().selectAll
        )
        self.action_list = [
            self.cutAct, self.copyAct,
            self.pasteAct, self.cancelAct, self.selectAllAct
        ]

    def _parentText(self):
        raise NotImplementedError

    def _parentSelectedText(self):
        raise NotImplementedError

    def exec(self, pos, ani=True):
        self.clear()
        self.createActions()

        if QApplication.clipboard().mimeData().hasText():
            if self._parentText():
                if self._parentSelectedText():
                    self.addActions(self.action_list)
                else:
                    self.addActions(self.action_list[2:])
            else:
                self.addAction(self.pasteAct)
        else:
            if self._parentText():
                if self._parentSelectedText():
                    self.addActions(
                        self.action_list[:2] + self.action_list[3:])
                else:
                    self.addActions(self.action_list[3:])
            else:
                return

        super().exec(pos, ani)


class LineEditMenu(EditMenu):
    """ Line edit menu """

    def __init__(self, parent: QLineEdit):
        super().__init__("", parent)
        self.selectionStart = parent.selectionStart()
        self.selectionLength = parent.selectionLength()

    def _onItemClicked(self, item):
        if self.selectionStart >= 0:
            self.parent().setSelection(self.selectionStart, self.selectionLength)

        super()._onItemClicked(item)

    def _parentText(self):
        return self.parent().text()

    def _parentSelectedText(self):
        return self.parent().selectedText()


class TextEditMenu(EditMenu):
    """ Text edit menu """

    def __init__(self, parent: QTextEdit):
        super().__init__("", parent)
        cursor = parent.textCursor()
        self.selectionStart = cursor.selectionStart()
        self.selectionLength = cursor.selectionEnd() - self.selectionStart + 1

    def _parentText(self):
        return self.parent().toPlainText()

    def _parentSelectedText(self):
        return self.parent().textCursor().selectedText()

    def _onItemClicked(self, item):
        if self.selectionStart >= 0:
            cursor = self.parent().textCursor()
            cursor.setPosition(self.selectionStart)
            cursor.movePosition(
                QTextCursor.Right, QTextCursor.KeepAnchor, self.selectionLength)

        super()._onItemClicked(item)
