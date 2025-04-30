# coding:utf-8
from typing import Dict

from PyQt5.QtCore import Qt, pyqtSignal, QRectF
from PyQt5.QtGui import QPainter, QFont, QColor
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QHBoxLayout, QSizePolicy

from ...common.font import setFont
from ...common.router import qrouter
from ...common.style_sheet import themeColor, FluentStyleSheet
from ...common.color import autoFallbackThemeColor
from ...common.animation import FluentAnimation, FluentAnimationType, FluentAnimationProperty
from ..widgets.button import PushButton
from .navigation_panel import RouteKeyError


class PivotItem(PushButton):
    """ Pivot item """

    itemClicked = pyqtSignal(bool)

    def _postInit(self):
        self.isSelected = False
        self.setProperty('isSelected', False)
        self.clicked.connect(lambda: self.itemClicked.emit(True))
        self.setAttribute(Qt.WA_LayoutUsesWidgetRect)

        FluentStyleSheet.PIVOT.apply(self)
        setFont(self, 18)

    def setSelected(self, isSelected: bool):
        if self.isSelected == isSelected:
            return

        self.isSelected = isSelected
        self.setProperty('isSelected', isSelected)
        self.setStyle(QApplication.style())
        self.update()


class Pivot(QWidget):
    """ Pivot """

    currentItemChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.items = {}  # type: Dict[str, PivotItem]
        self._currentRouteKey = None

        self.lightIndicatorColor = QColor()
        self.darkIndicatorColor = QColor()

        self.hBoxLayout = QHBoxLayout(self)
        self.slideAni = FluentAnimation.create(
            FluentAnimationType.POINT_TO_POINT, FluentAnimationProperty.SCALE, value=0, parent=self)

        FluentStyleSheet.PIVOT.apply(self)

        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setAlignment(Qt.AlignLeft)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)

    def addItem(self, routeKey: str, text: str, onClick=None, icon=None):
        """ add item

        Parameters
        ----------
        routeKey: str
            the unique name of item

        text: str
            the text of navigation item

        onClick: callable
            the slot connected to item clicked signal

        icon: str
            the icon of navigation item
        """
        return self.insertItem(-1, routeKey, text, onClick, icon)

    def addWidget(self, routeKey: str, widget: PivotItem, onClick=None):
        """ add widget

        Parameters
        ----------
        routeKey: str
            the unique name of item

        widget: PivotItem
            navigation widget

        onClick: callable
            the slot connected to item clicked signal
        """
        self.insertWidget(-1, routeKey, widget, onClick)

    def insertItem(self, index: int, routeKey: str, text: str, onClick=None, icon=None):
        """ insert item

        Parameters
        ----------
        index: int
            insert position

        routeKey: str
            the unique name of item

        text: str
            the text of navigation item

        onClick: callable
            the slot connected to item clicked signal

        icon: str
            the icon of navigation item
        """
        if routeKey in self.items:
            return

        item = PivotItem(text, self)
        if icon:
            item.setIcon(icon)

        self.insertWidget(index, routeKey, item, onClick)
        return item

    def insertWidget(self, index: int, routeKey: str, widget: PivotItem, onClick=None):
        """ insert item

        Parameters
        ----------
        index: int
            insert position

        routeKey: str
            the unique name of item

        widget: PivotItem
            navigation widget

        onClick: callable
            the slot connected to item clicked signal
        """
        if routeKey in self.items:
            return

        widget.setProperty('routeKey', routeKey)
        widget.itemClicked.connect(self._onItemClicked)
        if onClick:
            widget.itemClicked.connect(onClick)

        self.items[routeKey] = widget
        self.hBoxLayout.insertWidget(index, widget, 1)

    def removeWidget(self, routeKey: str):
        """ remove widget

        Parameters
        ----------
        routeKey: str
            the unique name of item
        """
        if routeKey not in self.items:
            return

        item = self.items.pop(routeKey)
        self.hBoxLayout.removeWidget(item)
        qrouter.remove(routeKey)
        item.deleteLater()

        if not self.items:
            self._currentRouteKey = None

    def clear(self):
        """ clear all navigation items """
        for k, w in self.items.items():
            self.hBoxLayout.removeWidget(w)
            qrouter.remove(k)
            w.deleteLater()

        self.items.clear()
        self._currentRouteKey = None

    def currentItem(self):
        """ Returns the current selected item """
        if self._currentRouteKey is None:
            return None

        return self.widget(self._currentRouteKey)

    def currentRouteKey(self):
        return self._currentRouteKey

    def setCurrentItem(self, routeKey: str):
        """ set current selected item

        Parameters
        ----------
        routeKey: str
            the unique name of item
        """
        if routeKey not in self.items or routeKey == self.currentRouteKey():
            return

        self._currentRouteKey = routeKey
        self.slideAni.startAnimation(self.widget(routeKey).x())

        for k, item in self.items.items():
            item.setSelected(k == routeKey)

        self.currentItemChanged.emit(routeKey)

    def showEvent(self, e):
        super().showEvent(e)
        self._adjustIndicatorPos()

    def setItemFontSize(self, size: int):
        """ set the pixel font size of items """
        for item in self.items.values():
            font = item.font()
            font.setPixelSize(size)
            item.setFont(font)
            item.adjustSize()

    def setItemText(self, routeKey: str, text: str):
        """ set the text of item """
        item = self.widget(routeKey)
        item.setText(text)

    def setIndicatorColor(self, light, dark):
        self.lightIndicatorColor = QColor(light)
        self.darkIndicatorColor = QColor(dark)
        self.update()

    def _onItemClicked(self):
        item = self.sender()  # type: PivotItem
        self.setCurrentItem(item.property('routeKey'))

    def widget(self, routeKey: str):
        if routeKey not in self.items:
            raise RouteKeyError(f"`{routeKey}` is illegal.")

        return self.items[routeKey]

    def resizeEvent(self, e) -> None:
        super().resizeEvent(e)
        self._adjustIndicatorPos()

    def _adjustIndicatorPos(self):
        item = self.currentItem()
        if item:
            self.slideAni.stop()
            self.slideAni.setValue(item.x())

    def paintEvent(self, e):
        super().paintEvent(e)

        if not self.currentItem():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(autoFallbackThemeColor(self.lightIndicatorColor, self.darkIndicatorColor))

        x = int(self.currentItem().width() / 2 - 8 + self.slideAni.value())
        painter.drawRoundedRect(x, self.height() - 3, 16, 3, 1.5, 1.5)