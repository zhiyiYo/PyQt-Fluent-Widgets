# coding:utf-8
from typing import Dict, Union, List, Iterable

from PySide6.QtCore import Qt, Signal, QRect, QRectF, QPoint, QObject, QEvent
from PySide6.QtGui import QColor, QPainter, QAction, QCursor, QIcon
from PySide6.QtWidgets import QPushButton, QWidget, QStyledItemDelegate, QStyle

from .menu import RoundMenu
from .line_edit import LineEdit, LineEditButton
from ...common.icon import FluentIconBase, isDarkTheme
from ...common.icon import FluentIcon as FIF
from ...common.style_sheet import FluentStyleSheet, themeColor


class ComboItem:
    """ Combo box item """

    def __init__(self, text: str, icon: Union[str, QIcon, FluentIconBase] = None, userData=None):
        """ add item

        Parameters
        ----------
        text: str
            the text of item

        icon: str | QIcon | FluentIconBase
            the icon of item

        userData: Any
            user data
        """
        self.text = text
        self.userData = userData
        if icon:
            self._icon = QIcon(icon) if isinstance(icon, str) else icon
        else:
            self._icon = QIcon()

    @property
    def icon(self):
        if isinstance(self._icon, QIcon):
            return self._icon

        return self._icon.icon()


class ComboBoxBase:
    """ Combo box base """

    def __init__(self, parent=None, **kwargs):
        pass

    def _setUpUi(self):
        self.isHover = False
        self.isPressed = False
        self.items = []     # type: List[ComboItem]
        self.itemMap = {}   # type: Dict[str, ComboItem]
        self._currentIndex = -1
        self.dropMenu = None

        FluentStyleSheet.COMBO_BOX.apply(self)
        self.installEventFilter(self)

    def addItem(self, text, icon: Union[str, QIcon, FluentIconBase] = None, userData=None):
        """ add item

        Parameters
        ----------
        text: str
            the text of item

        icon: str | QIcon | FluentIconBase
        """
        if not text or text in self.itemMap:
            return

        item = ComboItem(text, icon, userData)
        self.itemMap[text] = item
        self.items.append(item)

    def addItems(self, texts: Iterable[str]):
        """ add items

        Parameters
        ----------
        text: Iterable[str]
            the text of item
        """
        for text in texts:
            self.addItem(text)

    def removeItem(self, index: int):
        """ Removes the item at the given index from the combobox.
        This will update the current index if the index is removed.
        """
        if not 0 <= index < len(self.items):
            return

        item = self.items[index]
        self.items.pop(index)
        self.itemMap.pop(item.text)

        if index < self.currentIndex():
            self._onItemClicked(self._currentIndex - 1)
        elif index == self.currentIndex():
            if index > 0:
                self._onItemClicked(self._currentIndex - 1)
            else:
                self.setCurrentIndex(0)
                self.currentTextChanged.emit(self.currentText())
                self.currentIndexChanged.emit(0)

    def currentIndex(self):
        return self._currentIndex

    def setCurrentIndex(self, index):
        """ set current index

        Parameters
        ----------
        index: int
            current index
        """
        if not 0 <= index < len(self.items):
            return

        self._currentIndex = index
        self.setText(self.items[index].text)

    def setText(self, text: str):
        super().setText(text)
        self.adjustSize()

    def currentText(self):
        if not 0 <= self.currentIndex() < len(self.items):
            return ''

        return self.items[self.currentIndex()].text

    def setCurrentText(self, text):
        """ set the current text displayed in combo box,
        text should be in the item list

        Parameters
        ----------
        text: str
            text displayed in combo box
        """
        if text not in self.itemMap or text == self.currentText():
            return

        self.setCurrentIndex(self.items.index(self.itemMap[text]))

    def setItemText(self, index, text):
        """ set the text of item

        Parameters
        ----------
        index: int
            the index of item

        text: str
            new text of item
        """
        if text in self.itemMap or not 0 <= index < len(self.items):
            return

        item = self.itemMap.pop()
        item.text = text
        self.itemMap[text] = item
        if self.currentIndex() == index:
            self.setText(text)

    def itemData(self, index: int):
        """ Returns the data for the given role in the given index in the combobox """
        if not 0 <= index < len(self.items):
            return None

        return self.items[index].userData

    def setItemData(self, index: int, value):
        """ Sets the data role for the item on the given index in the combobox to the specified value """
        if 0 <= index < len(self.items):
            self.items[index].userData = value

    def findData(self, data):
        """ Returns the index of the item containing the given data, otherwise returns -1 """
        for i, item in enumerate(self.items):
            if item.userData == data:
                return i

        return -1

    def findText(self, text: str):
        """ Returns the index of the item containing the given text; otherwise returns -1. """
        if text not in self.itemMap:
            return -1

        return self.items.index(self.itemMap[text])

    def _closeComboMenu(self):
        if not self.dropMenu:
            return

        self.dropMenu.close()
        self.dropMenu = None

    def _onDropMenuClosed(self):
        pos = self.mapFromGlobal(QCursor.pos())
        if not self.rect().contains(pos):
            self.dropMenu = None

    def _showComboMenu(self):
        if not self.items:
            return

        menu = ComboBoxMenu(self)
        for i, item in enumerate(self.items):
            menu.addAction(
                QAction(item.icon, item.text, triggered=lambda x=i: self._onItemClicked(x)))

        if menu.view.width() < self.width():
            menu.view.setMinimumWidth(self.width())
            menu.adjustSize()

        menu.closedSignal.connect(self._onDropMenuClosed)
        self.dropMenu = menu

        # set the selected item
        if self.currentIndex() >= 0 and self.items:
            menu.setDefaultAction(menu.menuActions()[self.currentIndex()])

        # show menu
        x = -menu.width()//2 + menu.layout().contentsMargins().left() + self.width()//2
        y = self.height()
        menu.exec(self.mapToGlobal(QPoint(x, y)))

    def _toggleComboMenu(self):
        if self.dropMenu:
            self._closeComboMenu()
        else:
            self._showComboMenu()

    def _onItemClicked(self, index):
        if index == self.currentIndex():
            return

        self.setCurrentIndex(index)
        self.currentTextChanged.emit(self.currentText())
        self.currentIndexChanged.emit(index)


class ComboBox(QPushButton, ComboBoxBase):
    """ Combo box """

    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._setUpUi()

    def eventFilter(self, obj, e: QEvent):
        if obj is self:
            if e.type() == QEvent.MouseButtonPress:
                self.isPressed = True
            elif e.type() == QEvent.MouseButtonRelease:
                self.isPressed = False
            elif e.type() == QEvent.Enter:
                self.isHover = True
            elif e.type() == QEvent.Leave:
                self.isHover = False

        return super().eventFilter(obj, e)

    def setPlaceholderText(self, text: str):
        self.setText(text)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self._toggleComboMenu()

    def paintEvent(self, e):
        QPushButton.paintEvent(self, e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        if self.isHover:
            painter.setOpacity(0.8)
        elif self.isPressed:
            painter.setOpacity(0.7)

        rect = QRectF(self.width()-22, self.height()/2-5, 10, 10)
        if isDarkTheme():
            FIF.ARROW_DOWN.render(painter, rect)
        else:
            FIF.ARROW_DOWN.render(painter, rect, fill="#646464")


class EditableComboBox(LineEdit, ComboBoxBase):
    """ Editable combo box """

    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._setUpUi()

        self.dropButton = LineEditButton(FIF.ARROW_DOWN, self)

        self.setTextMargins(0, 0, 29, 0)
        self.dropButton.setFixedSize(30, 25)
        self.hBoxLayout.addWidget(self.dropButton, 0, Qt.AlignRight)

        self.dropButton.clicked.connect(self._toggleComboMenu)
        self.textEdited.connect(self._onTextEdited)
        self.returnPressed.connect(lambda: self.addItem(self.text()))

        FluentStyleSheet.LINE_EDIT.apply(self)

    def eventFilter(self, obj, e: QEvent):
        if obj is self:
            if e.type() == QEvent.MouseButtonPress:
                self.isPressed = True
            elif e.type() == QEvent.MouseButtonRelease:
                self.isPressed = False
            elif e.type() == QEvent.Enter:
                self.isHover = True
            elif e.type() == QEvent.Leave:
                self.isHover = False

        return super().eventFilter(obj, e)

    def _onTextEdited(self, text: str):
        if text not in self.itemMap:
            self._currentIndex = -1
        else:
            self._currentIndex = self.items.index(self.itemMap[text])

        self.currentTextChanged.emit(text)

    def _onDropMenuClosed(self):
        self.dropMenu = None


class ComboMenuItemDelegate(QStyledItemDelegate):
    """ Combo box drop menu item delegate """

    def paint(self, painter: QPainter, option, index):
        super().paint(painter, option, index)
        if not option.state & QStyle.State_Selected:
            return

        painter.save()
        painter.setRenderHints(
            QPainter.Antialiasing | QPainter.SmoothPixmapTransform | QPainter.TextAntialiasing)

        painter.setPen(Qt.NoPen)
        painter.setBrush(themeColor())
        painter.drawRoundedRect(0, 11+option.rect.y(), 3, 15, 1.5, 1.5)

        painter.restore()


class ComboBoxMenu(RoundMenu):
    """ Combo box menu """

    def __init__(self, parent=None):
        super().__init__(title="", parent=parent)

        self.view.setViewportMargins(5, 2, 5, 6)
        self.view.setItemDelegate(ComboMenuItemDelegate())

        FluentStyleSheet.COMBO_BOX.apply(self)
        self.setItemHeight(33)
