# coding:utf-8
from typing import Iterable, List, Tuple

from PyQt5.QtCore import QPoint, Qt, pyqtSignal

from ..date_time.picker_base import (PickerBase, PickerColumnFormatter,
                                     PickerPanel)
from ...common.screen import getCurrentScreenGeometry

_MISSING = object()


class _ListPickerFormatter(PickerColumnFormatter):
    """ List picker formatter """

    def __init__(self):
        super().__init__()
        self._options = []   # type: List[Tuple[object, str]]

    def setOptions(self, options: Iterable):
        """ set the options to be encoded and decoded """
        self._options = list(options)

    def encode(self, value):
        """ convert original value to formatted value """
        for optionValue, optionText in self._options:
            if type(optionValue) is not type(value):
                continue

            try:
                if optionValue == value:
                    return optionText
            except Exception:
                continue

        return "" if value is None else str(value)

    def decode(self, value: str):
        """ convert formatted value to original value """
        for optionValue, optionText in self._options:
            if optionText == value:
                return optionValue

        return value


class _ListPickerPanel(PickerPanel):
    """ List picker panel """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.itemMaskWidget.setAttribute(Qt.WA_TransparentForMouseEvents)

    @staticmethod
    def visibleRowCount(count: int) -> int:
        """ return the number of visible rows of list """
        if count <= 3:
            return 3
        if count >= 9:
            return 9
        return count if count % 2 else count + 1

    def addColumn(self, items: Iterable, width: int, align=Qt.AlignCenter):
        """ add one column to view

        Parameters
        ----------
        items: Iterable
            the items to be added

        width: int
            the width of item

        align: Qt.AlignmentFlag
            the text alignment of item
        """
        itemList = list(items)
        super().addColumn(itemList, width, align)

        widget = self.listWidgets[-1]
        widget.itemClicked.connect(self._onItemClicked)
        visibleRows = self.visibleRowCount(len(itemList))
        if widget.visibleNumber != visibleRows:
            widget.visibleNumber = visibleRows
            widget.setItems(widget.originItems)

        widget.setFixedHeight(widget.itemSize.height() * visibleRows)
        self.listLayout.setAlignment(widget, Qt.AlignHCenter)

    def resizeEvent(self, e):
        self.itemMaskWidget.resize(self.view.width() - 3, self.itemHeight)
        margins = self.hBoxLayout.contentsMargins()
        visibleRows = max(
            (int(w.visibleNumber or 1) for w in self.listWidgets),
            default=1,
        )
        self.itemMaskWidget.move(
            margins.left() + 2,
            margins.top() + self.itemHeight * (visibleRows // 2),
        )

    def _confirmClickedItem(self, widget, item):
        """ confirm the clicked item and close the panel """
        # empty items are padded at the top and bottom to enable scrolling,
        # they are disabled and should not be confirmed
        if not item or not (item.flags() & Qt.ItemIsEnabled):
            return

        widget.setCurrentIndex(widget.row(item))
        widget.scrollToItem(widget.currentItem())
        self.confirmed.emit(self.value())
        self._fadeOut()

    def _onItemClicked(self, item):
        widget = self.sender()
        if widget is None:
            return

        self._confirmClickedItem(widget, item)


class ListPicker(PickerBase):
    """ List picker """

    FIXED = 0
    ADJUST_TO_CONTENTS = 1

    valueChanged = pyqtSignal(object)
    textChanged = pyqtSignal(str)

    def __init__(self, parent=None, items=None, placeholder=None, width=160,
                 widthMode=FIXED, align=Qt.AlignCenter):
        """ create a list picker

        Parameters
        ----------
        parent: QWidget
            the parent widget

        items: Iterable[Union[object, Tuple[object, str]]]
            the items of picker, an item can be a value or a (value, text) tuple

        placeholder: str
            the text to be displayed when no value is selected

        width: int
            the width of picker

        widthMode: int
            the width mode of panel, which can be `ListPicker.FIXED` or
            `ListPicker.ADJUST_TO_CONTENTS`

        align: Qt.AlignmentFlag
            the text alignment of items
        """
        super().__init__(parent=parent)
        self._value = None
        self._options = []   # type: List[Tuple[object, str]]
        self._formatter = _ListPickerFormatter()
        self._pickerWidth = max(0, int(width))
        self._widthMode = self.FIXED

        if placeholder is None:
            placeholder = self.tr("Please select")
        self.addColumn(placeholder, [], self._pickerWidth, align, self._formatter)
        self.setEnabled(False)
        self.setWidthMode(widthMode)

        if items is not None:
            self.setItems(items)

    def options(self) -> List[Tuple[object, str]]:
        """ return the options of picker """
        return list(self._options)

    def setItems(self, items: Iterable):
        """ set the items of picker

        Parameters
        ----------
        items: Iterable[Union[object, Tuple[object, str]]]
            the items of picker, an item can be a value or a (value, text) tuple
        """
        previousValue = self._value
        previousText = self.currentText()
        options = self._normalizeOptions(items)
        self._options = options
        self._formatter.setOptions(options)
        self.setColumnItems(0, [v for v, _ in options])
        self.setEnabled(bool(options))
        self._applyWidth()

        if previousValue is None:
            return

        matchedValue = self._matchValue(previousValue)
        if matchedValue is not _MISSING:
            self._value = matchedValue
            self.setColumnValue(0, matchedValue)
            currentText = self.currentText()
            if previousText != currentText:
                self.textChanged.emit(currentText or "")
            return

        self._clearValue(True)

    def currentValue(self):
        """ return the value of picker """
        return self._value

    def currentText(self) -> str:
        """ return the text of current value """
        if self._value is None:
            return None

        return self.encodeValue(0, self._value)

    def panelInitialValue(self):
        """ return the initial value of panel """
        currentText = self.currentText()
        return [] if currentText is None else [currentText]

    def setValue(self, value):
        """ set the value of picker

        Parameters
        ----------
        value: object
            the value of picker, `None` means that no value is selected
        """
        previousValue = self._value
        previousText = self.currentText()
        if value is None:
            self._clearValue(True)
            return

        matchedValue = self._matchValue(value)
        if matchedValue is _MISSING:
            raise ValueError(f"unknown picker value: {value!r}")

        self._value = matchedValue
        self.setColumnValue(0, matchedValue)
        self._applyWidth()
        currentText = self.currentText()
        if not self._valuesMatch(previousValue, matchedValue):
            self.valueChanged.emit(matchedValue)
        if previousText != currentText:
            self.textChanged.emit(currentText or "")

    def setPlaceholderText(self, text: str):
        """ set the text to be displayed when no value is selected """
        if not self.columns:
            return

        self.columns[0].setName(text)
        self._applyWidth()

    def setColumnValue(self, index: int, value):
        super().setColumnValue(index, value)
        if index == 0:
            self._elideColumnText()

    def showEvent(self, e):
        super().showEvent(e)
        # the font of button is set by qss and is only available after polish
        self._elideColumnText()

    def pickerWidth(self) -> int:
        """ return the width of picker """
        return self._pickerWidth

    def setPickerWidth(self, width: int):
        """ set the width of picker """
        self._pickerWidth = max(0, int(width))
        self._applyWidth()

    def widthMode(self) -> int:
        """ return the width mode of panel """
        return self._widthMode

    def setWidthMode(self, mode: int):
        """ set the width mode of panel

        Parameters
        ----------
        mode: int
            the width mode of panel, which can be `ListPicker.FIXED` or
            `ListPicker.ADJUST_TO_CONTENTS`
        """
        if mode not in (self.FIXED, self.ADJUST_TO_CONTENTS):
            raise ValueError(f"unknown width mode: {mode!r}")

        self._widthMode = mode
        self._applyWidth()

    def reset(self):
        """ clear the value of picker """
        self._clearValue(True)

    def _createPanel(self) -> _ListPickerPanel:
        panel = _ListPickerPanel(self)
        for column in self.columns:
            if not column.isHidden():
                # the width of view can't be set directly, the qss of view
                # will override the minimum width after it is polished
                width = max(column.width(), self._panelWidth())
                panel.addColumn(column.items(), width, column.align())

        panel.setValue(self.panelInitialValue())
        panel.setResetEnabled(self.isRestEnabled())
        panel.setScrollButtonRepeatEnabled(self._isScrollButtonRepeatEnabled)
        panel.setSelectedBackgroundColor(
            self.lightSelectedBackgroundColor, self.darkSelectedBackgroundColor)
        panel.confirmed.connect(self._onConfirmed)
        panel.resetted.connect(self.reset)
        panel.resize(panel.sizeHint())
        return panel

    def _showPanel(self):
        if not self.isEnabled() or not self._options:
            return

        panel = self._createPanel()
        # the width of view is invalid until its layout is activated
        widthDelta = panel.view.sizeHint().width() - self.width()
        offsetY = self._panelOffsetY(panel)
        panel.exec(self.mapToGlobal(QPoint(-widthDelta // 2, -offsetY)))

    def _panelOffsetY(self, panel: _ListPickerPanel) -> int:
        # center the selected row on the picker button
        visibleRows = _ListPickerPanel.visibleRowCount(len(self._options))
        topMargin = panel.layout().contentsMargins().top()
        selectedCenterX2 = topMargin * 2 + panel.itemHeight * visibleRows
        return (selectedCenterX2 - self.height()) // 2 - 4

    def _onConfirmed(self, value: list):
        text = value[0] if value else None
        selectedValue = None if text is None else self.decodeValue(0, text)

        if selectedValue is None:
            self._clearValue(True)
            return

        self.setValue(selectedValue)

    def _clearValue(self, emitSignal: bool):
        previousValue = self._value
        self._value = None
        super().reset()
        self._applyWidth()

        if emitSignal and previousValue is not None:
            self.valueChanged.emit(None)
            self.textChanged.emit("")

    def _matchValue(self, value):
        for optionValue, _ in self._options:
            if self._valuesMatch(optionValue, value):
                return optionValue

        return _MISSING

    @staticmethod
    def _valuesMatch(left, right) -> bool:
        if type(left) is not type(right):
            return False

        try:
            return left == right
        except Exception:
            return False

    def _elideColumnText(self):
        """ elide the text of button when it is wider than the button """
        if not self.columns:
            return

        button = self.columns[0]
        if self._value is None:
            text = button.name()
        else:
            text = self.encodeValue(0, self._value)

        fm = button.fontMetrics()
        width = button.width() - 22
        if 0 < width < fm.width(text):
            text = fm.elidedText(text, Qt.ElideRight, width)

        if text != button.text():
            button.setText(text)

    def _applyWidth(self):
        if not self.columns:
            return

        self.setColumnWidth(0, self._pickerWidth)
        self.setFixedHeight(self.columns[0].height())
        self.setFixedWidth(self._pickerWidth)
        self._elideColumnText()

    def _panelWidth(self) -> int:
        width = self._pickerWidth
        if self._widthMode == self.ADJUST_TO_CONTENTS:
            width = max(width, self._contentWidth())

        # the panel can't be wider than the screen, the excess text is elided
        # by the list widget, as WinUI ComboBox and Material menu do.
        # 40 = wheel margins(8) + view border(2) + panel margins(24) + slack
        screen = getCurrentScreenGeometry()
        return min(width, screen.width() - 40)

    def _contentWidth(self) -> int:
        texts = [self.columns[0].name(), *(text for _, text in self._options)]
        if not texts:
            return self._pickerWidth

        fm = self.fontMetrics()
        return max(fm.width(text) for text in texts) + 36

    def _normalizeOptions(self, items: Iterable) -> List[Tuple[object, str]]:
        options = []   # type: List[Tuple[object, str]]
        for item in items:
            if isinstance(item, tuple):
                if len(item) != 2:
                    raise ValueError("picker option tuple must be (value, text)")
                value, text = item
            else:
                value, text = item, str(item)

            text = str(text)
            if value is None:
                raise ValueError("picker option value cannot be None")
            if not text:
                raise ValueError("picker option text cannot be empty")
            if any(self._valuesMatch(v, value) for v, _ in options):
                raise ValueError(f"duplicate picker value: {value!r}")
            if any(t == text for _, t in options):
                raise ValueError(f"duplicate picker text: {text!r}")

            options.append((value, text))

        return options
