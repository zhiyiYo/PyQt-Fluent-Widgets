# coding:utf-8
from typing import Union, List, Iterable

from PyQt5.QtCore import (Qt, pyqtSignal, QRectF, QRect, QPoint, QObject, QEvent,
                          QVariantAnimation, QEasingCurve)
from PyQt5.QtGui import QPainter, QIcon, QColor
from PyQt5.QtWidgets import QAction, QPushButton, QApplication, QWidget, QStyle, QStyleOptionButton

from .menu import RoundMenu, MenuAnimationType, IndicatorMenuItemDelegate
from .line_edit import LineEdit, LineEditButton
from ...common.config import qconfig
from ...common.icon import FluentIconBase, isDarkTheme
from ...common.icon import FluentIcon as FIF
from ...common.font import setFont
from ...common.style_sheet import FluentStyleSheet


class _ComboBoxBase(QObject):
    """ Shared combo box interaction. """

    currentIndexChanged = pyqtSignal(int)
    currentTextChanged = pyqtSignal(str)
    activated = pyqtSignal(int)
    textActivated = pyqtSignal(str)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent=parent)
        self.isHover = False
        self.isPressed = False
        self._currentIndex = -1
        self._maxVisibleItems = -1
        self.dropMenu = None
        self._placeholderText = ""

        assert isinstance(self, QWidget)
        FluentStyleSheet.COMBO_BOX.apply(self)
        self.installEventFilter(self)

    def eventFilter(self, obj, e):
        if self.dropMenu is not None and self.dropMenu.isVisible():
            if obj in (self, self.dropMenu._hostWindow):
                if e.type() in (QEvent.Type.Move, QEvent.Type.Resize):
                    self.dropMenu._relayout()
                elif e.type() in (QEvent.Type.Hide, QEvent.Type.Close):
                    self._closeComboMenu()
        if obj is self:
            if isinstance(self, _ComboBoxButton):
                self._onComboEvent(e)
            if isinstance(self, QWidget) and e.type() in (QEvent.Type.Hide, QEvent.Type.EnabledChange):
                if e.type() == QEvent.Type.Hide or not self.isEnabled():
                    self._closeComboMenu()
        return super().eventFilter(obj, e)

    def _closeComboMenu(self):
        if self.dropMenu is not None:
            self.dropMenu.close()

    def _onDropMenuClosed(self):
        if self.dropMenu is not None:
            window = self.dropMenu._hostWindow
            if window is not None and window is not self:
                window.removeEventFilter(self)
        self.dropMenu = None

    def _createComboMenu(self):
        return ComboBoxMenu(self)

    def _isItemEnabled(self, index) -> bool:
        return True

    def count(self) -> int:
        raise NotImplementedError

    def itemText(self, index: int) -> str:
        raise NotImplementedError

    def itemIcon(self, index: int) -> QIcon:
        raise NotImplementedError

    def currentText(self) -> str:
        raise NotImplementedError

    def setCurrentIndex(self, index: int):
        raise NotImplementedError

    def currentIndex(self):
        return self._currentIndex

    def setMaxVisibleItems(self, num: int):
        self._maxVisibleItems = num

    def maxVisibleItems(self):
        return self._maxVisibleItems

    def _showComboMenu(self):
        assert isinstance(self, QWidget)
        if not self.isEnabled() or not self.count() or self.dropMenu is not None:
            return

        menu = self._createComboMenu()
        for i in range(self.count()):
            action = QAction(self.itemIcon(i), self.itemText(i), menu)
            action.triggered.connect(lambda checked, index=i: self._onItemClicked(index))
            action.setEnabled(self._isItemEnabled(i))
            menu.addAction(action)

        menu.setMaxVisibleItems(self.maxVisibleItems())
        menu.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        menu.closedSignal.connect(self._onDropMenuClosed)
        self.dropMenu = menu
        if menu._hostWindow is not None and menu._hostWindow is not self:
            menu._hostWindow.installEventFilter(self)
        menu.exec(self.mapToGlobal(QPoint()))

    def _toggleComboMenu(self):
        if self.dropMenu is not None:
            self._closeComboMenu()
        else:
            self._showComboMenu()

    def _onItemClicked(self, index):
        if not 0 <= index < self.count() or not self._isItemEnabled(index):
            return
        if index != self.currentIndex():
            self.setCurrentIndex(index)

        self.activated.emit(index)
        self.textActivated.emit(self.currentText())

    def _syncComboMenu(self):
        if self.dropMenu is not None:
            self.dropMenu._syncCurrentIndex()


class _ComboBoxButton(QPushButton):
    """ Combo box button shared by item and model based controls. """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._opacity = 1.0
        self._opacityAni = QVariantAnimation(self)
        self._opacityAni.setDuration(150)
        self._opacityAni.setEasingCurve(QEasingCurve.Type.OutQuart)
        self._opacityAni.valueChanged.connect(self._onOpacityChanged)
        self._backgroundColor = self._normalBackgroundColor()
        self.backgroundColorAni = QVariantAnimation(self)
        self.backgroundColorAni.valueChanged.connect(self._onBackgroundChanged)
        self.backgroundColorAni.setDuration(187)
        self.backgroundColorAni.setEasingCurve(QEasingCurve.Type.OutQuart)
        self.pressed.connect(self._updateBackgroundColor)
        self.released.connect(self._updateBackgroundColor)
        qconfig.themeChanged.connect(self._updateBackgroundColor)
        setFont(self)

    def setPlaceholderText(self, text: str):
        assert isinstance(self, _ComboBoxBase)
        self._placeholderText = text

        if self.currentIndex() < 0:
            self._updateTextState(True)
            self.setText(text)

    def _updateTextState(self, isPlaceholder):
        if self.property("isPlaceholderText") == isPlaceholder:
            return

        self.setProperty("isPlaceholderText", isPlaceholder)
        self.setStyle(QApplication.style())

    def _onBackgroundChanged(self, color):
        self._backgroundColor = color
        self.update()

    def _onOpacityChanged(self, opacity):
        self._opacity = opacity
        self.update()

    def _normalBackgroundColor(self):
        return QColor(255, 255, 255, 17 if isDarkTheme() else 178)

    def _hoverBackgroundColor(self):
        return QColor(255, 255, 255, 21) if isDarkTheme() else QColor(249, 249, 249, 128)

    def _pressedBackgroundColor(self):
        return QColor(255, 255, 255, 11) if isDarkTheme() else QColor(249, 249, 249, 77)

    def _updateBackgroundColor(self):
        self.isPressed = self.isDown()
        if self.isPressed:
            color = self._pressedBackgroundColor()
        elif self.isHover:
            color = self._hoverBackgroundColor()
        else:
            color = self._normalBackgroundColor()
        self.backgroundColorAni.stop()
        self.backgroundColorAni.setStartValue(self._backgroundColor)
        self.backgroundColorAni.setEndValue(color)
        self.backgroundColorAni.start()
        self._opacityAni.stop()
        self._opacityAni.setStartValue(self._opacity)
        self._opacityAni.setEndValue(0.7 if self.isPressed else 1.0)
        self._opacityAni.start()

    def _onComboEvent(self, e):
        if e.type() in (QEvent.Type.Enter, QEvent.Type.Leave):
            self.isHover = e.type() == QEvent.Type.Enter
            self._updateBackgroundColor()
        elif e.type() == QEvent.Type.EnabledChange:
            self._updateBackgroundColor()

    def mouseMoveEvent(self, e):
        super().mouseMoveEvent(e)
        if self.isPressed != self.isDown():
            self._updateBackgroundColor()

    def mouseReleaseEvent(self, e):
        isClick = (e is not None and e.button() == Qt.MouseButton.LeftButton
                   and self.isDown() and self.rect().contains(e.pos()))
        super().mouseReleaseEvent(e)
        self._updateBackgroundColor()
        if isClick:
            self._toggleComboMenu()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setOpacity(self._opacity if self.isEnabled() else 0.4)
        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self._backgroundColor)
        painter.drawRoundedRect(QRectF(self.rect()).adjusted(0.5, 0.5, -0.5, -0.5), 5, 5)
        painter.restore()

        option = QStyleOptionButton()
        self.initStyleOption(option)
        style = self.style()
        if style is not None:
            style.drawControl(QStyle.ControlElement.CE_PushButton, option, painter, self)
        color = '#ffffff' if isDarkTheme() else '#000000'
        painter.setOpacity(painter.opacity() * (0.6047 if isDarkTheme() else 0.6063))
        FIF.ARROW_DOWN.render(painter, QRectF(self.width() - 27, self.height() / 2 - 7, 14, 14), fill=color)


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


class ComboBoxBase(_ComboBoxBase):
    """ Combo box base """

    currentIndexChanged = pyqtSignal(int)
    currentTextChanged = pyqtSignal(str)
    activated = pyqtSignal(int)
    textActivated = pyqtSignal(str)

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent=parent)
        self.items = []     # type: List[ComboItem]

    def addItem(self, text: str, icon: Union[str, QIcon, FluentIconBase] = None, userData=None):
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
        self._closeComboMenu()
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

    def _isItemEnabled(self, index):
        return self.items[index].isEnabled


class ComboBox(_ComboBoxButton, ComboBoxBase):
    """ Combo box """

    currentIndexChanged = pyqtSignal(int)
    currentTextChanged = pyqtSignal(str)
    activated = pyqtSignal(int)
    textActivated = pyqtSignal(str)

    def setCurrentIndex(self, index: int):
        if index < 0:
            self._currentIndex = -1
            self.setPlaceholderText(self._placeholderText)
        elif 0 <= index < len(self.items):
            self._updateTextState(False)
            super().setCurrentIndex(index)
        self._syncComboMenu()


class EditableComboBox(LineEdit, ComboBoxBase):
    """ Editable combo box """

    currentIndexChanged = pyqtSignal(int)
    currentTextChanged = pyqtSignal(str)
    activated = pyqtSignal(int)
    textActivated = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.dropButton = LineEditButton(FIF.ARROW_DOWN, self)

        self.setTextMargins(0, 0, 29, 0)
        self.dropButton.setFixedSize(30, 25)
        self.hBoxLayout.addWidget(self.dropButton, 0, Qt.AlignmentFlag.AlignRight)

        self.dropButton.clicked.connect(self._toggleComboMenu)
        self.textChanged.connect(self._onComboTextChanged)
        self.returnPressed.connect(self._onReturnPressed)

        self.clearButton.disconnect()
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
        self._syncComboMenu()

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

    def _onComboTextChanged(self, text: str):
        self._currentIndex = -1
        self.currentTextChanged.emit(text)

        for i, item in enumerate(self.items):
            if item.text == text:
                self._currentIndex = i
                self.currentIndexChanged.emit(i)
                return

    def _onClearButtonClicked(self):
        LineEdit.clear(self)
        self._currentIndex = -1


class ComboBoxMenu(RoundMenu):
    """ Combo box menu """

    def __init__(self, parent=None):
        super().__init__(title="", parent=parent)
        self._comboBox = parent if isinstance(parent, _ComboBoxBase) else None
        self.view.setItemDelegate(IndicatorMenuItemDelegate(self.view))
        self.view.setObjectName('comboListWidget')
        self._hostWindow = parent.window() if isinstance(parent, QWidget) else None
        if self._comboBox is not None:
            self._comboBox.currentIndexChanged.connect(self._syncCurrentIndex)

    def _syncCurrentIndex(self):
        if self._comboBox is None:
            return
        index = self._comboBox.currentIndex()
        actions = self.menuActions()
        item = actions[index].property('item') if 0 <= index < len(actions) else None
        if self.view.currentItem() is item:
            return
        self.view.setCurrentItem(item)
        if item is None:
            self.view.clearSelection()
        if self.isVisible():
            self._relayout()

    def _layout(self):
        host = self._comboBox
        assert isinstance(host, QWidget)
        window = self._hostWindow
        assert window is not None
        bounds = QRect(window.mapToGlobal(QPoint()), window.size()).adjusted(8, 8, -8, -8)
        screen = host.screen()
        if screen is not None:
            bounds = bounds.intersected(screen.availableGeometry().adjusted(8, 8, -8, -8))
        anchor = QRect(host.mapToGlobal(QPoint()), host.size())
        margins = self.view.viewportMargins()
        inset = margins.top() + self.view.frameWidth()
        self._contentHeight = sum(self.view.sizeHintForRow(i) for i in range(self.view.count()))
        insetHeight = margins.top() + margins.bottom() + 2 * self.view.frameWidth()
        fullHeight = self._contentHeight + insetHeight
        paddingHeight = fullHeight - len(self.menuActions()) * self.itemHeight
        limit = self.view.maxVisibleItems() * self.itemHeight + paddingHeight if self.view.maxVisibleItems() > 0 else 300
        height = max(1, min(fullHeight, limit, bounds.height()))
        width = max(host.width(), max((a.property('item').sizeHint().width() for a in self.menuActions()), default=0))
        width = max(1, min(width, bounds.width()))
        self.view.setFixedSize(width, height)
        self.view.doItemsLayout()

        item = self.view.currentItem()
        selected = item is not None
        self._selectedTop = self.view.visualItemRect(item).top() + self.view.scrollDelegate.vScrollBar.value() if selected else 0
        rowHeight = item.sizeHint().height() if selected else self.itemHeight
        self._rowHeight = rowHeight
        offset = max(0, (anchor.height() - rowHeight) // 2)
        y = anchor.y() + (anchor.height() - height) // 2
        self._mode = 0
        scroll = 0
        if selected:
            y = anchor.y() + offset - inset - self._selectedTop
            if y < bounds.top() or y + height > bounds.bottom() + 1:
                top = anchor.y() + offset - inset
                bottom = anchor.y() + anchor.height() - offset + inset
                topHeight = min(height, bounds.bottom() + 1 - top) if top >= bounds.top() else 0
                bottomHeight = min(height, bottom - bounds.top())
                modes = (1, 2) if y < bounds.top() else (2, 1)
                for mode in modes:
                    available = topHeight if mode == 1 else bottomHeight
                    if available >= rowHeight + insetHeight:
                        self._mode = mode
                        height = available
                        y = top if mode == 1 else bottom - height
                        break
                else:
                    y = anchor.y() + (anchor.height() - height) // 2
                    scroll = self._scrollFor(height, 0)
            if self._mode:
                scroll = self._scrollFor(height, self._mode)

        x = anchor.x() if selected else anchor.x() + (anchor.width() - width) // 2
        if x + width > bounds.right() + 1:
            x = anchor.right() + 1 - width
        x = max(bounds.left(), min(x, bounds.right() + 1 - width))
        y = max(bounds.top(), min(y, bounds.bottom() + 1 - height))
        self._endRect = QRect(x, y, width, height)
        self._endScroll = scroll
        self._startHeight = min(46, height)
        self._startScroll = self._scrollFor(self._startHeight, self._mode) if selected else 0
        if self._mode == 1:
            self._startY = y
        elif self._mode == 2:
            self._startY = y + height - self._startHeight
        elif selected:
            self._startY = y - scroll + self._startScroll
        else:
            self._startY = y + (height - self._startHeight) // 2

        self._setMenuGeometry()

    def _relayout(self):
        self._aniGroup.stop()
        self._layout()
        self.setWindowOpacity(1.0)
        self._onExpandFinished()

    def hideEvent(self, e):
        if self._comboBox is not None and self._comboBox.dropMenu is self:
            self._comboBox._onDropMenuClosed()
        super().hideEvent(e)
        if self.testAttribute(Qt.WidgetAttribute.WA_DeleteOnClose):
            self.deleteLater()

    def exec(self, pos, ani=True, aniType=MenuAnimationType.DROP_DOWN):
        if self._comboBox is None:
            return super().exec(pos, ani, aniType)
        self._aniGroup.stop()
        self._syncCurrentIndex()
        self._layout()
        self._showMenu(ani)
