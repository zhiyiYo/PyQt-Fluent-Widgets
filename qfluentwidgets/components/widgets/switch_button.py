# coding: utf-8
from enum import Enum

from PyQt5.QtCore import Qt, QTimer, pyqtProperty, pyqtSignal, QEvent, QPoint, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QPainter, QHoverEvent
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QLabel, QToolButton, QWidget

from ...common.style_sheet import FluentStyleSheet, themeColor, ThemeColor, isDarkTheme
from ...common.overload import singledispatchmethod
from .button import ToolButton


class Indicator(ToolButton):
    """ Indicator of switch button """

    checkedChanged = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setCheckable(True)
        self.setFixedSize(42, 22)

        self._sliderX = 5
        self.slideAni = QPropertyAnimation(self, b'sliderX', self)
        self.slideAni.setDuration(120)

        self.toggled.connect(self._toggleSlider)

    def mouseReleaseEvent(self, e):
        """ toggle checked state when mouse release"""
        super().mouseReleaseEvent(e)
        self.checkedChanged.emit(self.isChecked())

    def _toggleSlider(self):
        self.slideAni.setEndValue(25 if self.isChecked() else 5)
        self.slideAni.start()

    def toggle(self):
        self.setChecked(not self.isChecked())

    def setDown(self, isDown: bool):
        self.isPressed = isDown
        super().setDown(isDown)

    def setHover(self, isHover: bool):
        self.isHover = isHover
        self.update()

    def paintEvent(self, e):
        """ paint indicator """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        self._drawBackground(painter)
        self._drawCircle(painter)

    def _drawBackground(self, painter: QPainter):
        r = self.height() / 2
        painter.setPen(self._borderColor())
        painter.setBrush(self._backgroundColor())
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), r, r)

    def _drawCircle(self, painter: QPainter):
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._sliderColor())
        painter.drawEllipse(int(self.sliderX), 5, 12, 12)

    def _backgroundColor(self):
        isDark = isDarkTheme()

        if self.isChecked():
            if not self.isEnabled():
                return QColor(255, 255, 255, 41) if isDark else QColor(0, 0, 0, 56)
            if self.isPressed:
                return ThemeColor.LIGHT_2.color()
            elif self.isHover:
                return ThemeColor.LIGHT_1.color()

            return themeColor()
        else:
            if not self.isEnabled():
                return QColor(0, 0, 0, 0)
            if self.isPressed:
                return QColor(255, 255, 255, 18) if isDark else QColor(0, 0, 0, 23)
            elif self.isHover:
                return QColor(255, 255, 255, 10) if isDark else QColor(0, 0, 0, 15)

            return QColor(0, 0, 0, 0)

    def _borderColor(self):
        isDark = isDarkTheme()

        if self.isChecked():
            return self._backgroundColor() if self.isEnabled() else QColor(0, 0, 0, 0)
        else:
            if self.isEnabled():
                return QColor(255, 255, 255, 153) if isDark else QColor(0, 0, 0, 133)

            return QColor(255, 255, 255, 41) if isDark else QColor(0, 0, 0, 56)

    def _sliderColor(self):
        isDark = isDarkTheme()

        if self.isChecked():
            if self.isEnabled():
                return QColor(Qt.black if isDark else Qt.white)

            return QColor(255, 255, 255, 77) if isDark else QColor(255, 255, 255)
        else:
            if self.isEnabled():
                return QColor(255, 255, 255, 201) if isDark else QColor(0, 0, 0, 156)

            return QColor(255, 255, 255, 96) if isDark else QColor(0, 0, 0, 91)

    def getSliderX(self):
        return self._sliderX

    def setSliderX(self, x):
        self._sliderX = max(x, 5)
        self.update()

    sliderX = pyqtProperty(float, getSliderX, setSliderX)


class IndicatorPosition(Enum):
    """ Indicator position """
    LEFT = 0
    RIGHT = 1


class SwitchButton(QWidget):
    """ Switch button class

    Constructors
    ------------
    * SwitchButton(`parent`: QWidget = None)
    * SwitchButton(`text`: str = "Off", `parent`: QWidget = None, `indicatorPos`=IndicatorPosition.LEFT)
    """

    checkedChanged = pyqtSignal(bool)

    @singledispatchmethod
    def __init__(self, parent: QWidget = None, indicatorPos=IndicatorPosition.LEFT):
        """
        Parameters
        ----------
        parent: QWidget
            parent widget

        indicatorPosition: IndicatorPosition
            the position of indicator
        """
        super().__init__(parent=parent)
        self._text = self.tr('Off')
        self._offText =  self.tr('Off')
        self._onText =  self.tr('On')
        self.__spacing = 12

        self.indicatorPos = indicatorPos
        self.hBox = QHBoxLayout(self)
        self.indicator = Indicator(self)
        self.label = QLabel(self._text, self)

        self.__initWidget()

    @__init__.register
    def _(self, text: str = 'Off', parent: QWidget = None, indicatorPos=IndicatorPosition.LEFT):
        """
        Parameters
        ----------
        text: str
            the text of switch button

        parent: QWidget
            parent widget

        indicatorPosition: IndicatorPosition
            the position of indicator
        """
        self.__init__(parent, indicatorPos)
        self._offText = text
        self.setText(text)

    def __initWidget(self):
        """ initialize widgets """
        self.setAttribute(Qt.WA_StyledBackground)
        self.installEventFilter(self)
        self.setFixedHeight(22)

        # set layout
        self.hBox.setSpacing(self.__spacing)
        self.hBox.setContentsMargins(2, 0, 0, 0)

        if self.indicatorPos == IndicatorPosition.LEFT:
            self.hBox.addWidget(self.indicator)
            self.hBox.addWidget(self.label)
            self.hBox.setAlignment(Qt.AlignLeft)
        else:
            self.hBox.addWidget(self.label, 0, Qt.AlignRight)
            self.hBox.addWidget(self.indicator, 0, Qt.AlignRight)
            self.hBox.setAlignment(Qt.AlignRight)

        # set default style sheet
        FluentStyleSheet.SWITCH_BUTTON.apply(self)

        # connect signal to slot
        self.indicator.toggled.connect(self._updateText)
        self.indicator.toggled.connect(self.checkedChanged)

    def eventFilter(self, obj, e: QEvent):
        if obj is self and self.isEnabled():
            if e.type() == QEvent.MouseButtonPress:
                self.indicator.setDown(True)
            elif e.type() == QEvent.MouseButtonRelease:
                self.indicator.setDown(False)
                self.indicator.toggle()
            elif e.type() == QEvent.Enter:
                self.indicator.setHover(True)
            elif e.type() == QEvent.Leave:
                self.indicator.setHover(False)

        return super().eventFilter(obj, e)

    def isChecked(self):
        return self.indicator.isChecked()

    def setChecked(self, isChecked):
        """ set checked state """
        self._updateText()
        self.indicator.setChecked(isChecked)

    def toggleChecked(self):
        """ toggle checked state """
        self.indicator.setChecked(not self.indicator.isChecked())

    def _updateText(self):
        self.setText(self.onText if self.isChecked() else self.offText)
        self.adjustSize()

    def getText(self):
        return self._text

    def setText(self, text):
        self._text = text
        self.label.setText(text)
        self.adjustSize()

    def getSpacing(self):
        return self.__spacing

    def setSpacing(self, spacing):
        self.__spacing = spacing
        self.hBox.setSpacing(spacing)
        self.update()

    def getOnText(self):
        return self._onText

    def setOnText(self, text):
        self._onText = text
        self._updateText()

    def getOffText(self):
        return self._offText

    def setOffText(self, text):
        self._offText = text
        self._updateText()

    spacing = pyqtProperty(int, getSpacing, setSpacing)
    checked = pyqtProperty(bool, isChecked, setChecked)
    text = pyqtProperty(str, getText, setText)
    onText = pyqtProperty(str, getOnText, setOnText)
    offText = pyqtProperty(str, getOffText, setOffText)