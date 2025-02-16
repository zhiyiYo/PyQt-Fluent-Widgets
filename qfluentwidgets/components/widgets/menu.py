# coding:utf-8
from enum import Enum
from typing import List, Union

from qframelesswindow import WindowEffect
from PySide2.QtCore import (QEasingCurve, QEvent, QPropertyAnimation, QObject, QModelIndex,
                          Qt, QSize, QRectF, Signal, QPoint, QTimer, QParallelAnimationGroup)
from PySide2.QtGui import (QIcon, QColor, QPainter, QPen, QPixmap, QRegion, QCursor, QGuiApplication, QTextCursor, QHoverEvent,
                         QFontMetrics, QKeySequence)
from PySide2.QtWidgets import (QApplication, QAction, QMenu, QProxyStyle, QStyle,
                               QGraphicsDropShadowEffect, QListWidget, QWidget, QHBoxLayout,
                               QListWidgetItem, QLineEdit, QTextEdit, QStyledItemDelegate, QStyleOptionViewItem, QLabel)

from ...common.icon import FluentIcon as FIF
from ...common.icon import FluentIconEngine, Action, FluentIconBase, Icon
from ...common.style_sheet import FluentStyleSheet, themeColor
from ...common.screen import getCurrentScreenGeometry
from ...common.font import getFont
from ...common.config import isDarkTheme
from .scroll_bar import SmoothScrollDelegate
from .tool_tip import ItemViewToolTipDelegate, ItemViewToolTipType


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


class MenuAnimationType(Enum):
    """ Menu animation type """

    NONE = 0
    DROP_DOWN = 1
    PULL_UP = 2
    FADE_IN_DROP_DOWN = 3
    FADE_IN_PULL_UP = 4



class SubMenuItemWidget(QWidget):
    """ Sub menu item """

    showMenuSig = Signal(QListWidgetItem)

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

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tooltipDelegate = None

    def _isSeparator(self, index: QModelIndex):
        return index.model().data(index, Qt.DecorationRole) == "seperator"

    def paint(self, painter, option, index):
        if not self._isSeparator(index):
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

    def helpEvent(self, event, view, option, index):
        if not self.tooltipDelegate:
            self.tooltipDelegate = ItemViewToolTipDelegate(view, 100, ItemViewToolTipType.LIST)

        return self.tooltipDelegate.helpEvent(event, view, option, index)


class ShortcutMenuItemDelegate(MenuItemDelegate):
    """ Shortcut key menu item delegate """

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        super().paint(painter, option, index)
        if self._isSeparator(index):
            return

        # draw shortcut key
        action = index.data(Qt.UserRole)  # type: QAction
        if not isinstance(action, QAction) or action.shortcut().isEmpty():
            return

        painter.save()

        if not option.state & QStyle.State_Enabled:
            painter.setOpacity(0.5 if isDarkTheme() else 0.6)

        font = getFont(12)
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255, 200) if isDarkTheme() else QColor(0, 0, 0, 153))

        fm = QFontMetrics(font)
        shortcut = action.shortcut().toString(QKeySequence.NativeText)

        sw = fm.width(shortcut)
        painter.translate(option.rect.width()-sw-20, 0)

        rect = QRectF(0, option.rect.y(), sw, option.rect.height())
        painter.drawText(rect, Qt.AlignLeft | Qt.AlignVCenter, shortcut)

        painter.restore()


class MenuActionListWidget(QListWidget):
    """ Menu action list widget """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._itemHeight = 28
        self._maxVisibleItems = -1  # adjust visible items according to the size of screen

        self.setViewportMargins(0, 6, 0, 6)
        self.setTextElideMode(Qt.ElideNone)
        self.setDragEnabled(False)
        self.setMouseTracking(True)
        self.setIconSize(QSize(14, 14))
        self.setItemDelegate(ShortcutMenuItemDelegate(self))

        self.scrollDelegate = SmoothScrollDelegate(self)
        self.setStyleSheet(
            'MenuActionListWidget{font: 14px "Segoe UI", "Microsoft YaHei", "PingFang SC"}')

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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

    def adjustSize(self, pos=None, aniType=MenuAnimationType.NONE):
        size = QSize()
        for i in range(self.count()):
            s = self.item(i).sizeHint()
            size.setWidth(max(s.width(), size.width(), 1))
            size.setHeight(max(1, size.height() + s.height()))

        # adjust the height of viewport
        w, h = MenuAnimationManager.make(self, aniType).availableViewSize(pos)

        # fixes https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/844
        # self.viewport().adjustSize()

        # adjust the height of list widget
        m = self.viewportMargins()
        size += QSize(m.left()+m.right()+2, m.top()+m.bottom())
        size.setHeight(min(h, size.height()+3))
        size.setWidth(max(min(w, size.width()), self.minimumWidth()))

        if self.maxVisibleItems() > 0:
            size.setHeight(min(
                size.height(), self.maxVisibleItems() * self._itemHeight + m.top()+m.bottom() + 3))

        self.setFixedSize(size)

    def setItemHeight(self, height: int):
        """ set the height of item """
        if height == self._itemHeight:
            return

        for i in range(self.count()):
            item = self.item(i)
            if not self.itemWidget(item):
                item.setSizeHint(QSize(item.sizeHint().width(), height))

        self._itemHeight = height
        self.adjustSize()

    def setMaxVisibleItems(self, num: int):
        """ set the maximum visible items """
        self._maxVisibleItems = num
        self.adjustSize()

    def maxVisibleItems(self):
        return self._maxVisibleItems

    def heightForAnimation(self, pos: QPoint, aniType: MenuAnimationType):
        """ height for animation """
        ih = self.itemsHeight()
        _, sh = MenuAnimationManager.make(self, aniType).availableViewSize(pos)
        return min(ih, sh)

    def itemsHeight(self):
        """ Return the height of all items """
        N = self.count() if self.maxVisibleItems() < 0 else min(self.maxVisibleItems(), self.count())
        h = sum(self.item(i).sizeHint().height() for i in range(N))
        m = self.viewportMargins()
        return h + m.top() + m.bottom()


class RoundMenu(QMenu):
    """ Round corner menu """

    closedSignal = Signal()

    def __init__(self, title="", parent=None):
        super().__init__(parent=parent)
        self.setTitle(title)
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

    def setMaxVisibleItems(self, num: int):
        """ set the maximum visible items """
        self.view.setMaxVisibleItems(num)
        self.adjustSize()

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
        while self._actions:
            self.removeAction(self._actions[-1])

        while self._subMenus:
            self.removeMenu(self._subMenus[-1])

    def setIcon(self, icon: Union[QIcon, FluentIconBase]):
        """ set the icon of menu """
        if isinstance(icon, FluentIconBase):
            icon = Icon(icon)

        self._icon = icon

    def setTitle(self, title: str):
        self._title = title
        super().setTitle(title)

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

    def addWidget(self, widget: QWidget, selectable=True, onClick=None):
        """ add custom widget

        Parameters
        ----------
        widget: QWidget
            custom widget

        selectable: bool
            whether the menu item is selectable

        onClick: callable
            the slot connected to item clicked signal
        """
        action = QAction()
        action.setProperty('selectable', selectable)

        item = self._createActionItem(action)
        item.setSizeHint(widget.size())

        self.view.addItem(item)
        self.view.setItemWidget(item, widget)

        if not selectable:
            item.setFlags(Qt.NoItemFlags)

        if onClick:
            action.triggered.connect(onClick)

        self.adjustSize()

    def _createActionItem(self, action: QAction, before=None):
        """ create menu action item  """
        if not before:
            self._actions.append(action)
            super().addAction(action)
        elif before in self._actions:
            index = self._actions.index(before)
            self._actions.insert(index, action)
            super().insertAction(before, action)
        else:
            raise ValueError('`before` is not in the action list')

        item = QListWidgetItem(self._createItemIcon(action), action.text())
        self._adjustItemText(item, action)

        # disable item if the action is not enabled
        if not action.isEnabled():
            item.setFlags(Qt.NoItemFlags)
        if action.text() != action.toolTip():
            item.setToolTip(action.toolTip())

        item.setData(Qt.UserRole, action)
        action.setProperty('item', item)
        action.changed.connect(self._onActionChanged)
        return item

    def _hasItemIcon(self):
        return any(not i.icon().isNull() for i in self._actions+self._subMenus)

    def _adjustItemText(self, item: QListWidgetItem, action: QAction):
        """ adjust the text of item """
        # leave some space for shortcut key
        if isinstance(self.view.itemDelegate(), ShortcutMenuItemDelegate):
            sw = self._longestShortcutWidth()
            if sw:
                sw += 22
        else:
            sw = 0

        # adjust the width of item
        if not self._hasItemIcon():
            item.setText(action.text())
            w = 40 + self.view.fontMetrics().width(action.text()) + sw
        else:
            # add a blank character to increase space between icon and text
            item.setText(" " + action.text())
            space = 4 - self.view.fontMetrics().width(" ")
            w = 60 + self.view.fontMetrics().width(item.text()) + sw + space

        item.setSizeHint(QSize(w, self.itemHeight))
        return w

    def _longestShortcutWidth(self):
        """ longest shortcut key """
        fm = QFontMetrics(getFont(12))
        return max(fm.width(a.shortcut().toString()) for a in self.menuActions())

    def _createItemIcon(self, w):
        """ create the icon of menu item """
        hasIcon = self._hasItemIcon()
        icon = QIcon(FluentIconEngine(w.icon()))

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

        # remove action
        item = action.property("item")
        self._actions.remove(action)
        action.setProperty('item', None)

        if not item:
            return

        # remove item
        self._removeItem(item)
        super().removeAction(action)

    def removeMenu(self, menu):
        """ remove submenu """
        if menu not in self._subMenus:
            return

        item = menu.menuItem
        self._subMenus.remove(menu)
        self._removeItem(item)

    def setDefaultAction(self, action: Union[QAction, Action]):
        """ set the default action """
        if action not in self._actions:
            return

        item = action.property("item")
        if item:
            self.view.setCurrentItem(item)

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

    def _removeItem(self, item):
        self.view.takeItem(self.view.row(item))
        item.setData(Qt.UserRole, None)

        # delete widget
        widget = self.view.itemWidget(item)
        if widget:
            widget.deleteLater()

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
        item = QListWidgetItem()
        item.setFlags(Qt.NoItemFlags)
        item.setSizeHint(QSize(w, 9))
        self.view.addItem(item)
        item.setData(Qt.DecorationRole, "seperator")
        self.adjustSize()

    def _onItemClicked(self, item):
        action = item.data(Qt.UserRole)  # type: QAction
        if action not in self._actions or not action.isEnabled():
            return

        if self.view.itemWidget(item) and not action.property('selectable'):
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
        w = self.childAt(e.pos())
        if (w is not self.view) and (not self.view.isAncestorOf(w)):
            self._hideMenu(True)

    def mouseMoveEvent(self, e):
        if not self.isSubMenu:
            return

        # hide submenu when mouse moves out of submenu item
        pos = e.globalPos()
        view = self.parentMenu.view

        # get the rect of menu item
        margin = view.viewportMargins()
        rect = view.visualItemRect(self.menuItem).translated(view.mapToGlobal(QPoint()))
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

        if action.text() != action.toolTip():
            item.setToolTip(action.toolTip())

        self._adjustItemText(item, action)

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
        #if self.isVisible():
        #    aniType = MenuAnimationType.NONE

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

    def adjustPosition(self):
        m = self.layout().contentsMargins()
        rect = getCurrentScreenGeometry()
        w, h = self.layout().sizeHint().width() + 5, self.layout().sizeHint().height()

        x = min(self.x() - m.left(), rect.right() - w)
        y = self.y()
        if y > rect.bottom() - h:
            y = self.y() - h + m.bottom()

        self.move(x, y)

    def paintEvent(self, e):
        pass


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
        pass

    def availableViewSize(self, pos: QPoint):
        """ Return the available size of view """
        ss = getCurrentScreenGeometry()
        w, h = ss.width() - 100, ss.height() - 100
        return w, h

    def _updateMenuViewport(self):
        self.menu.view.viewport().update()
        self.menu.view.setAttribute(Qt.WA_UnderMouse, True)
        e = QHoverEvent(QEvent.HoverEnter, QPoint(), QPoint(1, 1))
        QApplication.sendEvent(self.menu.view, e)

    def _endPosition(self, pos):
        m = self.menu
        rect = getCurrentScreenGeometry()
        w, h = m.width() + 5, m.height()
        x = min(pos.x() - m.layout().contentsMargins().left(), rect.right() - w)
        y = min(pos.y() - 4, rect.bottom() - h + 10)

        return QPoint(x, y)

    def _menuSize(self):
        m = self.menu.layout().contentsMargins()
        w = self.menu.view.width() + m.left() + m.right() + 120
        h = self.menu.view.height() + m.top() + m.bottom() + 20
        return w, h

    def exec(self, pos: QPoint):
        pass

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

    def availableViewSize(self, pos: QPoint):
        ss = getCurrentScreenGeometry()
        return ss.width() - 100, max(ss.bottom() - pos.y() - 10, 1)

    def _onValueChanged(self):
        w, h = self._menuSize()
        y = self.ani.endValue().y() - self.ani.currentValue().y()
        self.menu.setMask(QRegion(0, y, w, h))


@MenuAnimationManager.register(MenuAnimationType.PULL_UP)
class PullUpMenuAnimationManager(MenuAnimationManager):
    """ Pull up menu animation manager """

    def _endPosition(self, pos):
        m = self.menu
        rect = getCurrentScreenGeometry()
        w, h = m.width() + 5, m.height()
        x = min(pos.x() - m.layout().contentsMargins().left(), rect.right() - w)
        y = max(pos.y() - h + 13, rect.top() + 4)
        return QPoint(x, y)

    def exec(self, pos):
        pos = self._endPosition(pos)
        h = self.menu.height() + 5

        self.ani.setStartValue(pos+QPoint(0, int(h/2)))
        self.ani.setEndValue(pos)
        self.ani.start()

    def availableViewSize(self, pos: QPoint):
        ss = getCurrentScreenGeometry()
        return ss.width() - 100, max(pos.y() - ss.top() - 28, 1)

    def _onValueChanged(self):
        w, h = self._menuSize()
        y = self.ani.endValue().y() - self.ani.currentValue().y()
        self.menu.setMask(QRegion(0, y, w, h - 28))


@MenuAnimationManager.register(MenuAnimationType.FADE_IN_DROP_DOWN)
class FadeInDropDownMenuAnimationManager(MenuAnimationManager):
    """ Fade in drop down menu animation manager """

    def __init__(self, menu: RoundMenu):
        super().__init__(menu)
        self.opacityAni = QPropertyAnimation(menu, b'windowOpacity', self)
        self.aniGroup = QParallelAnimationGroup(self)
        self.aniGroup.addAnimation(self.ani)
        self.aniGroup.addAnimation(self.opacityAni)

    def exec(self, pos):
        pos = self._endPosition(pos)

        self.opacityAni.setStartValue(0)
        self.opacityAni.setEndValue(1)
        self.opacityAni.setDuration(150)
        self.opacityAni.setEasingCurve(QEasingCurve.OutQuad)

        self.ani.setStartValue(pos-QPoint(0, 8))
        self.ani.setEndValue(pos)
        self.ani.setDuration(150)
        self.ani.setEasingCurve(QEasingCurve.OutQuad)

        self.aniGroup.start()

    def availableViewSize(self, pos: QPoint):
        ss = getCurrentScreenGeometry()
        return ss.width() - 100, max(ss.bottom() - pos.y() - 10, 1)


@MenuAnimationManager.register(MenuAnimationType.FADE_IN_PULL_UP)
class FadeInPullUpMenuAnimationManager(MenuAnimationManager):
    """ Fade in pull up menu animation manager """

    def __init__(self, menu: RoundMenu):
        super().__init__(menu)
        self.opacityAni = QPropertyAnimation(menu, b'windowOpacity', self)
        self.aniGroup = QParallelAnimationGroup(self)
        self.aniGroup.addAnimation(self.ani)
        self.aniGroup.addAnimation(self.opacityAni)

    def _endPosition(self, pos):
        m = self.menu
        rect = getCurrentScreenGeometry()
        w, h = m.width() + 5, m.height()
        x = min(pos.x() - m.layout().contentsMargins().left(), rect.right() - w)
        y = max(pos.y() - h + 15, rect.top() + 4)
        return QPoint(x, y)

    def exec(self, pos):
        pos = self._endPosition(pos)

        self.opacityAni.setStartValue(0)
        self.opacityAni.setEndValue(1)
        self.opacityAni.setDuration(150)
        self.opacityAni.setEasingCurve(QEasingCurve.OutQuad)

        self.ani.setStartValue(pos+QPoint(0, 8))
        self.ani.setEndValue(pos)
        self.ani.setDuration(200)
        self.ani.setEasingCurve(QEasingCurve.OutQuad)
        self.aniGroup.start()

    def availableViewSize(self, pos: QPoint):
        ss = getCurrentScreenGeometry()
        return ss.width() - 100, pos.y()- ss.top() - 28


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

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        self.clear()
        self.createActions()

        clipboard = QGuiApplication.clipboard()
        if clipboard.mimeData().hasText():
            if self._parentText():
                if self._parentSelectedText():
                    if self.parent().isReadOnly():
                        self.addActions([self.copyAct, self.selectAllAct])
                    else:
                        self.addActions(self.action_list)
                else:
                    if self.parent().isReadOnly():
                        self.addAction(self.selectAllAct)
                    else:
                        self.addActions(self.action_list[2:])
            elif not self.parent().isReadOnly():
                self.addAction(self.pasteAct)
            else:
                return
        else:
            if not self._parentText():
                return

            if self._parentSelectedText():
                if self.parent().isReadOnly():
                    self.addActions([self.copyAct, self.selectAllAct])
                else:
                    self.addActions(
                        self.action_list[:2] + self.action_list[3:])
            else:
                if self.parent().isReadOnly():
                    self.addAction(self.selectAllAct)
                else:
                    self.addActions(self.action_list[3:])

        super().exec(pos, ani, aniType)


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


class IndicatorMenuItemDelegate(MenuItemDelegate):
    """ Menu item delegate with indicator """

    def paint(self, painter: QPainter, option, index):
        super().paint(painter, option, index)
        if not option.state & QStyle.State_Selected:
            return

        painter.save()
        painter.setRenderHints(
            QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

        painter.setPen(Qt.NoPen)
        painter.setBrush(themeColor())
        painter.drawRoundedRect(6, 11+option.rect.y(), 3, 15, 1.5, 1.5)

        painter.restore()


class CheckableMenuItemDelegate(ShortcutMenuItemDelegate):
    """ Checkable menu item delegate """

    def _drawIndicator(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        raise NotImplementedError

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        super().paint(painter, option, index)

        # draw indicator
        action = index.data(Qt.UserRole)  # type: QAction
        if not (isinstance(action, QAction) and action.isChecked()):
            return

        painter.save()
        self._drawIndicator(painter, option, index)
        painter.restore()


class RadioIndicatorMenuItemDelegate(CheckableMenuItemDelegate):
    """ Checkable menu item delegate with radio indicator """

    def _drawIndicator(self, painter, option, index):
        rect = option.rect
        r = 5
        x = rect.x() + 22
        y = rect.center().y() - r / 2

        painter.setRenderHints(QPainter.Antialiasing)
        if not option.state & QStyle.State_MouseOver:
            painter.setOpacity(0.75 if isDarkTheme() else 0.65)

        painter.setPen(Qt.NoPen)
        painter.setBrush(Qt.white if isDarkTheme() else Qt.black)
        painter.drawEllipse(QRectF(x, y, r, r))


class CheckIndicatorMenuItemDelegate(CheckableMenuItemDelegate):
    """ Checkable menu item delegate with check indicator """

    def _drawIndicator(self, painter, option, index):
        rect = option.rect
        s = 11
        x = rect.x() + 19
        y = rect.center().y() - s / 2

        painter.setRenderHints(QPainter.Antialiasing)
        if not option.state & QStyle.State_MouseOver:
            painter.setOpacity(0.75)

        FIF.ACCEPT.render(painter, QRectF(x, y, s, s))


class MenuIndicatorType(Enum):
    """ Menu indicator type """
    CHECK = 0
    RADIO = 1


def createCheckableMenuItemDelegate(style: MenuIndicatorType):
    """ create checkable menu item delegate """
    if style == MenuIndicatorType.RADIO:
        return RadioIndicatorMenuItemDelegate()
    if style == MenuIndicatorType.CHECK:
        return CheckIndicatorMenuItemDelegate()

    raise ValueError(f'`{style}` is not a valid menu indicator type.')


class CheckableMenu(RoundMenu):
    """ Checkable menu """

    def __init__(self, title="", parent=None, indicatorType=MenuIndicatorType.CHECK):
        super().__init__(title, parent)
        self.view.setItemDelegate(createCheckableMenuItemDelegate(indicatorType))
        self.view.setObjectName('checkableListWidget')

    def _adjustItemText(self, item: QListWidgetItem, action: QAction):
        w = super()._adjustItemText(item, action)
        item.setSizeHint(QSize(w + 26, self.itemHeight))


class SystemTrayMenu(RoundMenu):
    """ System tray menu """

    def sizeHint(self) -> QSize:
        m = self.layout().contentsMargins()
        s = self.layout().sizeHint()
        return QSize(s.width() - m.right() + 5, s.height() - m.bottom())


class CheckableSystemTrayMenu(CheckableMenu):
    """ Checkable system tray menu """

    def sizeHint(self) -> QSize:
        m = self.layout().contentsMargins()
        s = self.layout().sizeHint()
        return QSize(s.width() - m.right() + 5, s.height() - m.bottom())


class LabelContextMenu(RoundMenu):
    """ Label context menu """

    def __init__(self, parent: QLabel):
        super().__init__("", parent)
        self.selectedText = parent.selectedText()

        self.copyAct = QAction(
            FIF.COPY.icon(),
            self.tr("Copy"),
            self,
            shortcut="Ctrl+C",
            triggered=self._onCopy
        )
        self.selectAllAct = QAction(
            self.tr("Select all"),
            self,
            shortcut="Ctrl+A",
            triggered=self._onSelectAll
        )

    def _onCopy(self):
        QApplication.clipboard().setText(self.selectedText)

    def _onSelectAll(self):
        self.label().setSelection(0, len(self.label().text()))

    def label(self) -> QLabel:
        return self.parent()

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        if self.label().hasSelectedText():
            self.addActions([self.copyAct, self.selectAllAct])
        else:
            self.addAction(self.selectAllAct)

        return super().exec(pos, ani, aniType)