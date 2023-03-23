# coding:utf-8
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QRectF, QPoint
from PyQt6.QtGui import QColor, QPainter, QAction
from PyQt6.QtWidgets import QPushButton, QWidget

from .menu import RoundMenu
from ...common.config import isDarkTheme
from ...common.icon import FluentIcon as FIF
from ...common.style_sheet import setStyleSheet, themeColor


class ComboBox(QPushButton):
    """ Combo box """

    currentIndexChanged = pyqtSignal(int)
    currentTextChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__("", parent)
        self.isHover = False
        self.isPressed = False
        self.items = []
        self._currentIndex = -1
        setStyleSheet(self, 'combo_box')

    def addItem(self, text):
        """ add item

        Parameters
        ----------
        text: str
            the text of item
        """
        self.items.append(text)

    def addItems(self, texts):
        """ add items

        Parameters
        ----------
        text: Iterable[str]
            the text of item
        """
        self.items.extend(texts)

    def currentIndex(self):
        return self._currentIndex

    def setCurrentIndex(self, index):
        """ set current index

        Parameters
        ----------
        index: int
            current index
        """
        if not 0 <= index < len(self.items) or self.currentIndex() == index:
            return

        self._currentIndex = index
        self.setText(self.items[index])

    def setText(self, text: str):
        super().setText(text)
        self.adjustSize()

    def currentText(self):
        if not 0 <= self.currentIndex() < len(self.items):
            return ''

        return self.items[self.currentIndex()]

    def setCurrentText(self, text):
        """ set the current text displayed in combo box,
        text should be in the item list

        Parameters
        ----------
        text: str
            text displayed in combo box
        """
        if text not in self.items or text == self.currentText():
            return

        self.setCurrentIndex(self.items.index(text))

    def setItemText(self, index, text):
        """ set the text of item

        Parameters
        ----------
        index: int
            the index of item

        text: str
            new text of item
        """
        if not 0 <= index < len(self.items):
            return

        self.items[index] = text
        if self.currentIndex() == index:
            self.setText(text)

    def enterEvent(self, e):
        self.isHover = True
        self.update()

    def leaveEvent(self, e):
        self.isHover = False
        self.update()

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.isPressed = True
        self.update()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.isPressed = False
        self.update()
        self._showComboMenu()

    def _showComboMenu(self):
        if not self.items:
            return

        menu = ComboBoxMenu(self)
        for i, item in enumerate(self.items):
            menu.addAction(
                QAction(item, triggered=lambda c, x=i: self._onItemClicked(x)))

        menu.view.setMinimumWidth(self.width())
        menu.adjustSize()

        # set the selected item
        menu.setDefaultAction(menu.menuActions()[self.currentIndex()])

        # show menu
        x = -menu.width()//2 + menu.layout().contentsMargins().left() + self.width()//2
        y = self.height()
        menu.exec(self.mapToGlobal(QPoint(x, y)))

    def _onItemClicked(self, index):
        if index == self.currentIndex():
            return

        self.setCurrentIndex(index)
        self.currentIndexChanged.emit(index)
        self.currentTextChanged.emit(self.items[index])

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        if self.isHover:
            painter.setOpacity(0.8)
        elif self.isPressed:
            painter.setOpacity(0.7)

        FIF.ARROW_DOWN.render(painter, QRectF(
            self.width()-22, self.height()/2-6, 10, 10))


class ComboBoxMenuItemWidget(QWidget):
    """ Combo box menu item widget """

    def __init__(self, item, parent=None):
        super().__init__(parent)
        self.isPressed = False
        self.item = item
        self.text = item.text()
        item.setText('')

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.isPressed = True
        self.update()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.isPressed = False
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform |
            QPainter.RenderHint.TextAntialiasing
        )

        if self.isPressed:
            painter.setOpacity(0.7)

        # draw text
        isLight = not isDarkTheme()
        painter.setPen(Qt.GlobalColor.black if isLight else Qt.GlobalColor.white)
        painter.setFont(self.item.font())
        painter.drawText(QRect(12, 0, self.width()-10,
                         self.height()), Qt.AlignmentFlag.AlignVCenter, self.text)

        # draw indicator
        if not self.item.isSelected():
            return

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(themeColor())
        painter.drawRoundedRect(0, 8, 3, 16, 1.5, 1.5)


class ComboBoxMenu(RoundMenu):
    """ Combo box menu """

    def __init__(self, parent=None):
        super().__init__(title="", parent=parent)
        setStyleSheet(self, 'combo_box')
        self.setItemHeight(33)

    def addAction(self, action):
        super().addAction(action)
        item = self.view.item(self.view.count()-1)
        w = ComboBoxMenuItemWidget(item, self)
        w.resize(item.sizeHint())
        self.view.setItemWidget(item, w)
