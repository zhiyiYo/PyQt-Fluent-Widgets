# coding:utf-8
from qframelesswindow import WindowEffect
from PyQt5.QtCore import QEasingCurve, QEvent, QPropertyAnimation, QRect, Qt, QSize, QRectF
from PyQt5.QtGui import QIcon, QColor, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QMenu, QProxyStyle, QStyle,
                             QGraphicsDropShadowEffect, QListWidget, QWidget, QHBoxLayout,
                             QListWidgetItem, QStyleOptionViewItem)
from PyQt5.QtSvg import QSvgRenderer

from ...common.smooth_scroll import SmoothScroll
from ...common.icon import Icon, getIconColor
from ...common.style_sheet import setStyleSheet
from ...common.config import qconfig


class MenuIconFactory:
    """ Menu icon factory """

    CUT = "Cut"
    ADD = "Add"
    COPY = "Copy"
    PASTE = "Paste"
    CANCEL = "Cancel"
    FOLDER = "Folder"
    SETTING = "Setting"
    CHEVRON_RIGHT = "ChevronRight"

    @classmethod
    def create(cls, iconType: str):
        """ create icon """
        return QIcon(cls.path(iconType))

    @classmethod
    def path(cls, iconType: str):
        return f":/qfluentwidgets/images/menu/{iconType}_{getIconColor()}.svg"


MIF = MenuIconFactory


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
        setStyleSheet(self, 'menu')

    def event(self, e: QEvent):
        if e.type() == QEvent.WinIdChange:
            self.windowEffect.addMenuShadowEffect(self.winId())
        return QMenu.event(self, e)


class LineEditMenu(DWMMenu):
    """ Line edit menu """

    def __init__(self, parent):
        super().__init__("", parent)
        self.setObjectName("lineEditMenu")
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.setProperty("selectAll", bool(self.parent().text()))

    def createActions(self):
        self.cutAct = QAction(
            MIF.create(MIF.CUT),
            self.tr("Cut"),
            self,
            shortcut="Ctrl+X",
            triggered=self.parent().cut,
        )
        self.copyAct = QAction(
            MIF.create(MIF.COPY),
            self.tr("Copy"),
            self,
            shortcut="Ctrl+C",
            triggered=self.parent().copy,
        )
        self.pasteAct = QAction(
            MIF.create(MIF.PASTE),
            self.tr("Paste"),
            self,
            shortcut="Ctrl+V",
            triggered=self.parent().paste,
        )
        self.cancelAct = QAction(
            MIF.create(MIF.CANCEL),
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

    def exec_(self, pos):
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

        w = 92+max(self.fontMetrics().width(i.text()) for i in self.actions())
        h = len(self.actions()) * 32 + 8

        self.animation.setStartValue(QRect(pos.x(), pos.y(), 1, 1))
        self.animation.setEndValue(QRect(pos.x(), pos.y(), w, h))
        self.setStyle(CustomMenuStyle())

        self.animation.start()
        super().exec_(pos)


class MenuSeparator(QWidget):
    """ Menu separator """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(9)

    def paintEvent(self, e):
        painter = QPainter(self)
        c = 0 if qconfig.theme == 'light' else 255
        pen = QPen(QColor(c, c, c, 104), 1)
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(0, 4, self.width(), 4)


class SubMenuItemWidget(QWidget):
    """ Sub menu item """

    def __init__(self, menu: QMenu, parent=None):
        """
        Parameters
        ----------
        menu: QMenu
            sub menu

        parent: QWidget
            parent widget
        """
        super().__init__(parent)
        self.menu = menu

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

        # draw icon and text
        option = QStyleOptionViewItem()
        option.initFrom(self.parent())
        self.style().drawPrimitive(QStyle.PE_PanelItemViewRow, option, painter)

        # draw right arrow
        s = 9
        renderer = QSvgRenderer(MIF.path(MIF.CHEVRON_RIGHT))
        renderer.render(painter, QRectF(self.width()-10, self.height()/2-s/2, s, s))


class MenuActionListWidget(QListWidget):
    """ Menu action list widget """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setViewportMargins(5, 6, 5, 6)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTextElideMode(Qt.ElideNone)
        self.setIconSize(QSize(14, 14))
        self.smoothScroll = SmoothScroll(self)

    def wheelEvent(self, e):
        self.smoothScroll.wheelEvent(e)

    def adjustSize(self):
        size = QSize()
        for i in range(self.count()):
            s = self.item(i).sizeHint()
            size.setWidth(max(s.width(), size.width()))
            size.setHeight(size.height() + s.height())

        # adjust the height of viewport
        vsize = QSize(size)
        vsize.setHeight(min(588, vsize.height()))
        self.viewport().adjustSize()

        # adjust the height of list widget
        size.setHeight(min(600, size.height()+3))
        m = self.viewportMargins()
        size += QSize(m.left()+m.right()+2, m.top()+m.bottom())
        self.setFixedSize(size)


class RoundMenu(QWidget):
    """ Round corner menu """

    def __init__(self, title="", parent=None):
        super().__init__(parent=parent)
        self._title = title
        self._icon = QIcon()
        self._actions = []
        self.hBoxLayout = QHBoxLayout(self)
        self.view = MenuActionListWidget(self)
        self.__initWidgets()

    def __initWidgets(self):
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint |
                            Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setShadowEffect()
        self.hBoxLayout.addWidget(self.view)
        self.hBoxLayout.setContentsMargins(12, 8, 12, 20)
        self.view.itemClicked.connect(self.__onItemClicked)
        setStyleSheet(self, 'menu')

    def setShadowEffect(self, blurRadius=30, offset=(0, 8), color=QColor(0, 0, 0, 30)):
        """ add shadow to dialog """
        self.shadowEffect = QGraphicsDropShadowEffect(self.view)
        self.shadowEffect.setBlurRadius(blurRadius)
        self.shadowEffect.setOffset(*offset)
        self.shadowEffect.setColor(color)
        self.view.setGraphicsEffect(None)
        self.view.setGraphicsEffect(self.shadowEffect)

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
        self._actions.append(action)
        hasIcon = any(not i.icon().isNull() for i in self._actions)

        # create empty icon
        icon = action.icon()
        if hasIcon and icon.isNull():
            pixmap = QPixmap(self.view.iconSize())
            pixmap.fill(Qt.transparent)
            icon = QIcon(pixmap)

        item = QListWidgetItem(icon, action.text(), self.view)
        if not hasIcon:
            w = 28 + self.view.fontMetrics().width(action.text())
        else:
            # add a blank character to increase space between icon and text
            item.setText(" " + item.text())
            w = 60 + self.view.fontMetrics().width(action.text())

        item.setSizeHint(QSize(w, 33))
        self.view.addItem(item)
        self.view.adjustSize()
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

    def removeAction(self, action):
        """ remove action from menu """
        if action not in self._actions:
            return

        index = self._actions.index(action)
        self._actions.remove(action)
        item = self.view.takeItem(index)
        self.view.adjustSize()

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

    def addMenu(self, menu: QMenu):
        """ add sub menu """
        hasIcon = any(not self.view.item(i).icon().isNull() for i in range(self.view.count()))

        # create empty icon
        icon = menu.icon()
        if hasIcon and icon.isNull():
            pixmap = QPixmap(self.view.iconSize())
            pixmap.fill(Qt.transparent)
            icon = QIcon(pixmap)

        item = QListWidgetItem(icon, menu.title(), self.view)
        if not hasIcon:
            w = 28 + self.view.fontMetrics().width(menu.title())
        else:
            # add a blank character to increase space between icon and text
            item.setText(" " + item.text())
            w = 60 + self.view.fontMetrics().width(menu.title())

        item.setSizeHint(QSize(w, 33))
        self.view.addItem(item)
        self.view.setItemWidget(item, SubMenuItemWidget(menu, self))
        self.view.adjustSize()

    def addSeparator(self):
        """ add seperator to menu """
        m = self.view.viewportMargins()
        w = self.view.width()-m.left()-m.right()

        # create separator
        separator = MenuSeparator(self.view)
        separator.resize(w, separator.height())

        # add separator to list widget
        item = QListWidgetItem(self.view)
        item.setFlags(Qt.NoItemFlags)
        item.setSizeHint(QSize(w, separator.height()))
        self.view.addItem(item)
        self.view.setItemWidget(item, separator)

    def __onItemClicked(self, item):
        index = self.view.row(item)
        if not 0 <= index < len(self._actions):
            return

        self._actions[index].trigger()
        self.deleteLater()

    def menuActions(self):
        return self._actions

    def mousePressEvent(self, e):
        if self.childAt(e.pos()) is not self.view:
            self.deleteLater()

    def exec(self, pos):
        desktop = QApplication.desktop().availableGeometry()
        pos.setX(min(pos.x() - 40, desktop.width() - self.width()))
        pos.setY(min(pos.y() - 12, desktop.height() - self.height()))
        self.move(pos)
        self.show()
