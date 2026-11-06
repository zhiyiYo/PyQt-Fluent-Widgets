# coding:utf-8
from typing import List
from PyQt5.QtCore import Qt, QRect, QRectF, QSize, QPoint
from PyQt5.QtGui import QPainter, QColor, QPainterPath
from PyQt5.QtWidgets import QLineEdit, QListWidgetItem, QListWidget

from ..widgets.menu  import (RoundMenu, MenuActionListWidget, LineEditMenu, MenuIndicatorType, CheckableMenu)
from ..widgets.line_edit import CompleterMenu, LineEdit
from ..widgets.acrylic_label import AcrylicBrush
from ...common.style_sheet import isDarkTheme


class AcrylicMenuActionListWidget(MenuActionListWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.acrylicBrush = AcrylicBrush(self.viewport(), 35)
        self.setViewportMargins(0, 0, 0, 0)
        self.setProperty("transparent", True)

        super().addItem(self.createPlaceholderItem(self._topMargin()))
        super().addItem(self.createPlaceholderItem(self._bottomMargin()))

    def _updateAcrylicColor(self):
        if isDarkTheme():
            tintColor = QColor(32, 32, 32, 200)
            luminosityColor = QColor(0, 0, 0, 0)
        else:
            tintColor = QColor(255, 255, 255, 160)
            luminosityColor = QColor(255, 255, 255, 50)

        self.acrylicBrush.tintColor = tintColor
        self.acrylicBrush.luminosityColor = luminosityColor

    def _topMargin(self):
        return 2

    def _bottomMargin(self):
        return 2

    def setItemHeight(self, height: int):
        """ set the height of item """
        if height == self._itemHeight:
            return

        for i in range(1, self.count() - 1):
            item = self.item(i)
            if not self.itemWidget(item):
                item.setSizeHint(QSize(item.sizeHint().width(), height))

        self._itemHeight = height
        self.adjustSize()

    def addItem(self, item):
        return super().insertItem(self.count() - 1, item)

    def createPlaceholderItem(self, height=2):
        item = QListWidgetItem()
        item.setSizeHint(QSize(1, height))
        item.setFlags(Qt.ItemFlag.NoItemFlags)
        return item

    def clipPath(self):
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect()).adjusted(0, 0, -2.5, -2.5), 7, 7)
        return path

    def paintEvent(self, e) -> None:
        painter = QPainter(self.viewport())
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)

        self.acrylicBrush.clipPath = self.clipPath()
        self._updateAcrylicColor()
        self.acrylicBrush.paint()

        super().paintEvent(e)


class AcrylicMenuBase:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def setUpMenu(self, view):
        assert isinstance(self, RoundMenu)
        delegate = self.view.itemDelegate()
        if delegate is not None:
            delegate.setParent(view)
            view.setItemDelegate(delegate)
        view.setObjectName(self.view.objectName())
        self.hBoxLayout.removeWidget(self.view)
        self.view.deleteLater()

        self.view = view
        self.view.setItemHeight(self.itemHeight)
        self.hBoxLayout.addWidget(self.view)

        self.setShadowEffect()

        self.view.itemClicked.connect(self._onItemClicked)
        self.view.itemEntered.connect(self._onItemEntered)

    def _prepareMenu(self):
        viewport = self.view.viewport()
        self.view.acrylicBrush.grabImage(QRect(viewport.mapToGlobal(QPoint()), viewport.size()))


class AcrylicMenu(AcrylicMenuBase, RoundMenu):
    """ Acrylic menu """

    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.setUpMenu(AcrylicMenuActionListWidget(self))


class AcrylicCompleterMenuActionListWidget(AcrylicMenuActionListWidget):

    def clipPath(self):
        path = QPainterPath()
        path.setFillRule(Qt.FillRule.WindingFill)
        path.addRoundedRect(QRectF(self.rect()).adjusted(1, 1, -2.5, -2.5), 7, 7)

        if self.property("dropDown"):
            path.addRect(1, 1, 11, 11)
            path.addRect(self.width() - 12, 1, 11, 11)
        else:
            path.addRect(1, self.height() - 11, 11, 11)
            path.addRect(self.width() - 12, self.height() - 11, 11, 11)

        return path


class AcrylicCompleterMenu(AcrylicMenuBase, CompleterMenu):
    """ Acrylic completer menu """

    def __init__(self, lineEdit: LineEdit):
        super().__init__(lineEdit)
        self.setUpMenu(AcrylicCompleterMenuActionListWidget(self))

    def _onItemClicked(self, item):
        self._hideMenu(False)
        self._onCompletionItemSelected(item.text(), self.view.row(item)-1)

    def setItems(self, items: List[str]):
        """ set completion items """
        self.view.clear()

        self.items = items
        QListWidget.addItem(self.view, self.view.createPlaceholderItem(self.view._topMargin()))
        self.view.addItems(items)

        for i in range(1, self.view.count()):
            item = self.view.item(i)
            item.setSizeHint(QSize(1, self.itemHeight))

        QListWidget.addItem(self.view, self.view.createPlaceholderItem(self.view._bottomMargin()))


class AcrylicLineEditMenu(AcrylicMenuBase, LineEditMenu):
    """ Acrylic line edit menu """

    def __init__(self, parent: QLineEdit):
        super().__init__(parent)
        self.setUpMenu(AcrylicMenuActionListWidget(self))



class AcrylicCheckableMenu(AcrylicMenuBase, CheckableMenu):
    """ Checkable menu """

    def __init__(self, title="", parent=None, indicatorType=MenuIndicatorType.CHECK):
        super().__init__(title, parent, indicatorType)
        self.setUpMenu(AcrylicMenuActionListWidget(self))


class AcrylicSystemTrayMenu(AcrylicMenu):
    """ Acrylic system tray menu """


class AcrylicCheckableSystemTrayMenu(AcrylicCheckableMenu):
    """ Acrylic checkable system tray menu """
