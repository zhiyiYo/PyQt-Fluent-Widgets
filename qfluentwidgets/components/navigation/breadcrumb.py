# coding:utf-8
import math

from typing import Dict, List
from PyQt5.QtCore import Qt, pyqtSignal, QRectF, pyqtProperty, QPoint, QEvent
from PyQt5.QtGui import QPainter, QFont, QHoverEvent
from PyQt5.QtWidgets import QWidget, QAction, QApplication

from ...common.font import setFont
from ...common.icon import FluentIcon
from ...common.style_sheet import isDarkTheme
from ...components.widgets.menu import RoundMenu, MenuAnimationType


class BreadcrumbWidget(QWidget):
    """ Bread crumb widget """

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.isHover = False
        self.isPressed = False

    def mousePressEvent(self, e):
        self.isPressed = True
        self.update()

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        self.update()
        self.clicked.emit()

    def enterEvent(self, e):
        self.isHover = True
        self.update()

    def leaveEvent(self, e):
        self.isHover = False
        self.update()


class ElideButton(BreadcrumbWidget):
    """ Elide button """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(16, 16)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        if self.isPressed:
            painter.setOpacity(0.5)
        elif not self.isHover:
            painter.setOpacity(0.61)

        FluentIcon.MORE.render(painter, self.rect())

    def clearState(self):
        self.setAttribute(Qt.WA_UnderMouse, False)
        self.isHover = False
        e = QHoverEvent(QEvent.HoverLeave, QPoint(-1, -1), QPoint())
        QApplication.sendEvent(self, e)


class BreadcrumbItem(BreadcrumbWidget):
    """ Breadcrumb item """

    separatorMenuClicked = pyqtSignal()
    menuClicked = pyqtSignal()

    # interactive zones of item
    NoneZone = 0
    SeparatorZone = 1
    TextZone = 2
    MenuZone = 3

    def __init__(self, routeKey: str, text: str, index: int, parent=None):
        super().__init__(parent=parent)
        self.text = text
        self.routeKey = routeKey
        self.isHover = False
        self.isPressed = False
        self.isSelected = False
        self.index = index
        self.spacing = 5
        self.menuActions = []       # type: List[QAction]
        self.isMenuVisible = False
        self.hasSeparatorMenu = False
        self._hoveredZone = BreadcrumbItem.NoneZone
        self._pressedZone = BreadcrumbItem.NoneZone
        self.setMouseTracking(True)

    def setText(self, text: str):
        self.text = text

        rect = self.fontMetrics().boundingRect(text)
        w = rect.width() + math.ceil(self.font().pixelSize() / 10)
        if not self.isRoot():
            w += self.spacing * 2
        if self.isMenuVisible:
            w += self.menuWidth()

        self.setFixedWidth(w)
        self.setFixedHeight(rect.height())
        self.update()

    def menuWidth(self):
        return self.spacing * 2 if self.isMenuVisible else 0

    def setMenuActions(self, actions):
        """ set the actions of item drop-down menu """
        self.menuActions = list(actions or [])
        if not self.menuActions:
            self.isMenuVisible = False

        self.setText(self.text)

    def setMenuVisible(self, isVisible: bool):
        isVisible = bool(isVisible and self.menuActions)
        if isVisible == self.isMenuVisible:
            return

        self.isMenuVisible = isVisible
        self.setText(self.text)

    def zoneAt(self, pos: QPoint):
        """ return the interactive zone at position """
        if not self.rect().contains(pos):
            return self.NoneZone

        if not self.isRoot() and self.hasSeparatorMenu and pos.x() < self.spacing * 2:
            return self.SeparatorZone

        if self.isMenuVisible and pos.x() >= self.width() - self.menuWidth():
            return self.MenuZone

        return self.TextZone

    def mousePressEvent(self, e):
        self.isPressed = True
        self._pressedZone = self.zoneAt(e.pos())
        self.update()

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        pressedZone = self._pressedZone
        self._pressedZone = self.NoneZone
        self.update()

        if pressedZone == self.NoneZone or pressedZone != self.zoneAt(e.pos()):
            return

        if pressedZone == self.SeparatorZone:
            self.separatorMenuClicked.emit()
        elif pressedZone == self.MenuZone:
            self.menuClicked.emit()
        else:
            self.clicked.emit()

    def mouseMoveEvent(self, e):
        zone = self.zoneAt(e.pos())
        if zone != self._hoveredZone:
            self._hoveredZone = zone
            self.update()

    def leaveEvent(self, e):
        self.isHover = False
        self._hoveredZone = self.NoneZone
        self._pressedZone = self.NoneZone
        self.update()

    def isRoot(self):
        return self.index == 0

    def setSelected(self, isSelected: bool):
        self.isSelected = isSelected
        self.update()

    def setFont(self, font: QFont):
        super().setFont(font)
        self.setText(self.text)

    def setSpacing(self, spacing: int):
        self.spacing = spacing
        self.setText(self.text)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.TextAntialiasing | QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        # draw seperator
        sw = self.spacing * 2
        if not self.isRoot():
            iw = self.font().pixelSize() / 14 * 8
            rect = QRectF((sw - iw) / 2, (self.height() - iw) / 2 + 1, iw, iw)

            if self._pressedZone == self.SeparatorZone:
                painter.setOpacity(1)
            elif self._hoveredZone == self.SeparatorZone and self.hasSeparatorMenu:
                painter.setOpacity(0.85)
            else:
                painter.setOpacity(0.61)
            FluentIcon.CHEVRON_RIGHT_MED.render(painter, rect)

        # draw menu indicator
        mw = self.menuWidth()
        if mw > 0:
            iw = self.font().pixelSize() / 14 * 8
            rect = QRectF(self.width() - mw + (mw - iw) / 2,
                          (self.height() - iw) / 2 + 1, iw, iw)

            if self._pressedZone == self.MenuZone:
                painter.setOpacity(1)
            elif self._hoveredZone == self.MenuZone:
                painter.setOpacity(0.85)
            else:
                painter.setOpacity(0.61)
            FluentIcon.CHEVRON_DOWN_MED.render(painter, rect)

        # draw text
        if self._pressedZone == self.TextZone:
            alpha = 0.54 if isDarkTheme() else 0.45
            painter.setOpacity(1 if self.isSelected else alpha)
        elif self.isSelected or self._hoveredZone == self.TextZone:
            painter.setOpacity(1)
        else:
            painter.setOpacity(0.79 if isDarkTheme() else 0.61)

        painter.setFont(self.font())
        painter.setPen(Qt.white if isDarkTheme() else Qt.black)

        if self.isRoot():
            rect = QRectF(0, 0, self.width() - mw, self.height())
        else:
            rect = QRectF(sw, 0, self.width() - sw - mw, self.height())

        painter.drawText(rect, Qt.AlignVCenter | Qt.AlignLeft, self.text)



class BreadcrumbBar(QWidget):
    """ Breadcrumb bar """

    currentItemChanged = pyqtSignal(str)
    currentIndexChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.itemMap = {}       # type: Dict[BreadcrumbItem]
        self.items = []         # type: List[BreadcrumbItem]
        self.hiddenItems = []   # type: List[BreadcrumbItem]

        self._spacing = 10
        self._currentIndex = -1

        self.elideButton = ElideButton(self)

        setFont(self, 14)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.elideButton.hide()
        self.elideButton.clicked.connect(self._showHiddenItemsMenu)

    def addItem(self, routeKey: str, text: str, menu: List[QAction] = None):
        """ add item

        Parameters
        ----------
        routeKey: str
            unique key of item

        text: str
            the text of item

        menu: List[QAction]
            the actions of drop-down menu of item
        """
        if routeKey in self.itemMap:
            return

        item = BreadcrumbItem(routeKey, text, len(self.items), self)
        item.setFont(self.font())
        item.setSpacing(self.spacing)
        item.setMenuActions(menu)
        item.clicked.connect(lambda: self.setCurrentItem(routeKey))
        item.separatorMenuClicked.connect(lambda i=item: self._showSeparatorMenu(i))
        item.menuClicked.connect(lambda i=item: self._showItemMenu(i))

        self.itemMap[routeKey] = item
        self.items.append(item)
        self.setFixedHeight(max(i.height() for i in self.items))
        self.setCurrentItem(routeKey)

        self.updateGeometry()

    def setCurrentIndex(self, index: int):
        if not 0 <= index < len(self.items) or index == self.currentIndex():
            return

        if 0<= self.currentIndex() < len(self.items):
            self.currentItem().setSelected(False)

        self._currentIndex = index
        self.currentItem().setSelected(True)

        # remove trailing items
        for item in self.items[-1:index:-1]:
            item = self.items.pop()
            self.itemMap.pop(item.routeKey)
            item.deleteLater()

        self._updateItemMenuState()
        self.updateGeometry()

        self.currentIndexChanged.emit(index)
        self.currentItemChanged.emit(self.currentItem().routeKey)

    def setCurrentItem(self, routeKey: str):
        if routeKey not in self.itemMap:
            return

        self.setCurrentIndex(self.items.index(self.itemMap[routeKey]))

    def setItemText(self, routeKey: str, text: str):
        item = self.item(routeKey)
        if item:
            item.setText(text)
            self.updateGeometry()

    def item(self, routeKey: str) -> BreadcrumbItem:
        return self.itemMap.get(routeKey, None)

    def itemAt(self, index: int):
        if 0 <= index < len(self.items):
            return self.items[index]

        return None

    def currentIndex(self):
        return self._currentIndex

    def currentItem(self) -> BreadcrumbItem:
        if self.currentIndex() >= 0:
            return self.items[self.currentIndex()]

        return None

    def resizeEvent(self, e):
        self.updateGeometry()

    def clear(self):
        """ clear all items """
        while self.items:
            item = self.items.pop()
            self.itemMap.pop(item.routeKey)
            item.deleteLater()

        self.elideButton.hide()
        self._currentIndex = -1

    def popItem(self):
        """ pop trailing item """
        if not self.items:
            return

        if self.count() >= 2:
            self.setCurrentIndex(self.currentIndex() - 1)
        else:
            self.clear()

    def count(self):
        """ Returns the number of items """
        return len(self.items)

    def updateGeometry(self):
        if not self.items:
            return

        x = 0
        self.elideButton.hide()
        self.hiddenItems = self.items[:-1].copy()

        if not self.isElideVisible():
            visibleItems = self.items
            self.hiddenItems.clear()
        else:
            visibleItems = [self.elideButton, self.items[-1]]
            w = sum(i.width() for i in visibleItems)

            for item in self.items[-2::-1]:
                w += item.width()
                if w > self.width():
                    break

                visibleItems.insert(1, item)
                self.hiddenItems.remove(item)

        for item in self.hiddenItems:
            item.hide()

        for item in visibleItems:
            item.move(x, (self.height() - item.height()) // 2)
            item.show()
            x += item.width()

    def isElideVisible(self):
        w = sum(i.width() for i in self.items)
        return w > self.width()

    def setFont(self, font: QFont):
        super().setFont(font)

        s = int(font.pixelSize() / 14 * 16)
        self.elideButton.setFixedSize(s, s)

        for item in self.items:
            item.setFont(font)

        self.updateGeometry()

    def _showHiddenItemsMenu(self):
        self.elideButton.clearState()

        menu = RoundMenu(parent=self)
        menu.setItemHeight(32)

        for item in self.hiddenItems:
            menu.addAction(
                QAction(item.text, menu, triggered=lambda c, i=item: self.setCurrentItem(i.routeKey)))

        self._execMenu(menu, self, -menu.layout().contentsMargins().left())

    def _showSeparatorMenu(self, item: BreadcrumbItem):
        """ show the menu of preceding item beside the seperator """
        if item.index > 0:
            self._showMenu(self.items[item.index - 1].menuActions, item)

    def _showItemMenu(self, item: BreadcrumbItem):
        if not item.isMenuVisible:
            return

        self._showMenu(item.menuActions, item, item.width() - item.menuWidth())

    def _showMenu(self, actions, anchor: QWidget, x=0):
        if not actions:
            return

        menu = RoundMenu(parent=self)
        menu.setItemHeight(32)
        for action in actions:
            menu.addAction(action)

        self._execMenu(menu, anchor, x)

    def _execMenu(self, menu: RoundMenu, anchor: QWidget, x=0):
        # determine the animation type by choosing the maximum height of view
        pd = anchor.mapToGlobal(QPoint(x, anchor.height()))
        hd = menu.view.heightForAnimation(pd, MenuAnimationType.DROP_DOWN)

        pu = anchor.mapToGlobal(QPoint(x, 0))
        hu = menu.view.heightForAnimation(pu, MenuAnimationType.PULL_UP)

        if hd >= hu:
            menu.view.adjustSize(pd, MenuAnimationType.DROP_DOWN)
            menu.exec(pd, aniType=MenuAnimationType.DROP_DOWN)
        else:
            menu.view.adjustSize(pu, MenuAnimationType.PULL_UP)
            menu.exec(pu, aniType=MenuAnimationType.PULL_UP)

    def _updateItemMenuState(self):
        # only the current item shows the trailing menu indicator, and the
        # seperator of an item is clickable if its preceding item has a menu
        for i, item in enumerate(self.items):
            item.hasSeparatorMenu = i > 0 and bool(self.items[i - 1].menuActions)
            item.setMenuVisible(item is self.currentItem() and bool(item.menuActions))

    def getSpacing(self):
        return self._spacing

    def setSpacing(self, spacing: int):
        if spacing == self._spacing:
            return

        self._spacing = spacing
        for item in self.items:
            item.setSpacing(spacing)

        self.updateGeometry()

    spacing = pyqtProperty(int, getSpacing, setSpacing)