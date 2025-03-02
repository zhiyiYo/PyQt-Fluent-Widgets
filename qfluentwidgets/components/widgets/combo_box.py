# coding:utf-8
import sys
from typing import Union, List, Iterable

from PySide6.QtCore import Qt, Signal, QRectF, QPoint, QObject, QEvent
from PySide6.QtGui import QPainter, QAction, QCursor, QIcon
from PySide6.QtWidgets import QPushButton, QApplication

from .menu import RoundMenu, MenuAnimationType, IndicatorMenuItemDelegate
from .line_edit import LineEdit, LineEditButton
from ...common.animation import TranslateYAnimation
from ...common.icon import FluentIconBase, isDarkTheme
from ...common.icon import FluentIcon as FIF
from ...common.font import setFont
from ...common.style_sheet import FluentStyleSheet


class ComboItem:
    """ Combo box item """

    def __init__(self, text: str, icon: Union[str, QIcon, FluentIconBase] = None, userData=None, isEnabled=True):
        """ add item

        Parameters
        ----------
        text: str
            the text of item

        icon: str | QIcon | FluentIconBase
            the icon of item

        userData: Any
            user data

        isEnabled: bool
            whether to enable the item
        """
        self.text = text
        self.userData = userData
        self.icon = icon
        self.isEnabled = isEnabled

    @property
    def icon(self):
        if isinstance(self._icon, QIcon):
            return self._icon

        return self._icon.icon()

    @icon.setter
    def icon(self, ico: Union[str, QIcon, FluentIconBase]):
        if ico:
            self._icon = QIcon(ico) if isinstance(ico, str) else ico
        else:
            self._icon = QIcon()


class ComboBoxBase:
    """ Combo box base """
    activated = Signal(int)
    textActivated = Signal(str)

    def __init__(self, parent=None, **kwargs):
        pass

    def _setUpUi(self):
        self.isHover = False
        self.isPressed = False
        self.items = []     # type: List[ComboItem]
        self._currentIndex = -1
        self._maxVisibleItems = -1
        self.dropMenu = None
        self._placeholderText = ""

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
        item = ComboItem(text, icon, userData)
        self.items.append(item)
        if len(self.items) == 1:
            self.setCurrentIndex(0)

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

        self.items.pop(index)

        if index < self.currentIndex():
            self.setCurrentIndex(self._currentIndex - 1)
        elif index == self.currentIndex():
            if index > 0:
                self.setCurrentIndex(self._currentIndex - 1)
            else:
                self.setText(self.itemText(0))
                self.currentTextChanged.emit(self.currentText())
                self.currentIndexChanged.emit(0)

        if self.count() == 0:
            self.clear()

    def currentIndex(self):
        return self._currentIndex

    def setCurrentIndex(self, index: int):
        """ set current index

        Parameters
        ----------
        index: int
            current index
        """
        if not 0 <= index < len(self.items) or index == self.currentIndex():
            return

        oldText = self.currentText()

        self._currentIndex = index
        self.setText(self.items[index].text)

        if oldText != self.currentText():
            self.currentTextChanged.emit(self.currentText())

        self.currentIndexChanged.emit(index)

    def setText(self, text: str):
        super().setText(text)
        self.adjustSize()

    def currentText(self):
        if not 0 <= self.currentIndex() < len(self.items):
            return ''

        return self.items[self.currentIndex()].text

    def currentData(self):
        if not 0 <= self.currentIndex() < len(self.items):
            return None

        return self.items[self.currentIndex()].userData

    def setCurrentText(self, text):
        """ set the current text displayed in combo box,
        text should be in the item list

        Parameters
        ----------
        text: str
            text displayed in combo box
        """
        if text == self.currentText():
            return

        index = self.findText(text)
        if index >= 0:
            self.setCurrentIndex(index)

    def setItemText(self, index: int, text: str):
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

        self.items[index].text = text
        if self.currentIndex() == index:
            self.setText(text)

    def itemData(self, index: int):
        """ Returns the data in the given index """
        if not 0 <= index < len(self.items):
            return None

        return self.items[index].userData

    def itemText(self, index: int):
        """ Returns the text in the given index """
        if not 0 <= index < len(self.items):
            return ''

        return self.items[index].text

    def itemIcon(self, index: int):
        """ Returns the icon in the given index """
        if not 0 <= index < len(self.items):
            return QIcon()

        return self.items[index].icon

    def setItemData(self, index: int, value):
        """ Sets the data role for the item on the given index """
        if 0 <= index < len(self.items):
            self.items[index].userData = value

    def setItemIcon(self, index: int, icon: Union[str, QIcon, FluentIconBase]):
        """ Sets the data role for the item on the given index """
        if 0 <= index < len(self.items):
            self.items[index].icon = icon

    def setItemEnabled(self, index: int, isEnabled: bool):
        """ Sets the enabled status of the item on the given index """
        if 0 <= index < len(self.items):
            self.items[index].isEnabled = isEnabled

    def findData(self, data):
        """ Returns the index of the item containing the given data, otherwise returns -1 """
        for i, item in enumerate(self.items):
            if item.userData == data:
                return i

        return -1

    def findText(self, text: str):
        """ Returns the index of the item containing the given text; otherwise returns -1. """
        for i, item in enumerate(self.items):
            if item.text == text:
                return i

        return -1

    def clear(self):
        """ Clears the combobox, removing all items. """
        if self.currentIndex() >= 0:
            self.setText('')

        self.items.clear()
        self._currentIndex = -1

    def count(self):
        """ Returns the number of items in the combobox """
        return len(self.items)

    def insertItem(self, index: int, text: str, icon: Union[str, QIcon, FluentIconBase] = None, userData=None):
        """ Inserts item into the combobox at the given index. """
        item = ComboItem(text, icon, userData)
        self.items.insert(index, item)

        if index <= self.currentIndex():
            self.setCurrentIndex(self.currentIndex() + 1)

    def insertItems(self, index: int, texts: Iterable[str]):
        """ Inserts items into the combobox, starting at the index specified. """
        pos = index
        for text in texts:
            item = ComboItem(text)
            self.items.insert(pos, item)
            pos += 1

        if index <= self.currentIndex():
            self.setCurrentIndex(self.currentIndex() + pos - index)

    def setMaxVisibleItems(self, num: int):
        self._maxVisibleItems = num

    def maxVisibleItems(self):
        return self._maxVisibleItems

    def _closeComboMenu(self):
        if not self.dropMenu:
            return

        # drop menu could be deleted before this method
        try:
            self.dropMenu.close()
        except:
            pass

        self.dropMenu = None

    def _onDropMenuClosed(self):
        if sys.platform != "win32":
            self.dropMenu = None
        else:
            pos = self.mapFromGlobal(QCursor.pos())
            if not self.rect().contains(pos):
                self.dropMenu = None

    def _createComboMenu(self):
        return ComboBoxMenu(self)

    def _showComboMenu(self):
        if not self.items:
            return

        menu = self._createComboMenu()
        for item in self.items:
            action = QAction(item.icon, item.text)
            action.setEnabled(item.isEnabled)
            menu.addAction(action)

        # fixes issue #468
        menu.view.itemClicked.connect(lambda i: self._onItemClicked(self.findText(i.text().lstrip())))

        if menu.view.width() < self.width():
            menu.view.setMinimumWidth(self.width())
            menu.adjustSize()

        menu.setMaxVisibleItems(self.maxVisibleItems())
        menu.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        menu.closedSignal.connect(self._onDropMenuClosed)
        self.dropMenu = menu

        # set the selected item
        if self.currentIndex() >= 0 and self.items:
            menu.setDefaultAction(menu.actions()[self.currentIndex()])

        # determine the animation type by choosing the maximum height of view
        x = -menu.width()//2 + menu.layout().contentsMargins().left() + self.width()//2
        pd = self.mapToGlobal(QPoint(x, self.height()))
        hd = menu.view.heightForAnimation(pd, MenuAnimationType.DROP_DOWN)

        pu = self.mapToGlobal(QPoint(x, 0))
        hu = menu.view.heightForAnimation(pu, MenuAnimationType.PULL_UP)

        if hd >= hu:
            menu.view.adjustSize(pd, MenuAnimationType.DROP_DOWN)
            menu.exec(pd, aniType=MenuAnimationType.DROP_DOWN)
        else:
            menu.view.adjustSize(pu, MenuAnimationType.PULL_UP)
            menu.exec(pu, aniType=MenuAnimationType.PULL_UP)

    def _toggleComboMenu(self):
        if self.dropMenu:
            self._closeComboMenu()
        else:
            self._showComboMenu()

    def _onItemClicked(self, index):
        if not self.items[index].isEnabled:
            return

        if index != self.currentIndex():
            self.setCurrentIndex(index)

        self.activated.emit(index)
        self.textActivated.emit(self.currentText())


class ComboBox(QPushButton, ComboBoxBase):
    """ Combo box """

    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)
    activated = Signal(int)
    textActivated = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.arrowAni = TranslateYAnimation(self)
        self._setUpUi()
        setFont(self)

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
        self._placeholderText = text

        if self.currentIndex() <= 0:
            self._updateTextState(True)
            self.setText(text)

    def setCurrentIndex(self, index: int):
        if index < 0:
            self._currentIndex = -1
            self.setPlaceholderText(self._placeholderText)
        elif 0 <= index < len(self.items):
            self._updateTextState(False)
            super().setCurrentIndex(index)

    def _updateTextState(self, isPlaceholder):
        if self.property("isPlaceholderText") == isPlaceholder:
            return

        self.setProperty("isPlaceholderText", isPlaceholder)
        self.setStyle(QApplication.style())

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

        rect = QRectF(self.width()-22, self.height()/2-5+self.arrowAni.y, 10, 10)
        if isDarkTheme():
            FIF.ARROW_DOWN.render(painter, rect)
        else:
            FIF.ARROW_DOWN.render(painter, rect, fill="#646464")


class EditableComboBox(LineEdit, ComboBoxBase):
    """ Editable combo box """

    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)
    activated = Signal(int)
    textActivated = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._setUpUi()

        self.dropButton = LineEditButton(FIF.ARROW_DOWN, self)

        self.setTextMargins(0, 0, 29, 0)
        self.dropButton.setFixedSize(30, 25)
        self.hBoxLayout.addWidget(self.dropButton, 0, Qt.AlignRight)

        self.dropButton.clicked.connect(self._toggleComboMenu)
        self.textChanged.connect(self._onComboTextChanged)
        self.returnPressed.connect(self._onReturnPressed)

        FluentStyleSheet.LINE_EDIT.apply(self)

        self.clearButton.clicked.disconnect()
        self.clearButton.clicked.connect(self._onClearButtonClicked)

    def setCompleterMenu(self, menu):
        super().setCompleterMenu(menu)
        menu.activated.connect(self.__onActivated)

    def __onActivated(self, text):
        index = self.findText(text)
        if index >= 0:
            self.setCurrentIndex(index)

    def currentText(self):
        return self.text()

    def setCurrentIndex(self, index: int):
        if index >= self.count() or index == self.currentIndex():
            return

        if index < 0:
            self._currentIndex = -1
            self.setText("")
            self.setPlaceholderText(self._placeholderText)
        else:
            self._currentIndex = index
            self.setText(self.items[index].text)

    def clear(self):
        ComboBoxBase.clear(self)

    def setPlaceholderText(self, text: str):
        self._placeholderText = text
        super().setPlaceholderText(text)

    def _onReturnPressed(self):
        if not self.text():
            return

        index = self.findText(self.text())
        if index >= 0 and index != self.currentIndex():
            self._currentIndex = index
            self.currentIndexChanged.emit(index)
        elif index == -1:
            self.addItem(self.text())
            self.setCurrentIndex(self.count() - 1)

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

    def _onComboTextChanged(self, text: str):
        self._currentIndex = -1
        self.currentTextChanged.emit(text)

        for i, item in enumerate(self.items):
            if item.text == text:
                self._currentIndex = i
                self.currentIndexChanged.emit(i)
                return

    def _onDropMenuClosed(self):
        self.dropMenu = None

    def _onClearButtonClicked(self):
        LineEdit.clear(self)
        self._currentIndex = -1


class ComboBoxMenu(RoundMenu):
    """ Combo box menu """

    def __init__(self, parent=None):
        super().__init__(title="", parent=parent)

        self.view.setViewportMargins(0, 2, 0, 6)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.view.setItemDelegate(IndicatorMenuItemDelegate())
        self.view.setObjectName('comboListWidget')

        self.setItemHeight(33)

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        self.view.adjustSize(pos, aniType)
        self.adjustSize()
        return super().exec(pos, ani, aniType)