# coding: utf-8
from enum import Enum

from PyQt5.QtCore import Qt, pyqtProperty, pyqtSignal, QEvent, QPropertyAnimation, QEasingCurve, QPointF, QRectF
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QWidget

from ...common.style_sheet import FluentStyleSheet, themeColor, ThemeColor, isDarkTheme, setCustomStyleSheet
from ...common.overload import singledispatchmethod
from ...common.color import fallbackThemeColor, validColor
from .button import ToolButton


class Indicator(ToolButton):
    """ Indicator of switch button """

    checkedChanged = pyqtSignal(bool)
    normalKnobSize, hoverKnobSize = 12, 14
    pressedKnobWidth, pressedKnobHeight = 17, 14
    knobSlotWidth, trackLeft = 20, 1
    offSliderX, onSliderX, dragThreshold = 5, 25, 2
    controlFastDuration, controlFasterDuration = 167, 83
    stateEvents = (QEvent.EnabledChange, QEvent.MouseButtonPress, QEvent.Enter, QEvent.Leave)

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setCheckable(True)
        self.setFixedSize(42, 22)
        self.lightCheckedColor = QColor()
        self.darkCheckedColor = QColor()

        self._sliderX = self.offSliderX
        self._knobWidth = self._knobHeight = self.normalKnobSize
        self._checkedProgress = 0
        self._isDragging, self._pressX, self._pressSliderX = False, None, self.offSliderX
        curve = self._fastOutSlowInCurve()
        self.slideAni = QPropertyAnimation(self, b'sliderX', self)
        self.checkedAni = QPropertyAnimation(self, b'checkedProgress', self)
        self.knobWidthAni = QPropertyAnimation(self, b'knobWidth', self)
        self.knobHeightAni = QPropertyAnimation(self, b'knobHeight', self)

        for ani, duration, easing in [
            (self.slideAni, self.controlFastDuration, curve),
            (self.checkedAni, self.controlFasterDuration, QEasingCurve.Linear),
            (self.knobWidthAni, self.controlFasterDuration, curve),
            (self.knobHeightAni, self.controlFasterDuration, curve),
        ]:
            ani.setDuration(duration)
            ani.setEasingCurve(easing)

        self.toggled.connect(self._toggleSlider)

    @staticmethod
    def _fastOutSlowInCurve():
        curve = QEasingCurve(QEasingCurve.BezierSpline)
        curve.addCubicBezierSegment(QPointF(0, 0), QPointF(0, 1), QPointF(1, 1))
        return curve

    def event(self, e: QEvent):
        result = super().event(e)
        if e.type() in self.stateEvents:
            self._updateKnobSize()

        return result

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self._startDrag(e.pos().x())

        super().mousePressEvent(e)

    def mouseMoveEvent(self, e):
        if e.buttons() & Qt.LeftButton and self._moveDrag(e.pos().x()):
            e.accept()
            return

        super().mouseMoveEvent(e)

    def mouseReleaseEvent(self, e):
        """ toggle checked state when mouse release"""
        if e.button() == Qt.LeftButton and self._endDrag():
            self.checkedChanged.emit(self.isChecked())
            e.accept()
            return

        super().mouseReleaseEvent(e)
        self._updateKnobSize()
        self.checkedChanged.emit(self.isChecked())

    def _toggleSlider(self):
        self._startAnimation(self.slideAni, self.onSliderX if self.isChecked() else self.offSliderX, self.sliderX)
        self._startAnimation(self.checkedAni, 1 if self.isChecked() else 0, self.checkedProgress)

    def _startDrag(self, x, updateDown=False):
        self._isDragging, self._pressX, self._pressSliderX = False, x, self.sliderX

        if updateDown:
            self.setDown(True)

    def _moveDrag(self, x):
        if self._pressX is None or not self.isEnabled():
            return False

        dx = x - self._pressX

        if not self._isDragging:
            if abs(dx) < self.dragThreshold:
                return False

            self._isDragging = True
            self.slideAni.stop()
            self.checkedAni.stop()

        self.setSliderX(self._pressSliderX + dx)
        self.setCheckedProgress((self.sliderX - self.offSliderX) / self.knobSlotWidth)
        return True

    def _endDrag(self):
        isDragging = self._isDragging
        self._pressX = None
        self._isDragging = False

        if not isDragging:
            return False

        self.setDown(False)
        if self.sliderX <= 15 if self.isChecked() else self.sliderX >= 15:
            self.toggle()
        else:
            self._toggleSlider()

        return True

    def toggle(self):
        self.setChecked(not self.isChecked())

    def setDown(self, isDown: bool):
        self.isPressed = isDown
        super().setDown(isDown)
        self._updateKnobSize()

    def setHover(self, isHover: bool):
        self.isHover = isHover
        self._updateKnobSize()

    def setCheckedColor(self, light, dark):
        self.lightCheckedColor = QColor(light)
        self.darkCheckedColor = QColor(dark)
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
        painter.drawEllipse(self._knobRect())

    def _knobRect(self):
        w = self.knobWidth
        h = self.knobHeight
        y = (self.height() - h) / 2

        if self.isPressed and self.isEnabled():
            progress = self.checkedProgress if self._isDragging else int(self.isChecked())
            x = self.trackLeft + 3 + (self.knobSlotWidth * 2 - w - 6) * progress
        else:
            x = self.sliderX + (self.normalKnobSize - w) / 2

        return QRectF(x, y, w, h)

    def _updateKnobSize(self):
        if not self.isEnabled():
            size = (self.normalKnobSize, self.normalKnobSize)
        elif self.isPressed:
            size = (self.pressedKnobWidth, self.pressedKnobHeight)
        elif self.isHover:
            size = (self.hoverKnobSize, self.hoverKnobSize)
        else:
            size = (self.normalKnobSize, self.normalKnobSize)

        self._startKnobAnimation(*size)

    def _startKnobAnimation(self, width, height):
        if self.knobWidth == width and self.knobHeight == height:
            return

        self._startAnimation(self.knobWidthAni, width, self.knobWidth)
        self._startAnimation(self.knobHeightAni, height, self.knobHeight)

    @staticmethod
    def _startAnimation(ani: QPropertyAnimation, endValue, startValue):
        ani.stop()
        ani.setStartValue(startValue)
        ani.setEndValue(endValue)
        ani.start()

    def _backgroundColor(self):
        return self._transitionColor(self._offBackgroundColor, self._onBackgroundColor)

    def _onBackgroundColor(self, isDark: bool):
        color = self.darkCheckedColor if isDark else self.lightCheckedColor

        if not self.isEnabled():
            return QColor(255, 255, 255, 41) if isDark else QColor(0, 0, 0, 56)
        if self.isPressed:
            return validColor(color, ThemeColor.LIGHT_2.color())
        elif self.isHover:
            return validColor(color, ThemeColor.LIGHT_1.color())

        return fallbackThemeColor(color)

    def _offBackgroundColor(self, isDark: bool):
        if not self.isEnabled():
            return QColor(0, 0, 0, 0)
        if self.isPressed:
            return QColor(255, 255, 255, 18) if isDark else QColor(0, 0, 0, 23)
        elif self.isHover:
            return QColor(255, 255, 255, 10) if isDark else QColor(0, 0, 0, 15)

        return QColor(0, 0, 0, 0)

    def _borderColor(self):
        return self._transitionColor(self._offBorderColor, self._onBorderColor)

    def _onBorderColor(self, isDark: bool):
        if self.isEnabled():
            return self._onBackgroundColor(isDark)

        return QColor(0, 0, 0, 0)

    def _offBorderColor(self, isDark: bool):
        if self.isEnabled():
            return QColor(255, 255, 255, 153) if isDark else QColor(0, 0, 0, 133)

        return QColor(255, 255, 255, 41) if isDark else QColor(0, 0, 0, 56)

    def _sliderColor(self):
        return self._transitionColor(self._offSliderColor, self._onSliderColor)

    def _onSliderColor(self, isDark: bool):
        if self.isEnabled():
            return QColor(Qt.black if isDark else Qt.white)

        return QColor(255, 255, 255, 77) if isDark else QColor(255, 255, 255)

    def _offSliderColor(self, isDark: bool):
        if self.isEnabled():
            return QColor(255, 255, 255, 201) if isDark else QColor(0, 0, 0, 156)

        return QColor(255, 255, 255, 96) if isDark else QColor(0, 0, 0, 91)

    def _transitionColor(self, offColor, onColor):
        isDark = isDarkTheme()
        return self._mixColor(offColor(isDark), onColor(isDark), self.checkedProgress)

    @staticmethod
    def _mixColor(start: QColor, end: QColor, progress: float):
        progress = max(0, min(1, progress))

        return QColor(
            round(start.red() + (end.red() - start.red()) * progress),
            round(start.green() + (end.green() - start.green()) * progress),
            round(start.blue() + (end.blue() - start.blue()) * progress),
            round(start.alpha() + (end.alpha() - start.alpha()) * progress)
        )

    def getSliderX(self):
        return self._sliderX

    def setSliderX(self, x):
        self._sliderX = max(self.offSliderX, min(self.onSliderX, x))
        self.update()

    def getKnobWidth(self):
        return self._knobWidth

    def setKnobWidth(self, width):
        self._knobWidth = width
        self.update()

    def getKnobHeight(self):
        return self._knobHeight

    def setKnobHeight(self, height):
        self._knobHeight = height
        self.update()

    def getCheckedProgress(self):
        return self._checkedProgress

    def setCheckedProgress(self, progress):
        self._checkedProgress = max(0, min(1, progress))
        self.update()

    sliderX = pyqtProperty(float, getSliderX, setSliderX)
    knobWidth = pyqtProperty(float, getKnobWidth, setKnobWidth)
    knobHeight = pyqtProperty(float, getKnobHeight, setKnobHeight)
    checkedProgress = pyqtProperty(float, getCheckedProgress, setCheckedProgress)


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
        self.lightTextColor = QColor(0, 0, 0)
        self.darkTextColor = QColor(255, 255, 255)

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
        self.label.installEventFilter(self)
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
        FluentStyleSheet.SWITCH_BUTTON.apply(self.label)

        # connect signal to slot
        self.indicator.toggled.connect(self._updateText)
        self.indicator.toggled.connect(self.checkedChanged)

    def eventFilter(self, obj, e: QEvent):
        if obj in (self, self.label) and self.isEnabled():
            pos = self.indicator.mapFromGlobal(e.globalPos()).x() if hasattr(e, 'globalPos') else 0

            if e.type() == QEvent.MouseButtonPress and e.button() == Qt.LeftButton:
                self.indicator._startDrag(pos, True)
            elif e.type() == QEvent.MouseMove and e.buttons() & Qt.LeftButton and self.indicator._moveDrag(pos):
                return True
            elif e.type() == QEvent.MouseButtonRelease and e.button() == Qt.LeftButton:
                if not self.indicator._endDrag():
                    self.indicator.setDown(False)
                    self.indicator.toggle()

                return True
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

    def setTextColor(self, light, dark):
        """ set the color of text

        Parameters
        ----------
        light, dark: str | QColor | Qt.GlobalColor
            text color in light/dark theme mode
        """
        self.lightTextColor = QColor(light)
        self.darkTextColor = QColor(dark)

        setCustomStyleSheet(
            self.label,
            f"SwitchButton>QLabel{{color:{self.lightTextColor.name(QColor.NameFormat.HexArgb)}}}",
            f"SwitchButton>QLabel{{color:{self.darkTextColor.name(QColor.NameFormat.HexArgb)}}}"
        )

    def setCheckedIndicatorColor(self, light, dark):
        """ set the color of indicator in checked status

        Parameters
        ----------
        light, dark: str | QColor | Qt.GlobalColor
            border color in light/dark theme mode
        """
        self.indicator.setCheckedColor(light, dark)

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
