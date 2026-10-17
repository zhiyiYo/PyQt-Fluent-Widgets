# coding:utf-8
from enum import Enum
from typing import List, Union
import math

from qframelesswindow import WindowEffect
from PyQt5.QtCore import (QEasingCurve, QEvent, QPropertyAnimation, QObject, QModelIndex,
                          Qt, QSize, QRectF, pyqtSignal, QPoint, QTimer, QParallelAnimationGroup, QRect, QPointF, QVariantAnimation)
from PyQt5.QtGui import (QIcon, QColor, QPainter, QPen, QPixmap, QTextCursor, QMouseEvent,
                         QKeySequence, QTextLayout)
from PyQt5.QtWidgets import (QAction, QApplication, QMenu, QProxyStyle, QStyle,
                             QGraphicsDropShadowEffect, QListWidget, QWidget, QHBoxLayout,
                             QListWidgetItem, QLineEdit, QTextEdit, QStyledItemDelegate, QStyleOptionViewItem, QLabel)

from ...common.icon import FluentIcon as FIF
from ...common.icon import FluentIconEngine, Action, FluentIconBase, Icon
from ...common.style_sheet import FluentStyleSheet, themeColor
from ...common.screen import getCurrentScreenGeometry
from ...common.font import getFont, fontStyleSheet
from ...common.config import isDarkTheme, qconfig
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
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
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


class _MenuItemDelegate(MenuItemDelegate):
    """ Animated menu rows. """

    def __init__(self, view=None):
        super().__init__(view)
        self.view = None
        self._hoverRow = -1
        self._pressedRow = -1
        self._alphas = {}
        self._colorAni = QVariantAnimation(self)
        self._colorAni.setStartValue(0.0)
        self._colorAni.setEndValue(1.0)
        self._colorAni.setDuration(187)
        self._colorAni.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self._colorAni.valueChanged.connect(self._onColorChanged)
        qconfig.themeChanged.connect(self._updateColors)
        if isinstance(view, QListWidget):
            self._setView(view)

    def _setView(self, view):
        if self.view is view:
            return
        self._colorAni.stop()
        if self.view is not None:
            self.view.selectionModel().selectionChanged.disconnect(self._onSelectionChanged)
            self.view.entered.disconnect(self._onEntered)
            self.view.viewport().removeEventFilter(self)
        self.view = view
        if view is None:
            return
        self.setParent(view)
        view.selectionModel().selectionChanged.connect(self._onSelectionChanged)
        view.entered.connect(self._onEntered)
        view.viewport().installEventFilter(self)

    def _onSelectionChanged(self):
        self._updateColors()

    def _onEntered(self, index):
        self._hoverRow = index.row()
        self._updateColors()

    def eventFilter(self, object, event):
        if event is None or self.view is None:
            return False
        if event.type() == QEvent.Type.Leave:
            self._hoverRow = self._pressedRow = -1
        elif (isinstance(event, QMouseEvent) and event.type() == QEvent.Type.MouseButtonPress
              and event.button() == Qt.MouseButton.LeftButton):
            self._pressedRow = self.view.indexAt(event.pos()).row()
        elif event.type() == QEvent.Type.MouseButtonRelease:
            self._pressedRow = -1
        else:
            return super().eventFilter(object, event)
        self._updateColors()
        return super().eventFilter(object, event)

    def _updateColors(self):
        if self.view is None:
            return
        self._colorAni.stop()
        self._alphas = {row: alpha for row, alpha in self._alphas.items() if alpha}
        rows = set(self._alphas) | {self.view.currentRow(), self._hoverRow, self._pressedRow}
        self._fromAlphas = self._alphas.copy()
        self._toAlphas = {}
        isDark = isDarkTheme()
        for row in rows - {-1}:
            item = self.view.item(row)
            if item is None:
                continue
            enabled = bool(item.flags() & Qt.ItemFlag.ItemIsEnabled)
            active = item.isSelected() or row == self._hoverRow
            alpha = (15 if isDark else 10) if enabled and active else 0
            if enabled and row == self._pressedRow:
                alpha = 11 if isDark else 6
            self._toAlphas[row] = alpha
        self._colorAni.start()

    def _onColorChanged(self, progress):
        if self.view is None:
            return
        for row, end in self._toAlphas.items():
            start = self._fromAlphas.get(row, 0)
            self._alphas[row] = round(start + (end - start) * progress)
            self.view.viewport().update(self.view.visualItemRect(self.view.item(row)))

    def paint(self, painter, option, index):
        if self._isSeparator(index):
            return super().paint(painter, option, index)
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRectF(option.rect).adjusted(5, 3, -5, 0)
        color = QColor(Qt.GlobalColor.white if isDarkTheme() else Qt.GlobalColor.black)
        color.setAlpha(self._alphas.get(index.row(), 0))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(color)
        painter.drawRoundedRect(rect, 5, 5)
        painter.restore()

        styleOption = QStyleOptionViewItem(option)
        styleOption.state &= ~(QStyle.StateFlag.State_Selected | QStyle.StateFlag.State_MouseOver)
        super().paint(painter, styleOption, index)


class ShortcutMenuItemDelegate(_MenuItemDelegate):
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

        shortcut = action.shortcut().toString(QKeySequence.NativeText)

        # use text layout to calculate text width
        layout = QTextLayout(shortcut, font)
        layout.beginLayout()
        line = layout.createLine()
        line.setNumColumns(1)
        layout.endLayout()

        # draw text
        y = option.rect.y() + (option.rect.height() - layout.boundingRect().height()) / 2
        x = option.rect.right() - layout.boundingRect().width() - 20
        layout.draw(painter, QPointF(x, y))

        painter.restore()


class MenuActionListWidget(QListWidget):
    """ Menu action list widget """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._itemHeight = 38
        self._maxVisibleItems = -1  # adjust visible items according to the size of screen

        self.setViewportMargins(0, 2, 0, 2)
        self.setTextElideMode(Qt.TextElideMode.ElideRight)
        self.setDragEnabled(False)
        self.setMouseTracking(True)
        self.setIconSize(QSize(14, 14))
        self.setItemDelegate(ShortcutMenuItemDelegate(self))

        self.scrollDelegate = SmoothScrollDelegate(self)
        self.setStyleSheet('MenuActionListWidget{' + fontStyleSheet(getFont()) + '}')

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def setItemDelegate(self, delegate):
        previous = self.itemDelegate()
        if isinstance(previous, _MenuItemDelegate) and previous is not delegate and previous.view is self:
            previous._setView(None)
            previous.deleteLater()
        if isinstance(delegate, _MenuItemDelegate):
            delegate._setView(self)
        super().setItemDelegate(delegate)

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

    closedSignal = pyqtSignal()

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
        self.itemHeight = 38

        self.hBoxLayout = QHBoxLayout(self)
        self.view = MenuActionListWidget(self)

        self._isShowing = False
        self.aniManager = None
        self.timer = QTimer(self)

        self.__initWidgets()

        self._expandAni = QVariantAnimation(self)
        self._expandAni.setStartValue(0.0)
        self._expandAni.setEndValue(1.0)
        self._expandAni.setDuration(667)
        self._expandAni.setEasingCurve(QEasingCurve.Type.OutQuint)
        self._expandAni.valueChanged.connect(self._onExpandValueChanged)
        self._fadeAni = QPropertyAnimation(self, b'windowOpacity', self)
        self._fadeAni.setStartValue(0.0)
        self._fadeAni.setEndValue(1.0)
        self._fadeAni.setDuration(70)
        self._fadeAni.setEasingCurve(QEasingCurve.Type.InOutQuart)
        self._aniGroup = QParallelAnimationGroup(self)
        self._aniGroup.addAnimation(self._expandAni)
        self._aniGroup.addAnimation(self._fadeAni)
        self._aniGroup.finished.connect(self._onExpandFinished)

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

        self.hBoxLayout.setContentsMargins(24, 16, 24, 32)
        FluentStyleSheet.MENU.apply(self)

        self.view.itemClicked.connect(self._onItemClicked)
        self.view.itemEntered.connect(self._onItemEntered)

    def _setMenuGeometry(self):
        shadow = self.shadowEffect.boundingRectFor(QRectF()).toAlignedRect()
        margins = self.hBoxLayout.contentsMargins()
        self.hBoxLayout.setContentsMargins(max(margins.left(), -shadow.x()), max(margins.top(), -shadow.y()),
                                          max(margins.right(), shadow.x() + shadow.width()),
                                          max(margins.bottom(), shadow.y() + shadow.height()))
        self.hBoxLayout.setEnabled(False)
        margins = self.hBoxLayout.contentsMargins()
        self.setFixedSize(self._endRect.width() + margins.left() + margins.right(),
                          self._endRect.height() + margins.top() + margins.bottom())
        self.move(self._endRect.x() - margins.left(), self._endRect.y() - margins.top())

    def _scrollFor(self, height, mode):
        margins = self.view.viewportMargins()
        listHeight = height - margins.top() - margins.bottom() - 2 * self.view.frameWidth()
        scroll = self._selectedTop
        if mode == 2:
            scroll += self._rowHeight - listHeight
        elif mode == 0:
            scroll += (self._rowHeight - listHeight) / 2
        return max(0, min(round(scroll), self._contentHeight - listHeight))

    def _onExpandValueChanged(self, progress):
        height = round(self._startHeight + (self._endRect.height() - self._startHeight) * progress)
        y = round(self._startY + (self._endRect.y() - self._startY) * progress)
        margins = self.hBoxLayout.contentsMargins()
        # Keep the native popup fixed while its contents expand.
        if self.view.height() != height:
            self.view.setFixedHeight(height)
            self.view.doItemsLayout()
        self.view.move(margins.left(), margins.top() + y - self._endRect.y())
        scroll = (self._scrollFor(height, self._mode) if self._mode else
                  round(self._startScroll + (self._endScroll - self._startScroll) * progress))
        # Expansion owns scrolling until its final frame.
        self.view.scrollDelegate.vScrollBar.scrollTo(scroll, useAni=False)

    def _onExpandFinished(self):
        self._onExpandValueChanged(1.0)
        self.view.scrollDelegate.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

    def _prepareMenu(self):
        pass

    def _showMenu(self, ani=True):
        viewport = self.view.viewport()
        if viewport is not None:
            viewport.installEventFilter(self)
        self._onExpandValueChanged(1.0)
        self._prepareMenu()
        delegate = self.view.itemDelegate()
        if isinstance(delegate, _MenuItemDelegate):
            delegate._updateColors()
        if isinstance(delegate, IndicatorMenuItemDelegate) and self.view.selectedItems():
            delegate._indicatorAni.stop()
            delegate._indicatorAni.start()
        self.view.scrollDelegate.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._onExpandValueChanged(0.0 if ani else 1.0)
        self.setWindowOpacity(0.0 if ani else 1.0)
        self._isShowing = True
        self.show()
        self._isShowing = False
        self._onExpandValueChanged(0.0 if ani else 1.0)
        if ani:
            self._aniGroup.start()
        else:
            self._onExpandFinished()

    def _execAnimation(self, pos, mode=1, ani=True):
        self._aniGroup.stop()
        bounds = getCurrentScreenGeometry().adjusted(8, 8, -8, -8)
        width = min(self.view.width(), bounds.width())
        height = min(self.view.height(), bounds.height())
        self.view.setFixedSize(width, height)
        self.view.doItemsLayout()
        margins = self.hBoxLayout.contentsMargins()
        x = max(bounds.left(), min(pos.x() + margins.left(), bounds.right() + 1 - width))
        y = max(bounds.top(), min(pos.y() + margins.top(), bounds.bottom() + 1 - height))
        self._endRect = QRect(x, y, width, height)
        self._contentHeight = sum(self.view.sizeHintForRow(i) for i in range(self.view.count()))
        item = self.view.currentItem()
        self._selectedTop = self.view.visualItemRect(item).top() + self.view.scrollDelegate.vScrollBar.value() if item else 0
        self._rowHeight = item.sizeHint().height() if item else self.itemHeight
        self._mode = mode
        self._startHeight = min(46, height)
        self._startY = y + height - self._startHeight if mode == 2 else y
        self._startScroll = self._scrollFor(self._startHeight, mode)
        self._endScroll = self._scrollFor(height, mode)
        self._setMenuGeometry()
        self._showMenu(ani)

    def eventFilter(self, obj, e):
        if obj is self.view.viewport() and e.type() == QEvent.Type.Wheel:
            if self._aniGroup.state() == QParallelAnimationGroup.State.Running:
                self._aniGroup.stop()
                self.setWindowOpacity(1.0)
                self._onExpandFinished()
        return super().eventFilter(obj, e)

    def showEvent(self, e):
        super().showEvent(e)
        if not self._isShowing:
            self._execAnimation(self.pos())

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

    def setShadowEffect(self, blurRadius=24, offset=(0, 8), color=QColor(0, 0, 0, 36)):
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

    def sizeHint(self):
        m = self.hBoxLayout.contentsMargins()
        return self.view.size() + QSize(m.left() + m.right(), m.top() + m.bottom())

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
        font = getFont(12)
        maxWidth = 0

        for action in self.menuActions():
            shortcut = action.shortcut().toString(QKeySequence.NativeText)

            # use text layout to calculate width
            layout = QTextLayout(shortcut, font)
            layout.beginLayout()
            line = layout.createLine()
            line.setNumColumns(1)
            layout.endLayout()

            rect = layout.boundingRect()
            if rect.width() > maxWidth:
                maxWidth = rect.width()

        return math.ceil(maxWidth)

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

        itemRect = QRect(w.mapToGlobal(w.rect().topLeft()), w.size())
        x = itemRect.right() + 5
        y = itemRect.y() - 5

        screenRect = getCurrentScreenGeometry()
        subMenuSize = w.menu.sizeHint()
        if (x + subMenuSize.width()) > screenRect.right():
            x = max(itemRect.left() - subMenuSize.width() - 5, screenRect.left())

        if (y + subMenuSize.height()) > screenRect.bottom():
            y = screenRect.bottom() - subMenuSize.height()

        y = max(y, screenRect.top())

        w.menu.exec(QPoint(x, y))

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
        self._aniGroup.stop()
        if hasattr(self, '_endRect'):
            self._onExpandFinished()
        self.timer.stop()
        delegate = self.view.itemDelegate()
        if isinstance(delegate, _MenuItemDelegate):
            delegate._colorAni.stop()
            delegate._hoverRow = delegate._pressedRow = -1
            delegate._alphas.clear()
        if isinstance(delegate, IndicatorMenuItemDelegate):
            delegate._indicatorAni.stop()
        for menu in self._subMenus:
            menu.isHideBySystem = False
            menu.hide()
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
        self.aniManager = MenuAnimationManager.make(self, aniType if ani else MenuAnimationType.NONE)
        self.aniManager.exec(pos)

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
        self.ani = getattr(menu, '_expandAni', None)
        self.opacityAni = getattr(menu, '_fadeAni', None)
        self.aniGroup = getattr(menu, '_aniGroup', None)

    def availableViewSize(self, pos: QPoint):
        """ Return the available size of view """
        ss = getCurrentScreenGeometry()
        view = self.menu.view if isinstance(self.menu, RoundMenu) else self.menu
        height = ss.height() - 16
        if view.maxVisibleItems() <= 0:
            height = min(height, 300)
        return ss.width() - 16, height

    def _endPosition(self, pos):
        margins = self.menu.hBoxLayout.contentsMargins()
        return QPoint(pos.x() - margins.left(), pos.y() - margins.top() + 4)

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
        self.menu._execAnimation(self._endPosition(pos), ani=False)


@MenuAnimationManager.register(MenuAnimationType.DROP_DOWN)
class DropDownMenuAnimationManager(MenuAnimationManager):
    """ Drop down menu animation manager """

    def exec(self, pos):
        self.menu._execAnimation(self._endPosition(pos))

    def availableViewSize(self, pos: QPoint):
        width, height = super().availableViewSize(pos)
        ss = getCurrentScreenGeometry()
        return width, min(height, max(ss.bottom() - pos.y() - 8, 1))


@MenuAnimationManager.register(MenuAnimationType.PULL_UP)
class PullUpMenuAnimationManager(MenuAnimationManager):
    """ Pull up menu animation manager """

    def _endPosition(self, pos):
        margins = self.menu.hBoxLayout.contentsMargins()
        return QPoint(pos.x() - margins.left(), pos.y() - self.menu.view.height() - margins.top() - 4)

    def exec(self, pos):
        self.menu._execAnimation(self._endPosition(pos), mode=2)

    def availableViewSize(self, pos: QPoint):
        width, height = super().availableViewSize(pos)
        ss = getCurrentScreenGeometry()
        return width, min(height, max(pos.y() - ss.top() - 8, 1))


@MenuAnimationManager.register(MenuAnimationType.FADE_IN_DROP_DOWN)
class FadeInDropDownMenuAnimationManager(DropDownMenuAnimationManager):
    """ Fade in drop down menu animation manager """


@MenuAnimationManager.register(MenuAnimationType.FADE_IN_PULL_UP)
class FadeInPullUpMenuAnimationManager(PullUpMenuAnimationManager):
    """ Fade in pull up menu animation manager """


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

        if QApplication.clipboard().mimeData().hasText():
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


class IndicatorMenuItemDelegate(_MenuItemDelegate):
    """ Menu item delegate with indicator """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._indicatorAni = QVariantAnimation(self)
        self._indicatorAni.setStartValue(0.0)
        self._indicatorAni.setEndValue(1.0)
        self._indicatorAni.setDuration(667)
        self._indicatorAni.setEasingCurve(QEasingCurve.Type.OutQuint)
        self._indicatorAni.valueChanged.connect(self._updateCurrentItem)

    def _onSelectionChanged(self):
        super()._onSelectionChanged()
        self._indicatorAni.stop()
        self._indicatorAni.start()

    def _updateCurrentItem(self):
        if self.view is None:
            return
        item = self.view.currentItem()
        if item is not None:
            self.view.viewport().update(self.view.visualItemRect(item))

    def paint(self, painter, option, index):
        super().paint(painter, option, index)
        selected = bool(option.state & QStyle.StateFlag.State_Selected)
        rect = QRectF(option.rect).adjusted(5, 3, -5, 0)
        if selected:
            painter.save()
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            progress = (self._indicatorAni.currentValue() or 0.0) if self.view is not None else 1.0
            height = max(0, option.rect.height() - 23) * progress
            painter.setBrush(themeColor())
            painter.setPen(Qt.PenStyle.NoPen)
            opacity = min(1.0, self._indicatorAni.currentTime() / 250) if self.view is not None else 1.0
            painter.setOpacity(1 - (1 - opacity) ** 2)
            painter.drawRoundedRect(QRectF(rect.x(), rect.center().y() - height / 2, 3, height), 1.5, 1.5)
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
