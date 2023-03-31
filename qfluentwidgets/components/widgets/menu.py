# coding:utf-8
from qframelesswindow import WindowEffect
from PyQt6.QtCore import (QEasingCurve, QEvent, QPropertyAnimation, QRect,
                          Qt, QSize, QRectF, pyqtSignal, QPoint, QTimer)
from PyQt6.QtGui import QIcon, QAction, QColor, QPainter, QPen, QPixmap, QRegion, QCursor
from PyQt6.QtWidgets import (QApplication, QMenu, QProxyStyle, QStyle,
                             QGraphicsDropShadowEffect, QListWidget, QWidget, QHBoxLayout,
                             QListWidgetItem)

from ...common.smooth_scroll import SmoothScroll
from ...common.icon import FluentIcon as FIF
from ...common.icon import MenuIconEngine
from ...common.style_sheet import setStyleSheet
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
        if metric == QStyle.PixelMetric.PM_SmallIconSize:
            return self.iconSize

        return super().pixelMetric(metric, option, widget)


class DWMMenu(QMenu):
    """ A menu with DWM shadow """

    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.windowEffect = WindowEffect(self)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup | Qt.WindowType.NoDropShadowWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyle(CustomMenuStyle())
        setStyleSheet(self, 'menu')

    def event(self, e: QEvent):
        if e.type() == QEvent.Type.WinIdChange:
            self.windowEffect.addMenuShadowEffect(self.winId())
        return QMenu.event(self, e)



class MenuSeparator(QWidget):
    """ Menu separator """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(9)

    def paintEvent(self, e):
        painter = QPainter(self)
        c = 0 if not isDarkTheme() else 255
        pen = QPen(QColor(c, c, c, 25), 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(0, 4, self.width(), 4)


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
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        # draw right arrow
        FIF.CHEVRON_RIGHT.render(painter, QRectF(
            self.width()-10, self.height()/2-9/2, 9, 9))


class MenuActionListWidget(QListWidget):
    """ Menu action list widget """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setViewportMargins(5, 6, 5, 6)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.setDragEnabled(False)
        self.setMouseTracking(True)
        self.setVerticalScrollMode(self.ScrollMode.ScrollPerPixel)
        self.setIconSize(QSize(14, 14))
        self.smoothScroll = SmoothScroll(self)
        self.setStyleSheet(
            'MenuActionListWidget{font: 14px "Segoe UI", "Microsoft YaHei"}')

    def wheelEvent(self, e):
        self.smoothScroll.wheelEvent(e)

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
            item.setSizeHint(item.sizeHint().width(), i)

        self.adjustSize()


class RoundMenu(QWidget):
    """ Round corner menu """

    closedSignal = pyqtSignal()

    def __init__(self, title="", parent=None):
        super().__init__(parent=parent)
        self._title = title
        self._icon = QIcon()
        self._actions = []
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
        self.ani = QPropertyAnimation(self, b'pos', self)
        self.timer = QTimer(self)
        self.__initWidgets()

    def __initWidgets(self):
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.NoDropShadowWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMouseTracking(True)

        self.timer.setSingleShot(True)
        self.timer.setInterval(400)
        self.timer.timeout.connect(self._onShowMenuTimeOut)

        self.setShadowEffect()
        self.hBoxLayout.addWidget(self.view, 1, Qt.AlignmentFlag.AlignCenter)

        self.hBoxLayout.setContentsMargins(12, 8, 12, 20)
        setStyleSheet(self, 'menu')

        self.view.itemClicked.connect(self._onItemClicked)
        self.view.itemEntered.connect(self._onItemEntered)
        self.ani.valueChanged.connect(self._onSlideValueChanged)

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

    def setIcon(self, icon):
        """ set the icon of menu """
        self._icon = icon

    def addAction(self, action):
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
            w = 28 + self.view.fontMetrics().boundingRect(action.text()).width()
        else:
            # add a blank character to increase space between icon and text
            item.setText(" " + item.text())
            w = 60 + self.view.fontMetrics().boundingRect(item.text()).width()

        item.setSizeHint(QSize(w, self.itemHeight))
        item.setData(Qt.ItemDataRole.UserRole, action)
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
            pixmap.fill(Qt.GlobalColor.transparent)
            icon = QIcon(pixmap)
        elif not hasIcon:
            icon = QIcon()

        return icon

    def insertAction(self, before, action):
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

    def addActions(self, actions):
        """ add actions to menu

        Parameters
        ----------
        actions: Iterable[QAction]
            menu actions
        """
        for action in actions:
            self.addAction(action)

    def insertActions(self, before, actions):
        """ inserts the actions actions to menu, before the action before """
        for action in actions:
            self.insertAction(before, action)

    def removeAction(self, action):
        """ remove action from menu """
        if action not in self._actions:
            return

        index = self._actions.index(action)
        self._actions.remove(action)
        action.setProperty('item', None)
        item = self.view.takeItem(index)
        item.setData(Qt.ItemDataRole.UserRole, None)

        # delete widget
        widget = self.view.itemWidget(item)
        if widget:
            widget.deleteLater()

    def setDefaultAction(self, action):
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

    def insertMenu(self, before, menu):
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
            w = 48 + self.view.fontMetrics().boundingRect(menu.title()).width()
        else:
            # add a blank character to increase space between icon and text
            item.setText(" " + item.text())
            w = 60 + self.view.fontMetrics().boundingRect(item.text()).width()

        # add submenu item
        menu._setParentMenu(self, item)
        item.setSizeHint(QSize(w, self.itemHeight))
        item.setData(Qt.ItemDataRole.UserRole, menu)
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
        pos = w.mapToGlobal(QPoint(w.width()+5, -5))
        w.menu.exec(pos)

    def addSeparator(self):
        """ add seperator to menu """
        m = self.view.viewportMargins()
        w = self.view.width()-m.left()-m.right()

        # icon separator
        separator = MenuSeparator(self.view)
        separator.resize(w, separator.height())

        # add separator to list widget
        item = QListWidgetItem(self.view)
        item.setFlags(Qt.ItemFlag.NoItemFlags)
        item.setSizeHint(QSize(w, separator.height()))
        self.view.addItem(item)
        self.view.setItemWidget(item, separator)
        self.adjustSize()

    def _onItemClicked(self, item):
        action = item.data(Qt.ItemDataRole.UserRole)
        if action not in self._actions:
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
        while menu.parentMenu:
            menu.close()
            menu = menu.parentMenu

        menu.close()

    def _onItemEntered(self, item):
        self.lastHoverItem = item
        if not isinstance(item.data(Qt.ItemDataRole.UserRole), RoundMenu):
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

    def menuActions(self):
        return self._actions

    def mousePressEvent(self, e):
        if self.childAt(e.pos()) is not self.view:
            self._hideMenu(True)

    def mouseMoveEvent(self, e):
        if not self.isSubMenu:
            return

        # hide submenu when mouse moves out of submenu item
        pos = e.globalPosition().toPoint()
        view = self.parentMenu.view

        # get the rect of menu item
        margin = view.viewportMargins()
        rect = view.visualItemRect(self.menuItem).translated(view.mapToGlobal(QPoint()))
        rect= rect.translated(margin.left(), margin.top()+2)
        if self.parentMenu.geometry().contains(pos) and not rect.contains(pos) and \
                not self.geometry().contains(pos):
            view.clearSelection()
            self._hideMenu(False)

            # update style
            index = view.row(self.menuItem)
            if index > 0:
                view.item(index-1).setFlags(Qt.ItemFlag.ItemIsEnabled)
            if index < view.count()-1:
                view.item(index+1).setFlags(Qt.ItemFlag.ItemIsEnabled)

    def _onActionChanged(self):
        """ action changed slot """
        action = self.sender()
        item = action.property('item')
        item.setIcon(self._createItemIcon(action))

        if not self._hasItemIcon():
            item.setText(action.text())
            w = 28 + self.view.fontMetrics().boundingRect(action.text()).width()
        else:
            # add a blank character to increase space between icon and text
            item.setText(" " + action.text())
            w = 60 + self.view.fontMetrics().boundingRect(item.text()).width()

        item.setSizeHint(QSize(w, self.itemHeight))
        self.view.adjustSize()
        self.adjustSize()

    def _onActionChanged(self):
        """ action changed slot """
        action = self.sender()
        item = action.property('item')
        item.setIcon(self._createItemIcon(action))

        if not self._hasItemIcon():
            item.setText(action.text())
            w = 28 + self.view.fontMetrics().boundingRect(action.text()).width()
        else:
            # add a blank character to increase space between icon and text
            item.setText(" " + action.text())
            w = 60 + self.view.fontMetrics().boundingRect(item.text()).width()

        item.setSizeHint(QSize(w, self.itemHeight))
        self.view.adjustSize()
        self.adjustSize()

    def _onSlideValueChanged(self, pos):
        m = self.layout().contentsMargins()
        w = self.view.width() + m.left() + m.right() + 120
        h = self.view.height() + m.top() + m.bottom() + 20
        y = self.ani.endValue().y() - pos.y()
        self.setMask(QRegion(0, y, w, h))

    def exec(self, pos, ani=True):
        """ show menu

        Parameters
        ----------
        pos: QPoint
            pop-up position

        ani: bool
            Whether to show pop-up animation
        """
        if self.isVisible():
            return

        rect = QApplication.screenAt(QCursor.pos()).availableGeometry()
        w, h = self.width() + 5, self.height() + 5
        pos.setX(min(pos.x() - self.layout().contentsMargins().left(), rect.right() - w))
        pos.setY(min(pos.y() - 4, rect.bottom() - h))

        if ani:
            self.ani.setStartValue(pos-QPoint(0, h/2))
            self.ani.setEndValue(pos)
            self.ani.setDuration(250)
            self.ani.setEasingCurve(QEasingCurve.Type.OutQuad)
            self.ani.start()
        else:
            self.move(pos)

        self.show()

        if not self.isSubMenu:
            return

        self.menuItem.setSelected(True)

        # temporarily disable item to change style
        view = self.parentMenu.view
        index = view.row(self.menuItem)
        if index > 0:
            view.item(index-1).setFlags(Qt.ItemFlag.NoItemFlags)
        if index < view.count()-1:
            view.item(index+1).setFlags(Qt.ItemFlag.NoItemFlags)


class LineEditMenu(RoundMenu):
    """ Line edit menu """

    def __init__(self, parent):
        super().__init__("", parent)
        self.setProperty("selectAll", bool(self.parent().text()))
        self.selectionStart = parent.selectionStart()
        self.selectionLength = parent.selectionLength()

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
        self.action_list = [self.cutAct, self.copyAct,
                            self.pasteAct, self.cancelAct, self.selectAllAct]

    def _onItemClicked(self, item):
        if self.selectionLength:
            self.parent().setSelection(self.selectionStart, self.selectionLength)

        super()._onItemClicked(item)

    def exec(self, pos, ani=True):
        self.clear()
        self.createActions()

        if QApplication.clipboard().mimeData().hasText():
            if self.parent().text():
                if self.parent().selectedText():
                    self.addActions(self.action_list)
                else:
                    self.addActions(self.action_list[2:])
            else:
                self.addAction(self.pasteAct)
        else:
            if self.parent().text():
                if self.parent().selectedText():
                    self.addActions(
                        self.action_list[:2] + self.action_list[3:])
                else:
                    self.addActions(self.action_list[3:])
            else:
                return

        super().exec(pos, ani)
