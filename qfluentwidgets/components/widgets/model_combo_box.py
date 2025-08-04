# coding:utf-8
import sys
from typing import Union, List, Iterable

from PySide6.QtCore import Qt, Signal, QRectF, QPoint, QObject, QEvent, QModelIndex, QAbstractItemModel
from PySide6.QtGui import QPainter, QCursor, QIcon, QStandardItemModel, QStandardItem, QAction
from PySide6.QtWidgets import QPushButton, QApplication

from .menu import RoundMenu, MenuAnimationType, IndicatorMenuItemDelegate
from .line_edit import LineEdit, LineEditButton
from .combo_box import ComboBoxMenu
from ...common.animation import TranslateYAnimation
from ...common.icon import FluentIconBase, isDarkTheme
from ...common.icon import FluentIcon as FIF
from ...common.font import setFont
from ...common.style_sheet import FluentStyleSheet


class ModelComboBoxBase:
    """ Abstract combo box build in data model """

    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)
    activated = Signal(int)
    textActivated = Signal(str)

    def __init__(self, parent=None, **kwargs):
        pass

    def _setUpUi(self):
        self.isHover = False
        self.isPressed = False
        self._currentIndex = -1
        self._maxVisibleItems = -1
        self.dropMenu = None
        self._placeholderText = ""
        self._model = None  # type: QAbstractItemModel

        self.setModel(QStandardItemModel(self))

        FluentStyleSheet.COMBO_BOX.apply(self)
        self.installEventFilter(self)

    def setModel(self, model: QAbstractItemModel):
        if self._model:
            self._model.disconnect(self)

        self._model = model
        model.rowsInserted.connect(self._onModelRowInserted)
        model.dataChanged.connect(self._onModelDataChanged)
        model.rowsRemoved.connect(self._onRowsRemoved)

    def model(self) -> QAbstractItemModel:
        return self._model

    def _onModelRowInserted(self, parentIndex: QModelIndex, first: int, last: int):
        if first <= self.currentIndex():
            self.setCurrentIndex(self.currentIndex() + last - first + 1)

    def _onRowsRemoved(self, parentIndex: QModelIndex, first: int, last: int):
        if last < self.currentIndex():
            self.setCurrentIndex(self.currentIndex() - (last - first + 1))
        elif first < self.currentIndex() <= last:
            self.setCurrentIndex(max(first - 1, 0))

        if self.count() == 0:
            self.clear()

    def _onModelDataChanged(self, topLeft: QModelIndex, bottomRight: QModelIndex, roles):
        if Qt.ItemDataRole.EditRole in roles:
            for row in range(topLeft.row(), bottomRight.row() + 1):
                self.setItemText(row, self.itemText(row))
        if Qt.ItemDataRole.DecorationRole in roles:
            for row in range(topLeft.row(), bottomRight.row() + 1):
                self.setItemIcon(row, self.itemIcon(row))

    def eventFilter(self, obj, e: QEvent):
        if obj is self:
            if e.type() == QEvent.Type.MouseButtonPress:
                self.isPressed = True
            elif e.type() == QEvent.Type.MouseButtonRelease:
                self.isPressed = False
            elif e.type() == QEvent.Type.Enter:
                self.isHover = True
            elif e.type() == QEvent.Type.Leave:
                self.isHover = False

        return super().eventFilter(obj, e)

    def insertItem(self, index: int, text: str, userData=None, icon: QIcon = None):
        """ Inserts item into the combobox at the given index. """
        values = {}
        values[Qt.ItemDataRole.EditRole] = text

        if icon:
            values[Qt.ItemDataRole.DecorationRole] = icon

        if userData:
            values[Qt.ItemDataRole.UserRole] = userData

        modelIndex = self._insertItemFromValues(index, values)

        if index <= self.currentIndex():
            self.setCurrentIndex(self.currentIndex() + 1)

        return modelIndex

    def insertItems(self, index: int, texts: Iterable[str]):
        """ Inserts items into the combobox, starting at the index specified. """
        self.blockSignals(True)

        row = index
        for text in texts:
            values = {}
            values[Qt.ItemDataRole.EditRole] = text
            self._insertItemFromValues(index, values)
            row += 1

        self.blockSignals(False)

        if index <= self.currentIndex():
            self.setCurrentIndex(self.currentIndex() + row - index)

    def _insertItemFromValues(self, row: int, values: dict) -> QModelIndex:
        ret = QModelIndex()

        self.model().blockSignals(True)

        row = min(max(0, row), self.model().rowCount())
        if isinstance(self.model(), QStandardItemModel):
            item = QStandardItem()
            for role, value in values.items():
                item.setData(value, role)

            self.model().insertRow(row, item)
            ret = item.index()
        elif self.model().insertRows(row, 1):
            ret = self.model().index(row, 0)
            if values:
                self.model().setItemData(ret, values)

        self.model().blockSignals(False)
        return ret

    def addItem(self, text: str, userData=None, icon: QIcon = None):
        """ add item

        Parameters
        ----------
        text: str
            the text of item

        icon: str | QIcon | FluentIconBase
        """
        self.insertItem(self.model().rowCount(), text, icon, userData)
        if self.count() == 1:
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
        if not self._isValidIndex(index):
            return

        self.model().blockSignals(True)
        self.model().removeRow(index)
        self.model().blockSignals(False)

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
        if not self._isValidIndex(index) or index == self.currentIndex():
            return

        oldText = self.currentText()

        self._currentIndex = index
        self.setText(self.itemText(index))

        if oldText != self.currentText():
            self.currentTextChanged.emit(self.currentText())

        self.currentIndexChanged.emit(index)

    def setText(self, text: str):
        super().setText(text)
        self.adjustSize()

    def currentText(self):
        return self.itemText(self.currentIndex())

    def currentData(self):
        return self.itemData(self.currentIndex())

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
        if not self._isValidIndex(index):
            return

        oldText = self.text()
        self.setItemData(index, text, Qt.ItemDataRole.EditRole)
        if self.currentIndex() == index:
            self.setText(text)
            if oldText != text:
                self.currentTextChanged.emit(text)

    def itemData(self, index: int):
        """ Returns the data in the given index """
        return self.model().data(self.model().index(index, 0), Qt.ItemDataRole.UserRole)

    def itemText(self, index: int):
        """ Returns the text in the given index """
        return self.model().data(self.model().index(index, 0), Qt.ItemDataRole.EditRole) or ""

    def itemIcon(self, index: int):
        """ Returns the icon in the given index """
        return self.model().data(self.model().index(index, 0), Qt.ItemDataRole.DecorationRole) or QIcon()

    def setItemData(self, index: int, value, role=Qt.ItemDataRole.UserRole):
        if self._isValidIndex(index):
            self.model().setData(self.model().index(index, 0), value, role)

    def setItemIcon(self, index: int, icon: Union[str, QIcon, FluentIconBase]):
        """ Sets the data role for the item on the given index """
        self.setItemData(index, icon, Qt.ItemDataRole.DecorationRole)

    def _isValidIndex(self, index: int):
        return 0 <= index < self.count()

    def findData(self, data, role=Qt.ItemDataRole.UserRole, flags=Qt.MatchFlag.MatchExactly) -> int:
        """ Returns the index of the item containing the given data for the given role; otherwise returns -1. """
        mi = self.model().index(0, 0)
        result = self.model().match(mi, role, data, -1, flags | Qt.MatchFlag.MatchRecursive)
        for i in result:
            return i.row()

        return -1

    def findText(self, text: str, flags=Qt.MatchFlag.MatchExactly):
        """ Returns the index of the item containing the given text; otherwise returns -1. """
        return self.findData(text, Qt.ItemDataRole.EditRole, flags)

    def clear(self):
        """ Clears the combobox, removing all items. """
        if self.currentIndex() >= 0:
            self.setText('')

        self.model().blockSignals(True)
        self.model().clear()
        self._currentIndex = -1
        self.model().blockSignals(False)

    def count(self):
        """ Returns the number of items in the combobox """
        return self.model().rowCount()

    def setMaxVisibleItems(self, num: int):
        """ Set the maximum allowed size on screen of the combo box, measured in items, set to -1 indicates no restriction """
        self._maxVisibleItems = num

    def maxVisibleItems(self):
        """ Returns the maximum allowed size on screen of the combo box, measured in items """
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
        if self.count() == 0:
            return

        menu = self._createComboMenu()
        for i in range(self.count()):
            action = QAction(self.itemIcon(i), self.itemText(i),
                             triggered=lambda c=True, x=i: self._onItemClicked(x))
            menu.addAction(action)

        if menu.view.width() < self.width():
            menu.view.setMinimumWidth(self.width())
            menu.adjustSize()

        menu.setMaxVisibleItems(self.maxVisibleItems())
        menu.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        menu.closedSignal.connect(self._onDropMenuClosed)
        self.dropMenu = menu

        # set the selected item
        if self.currentIndex() >= 0:
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
        if index != self.currentIndex():
            self.setCurrentIndex(index)

        self.activated.emit(index)
        self.textActivated.emit(self.currentText())


class ModelComboBox(QPushButton, ModelComboBoxBase):
    """ Combo box build in data model """

    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)
    activated = Signal(int)
    textActivated = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._isIconVisible = True
        self.arrowAni = TranslateYAnimation(self)
        self._setUpUi()
        setFont(self)

    def setIconVisible(self, isVisible: bool):
        if isVisible == self._isIconVisible or self.currentIndex() < 0:
            return

        self._isIconVisible = isVisible

        if isVisible:
            self._updateIcon()
        else:
            self.setIcon(QIcon())

    def isIconVisible(self):
        return self._isIconVisible

    def _updateIcon(self):
        if not self._isIconVisible:
            return

        icon = self.itemIcon(self.currentIndex())
        if icon and not icon.isNull():
            self.setIcon(icon)
        else:
            self.setIcon(QIcon())

    def setPlaceholderText(self, text: str):
        self._placeholderText = text

        if self.currentIndex() <= 0:
            self._updateTextState(True)
            self.setText(text)

    def setCurrentIndex(self, index: int):
        if index < 0:
            self._currentIndex = -1
            self.setPlaceholderText(self._placeholderText)
        elif self._isValidIndex(index):
            self._updateTextState(False)
            super().setCurrentIndex(index)

        self._updateIcon()

    def clear(self):
        super().clear()
        self.setCurrentIndex(-1)

    def setItemIcon(self, index, icon):
        super().setItemIcon(index, icon)
        if index == self.currentIndex() and self.isIconVisible():
            self.setIcon(icon)

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


class EditableModelComboBox(LineEdit, ModelComboBoxBase):
    """ Editable combo box build in data model """

    currentIndexChanged = Signal(int)
    currentTextChanged = Signal(str)
    activated = Signal(int)
    textActivated = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.dropButton = LineEditButton(FIF.ARROW_DOWN, self)
        self._setUpUi()

        self.setTextMargins(0, 0, 29, 0)
        self.dropButton.setFixedSize(30, 25)
        self.hBoxLayout.addWidget(self.dropButton, 0, Qt.AlignmentFlag.AlignRight)

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
            self.setText(self.itemText(index))

    def clear(self):
        ModelComboBoxBase.clear(self)

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

    def _onComboTextChanged(self, text: str):
        self._currentIndex = -1
        self.currentTextChanged.emit(text)

        index = self.findText(text)
        if index >= 0:
            self._currentIndex = index
            self.currentIndexChanged.emit(index)

    def _onDropMenuClosed(self):
        self.dropMenu = None

    def _onClearButtonClicked(self):
        LineEdit.clear(self)
        self._currentIndex = -1
