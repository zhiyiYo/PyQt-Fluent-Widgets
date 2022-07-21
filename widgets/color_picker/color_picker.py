# coding:utf-8
import colorsys
import math

from PyQt5.QtCore import QPoint, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QMouseEvent, QPainter, QPen, QPixmap
from PyQt5.QtWidgets import (QFrame, QGraphicsDropShadowEffect, QHBoxLayout,
                             QLabel, QPushButton, QSlider, QToolButton,
                             QVBoxLayout, QWidget)


class DefaultColorPanel(QWidget):
    """ Default color panel """

    colorSelected = pyqtSignal(QColor)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout0 = QHBoxLayout()
        self.hBoxLayout1 = QHBoxLayout()

        self.vBoxLayout.setSpacing(8)
        self.hBoxLayout0.setSpacing(6)
        self.hBoxLayout1.setSpacing(6)
        self.vBoxLayout.addLayout(self.hBoxLayout0)
        self.vBoxLayout.addLayout(self.hBoxLayout1)
        self.hBoxLayout0.setAlignment(Qt.AlignHCenter)
        self.hBoxLayout1.setAlignment(Qt.AlignHCenter)

        colors = [
            (255, 0, 0), (0, 255, 0), (0, 0, 255),
            (0, 255, 255), (255, 99, 71), (255, 0, 255),
            (138, 43, 226), (255, 255, 0), (255, 165, 0),
            (255, 68, 0), (0, 255, 157)
        ]
        for i, (r, g, b) in enumerate(colors):
            button = QPushButton()
            button.setStyleSheet(
                f"QPushButton{{background: rgb({r}, {g}, {b})}}")
            button.setFixedSize(32, 32)

            color = QColor(r, g, b)
            button.clicked.connect(
                lambda checked, c=color: self.colorSelected.emit(c))

            if i <= 5:
                self.hBoxLayout0.addWidget(button)
            else:
                self.hBoxLayout1.addWidget(button)


class Slider(QSlider):
    """ A slider which can be clicked """

    clicked = pyqtSignal(int)

    def __init__(self, orientation, parent=None):
        super().__init__(orientation, parent=parent)
        self.setRange(0, 255)
        self.setSingleStep(1)
        self.setValue(255)

    def mousePressEvent(self, e: QMouseEvent):
        super().mousePressEvent(e)
        if self.orientation() == Qt.Horizontal:
            value = int(e.pos().x() / self.width() * self.maximum())
        else:
            value = int((self.height()-e.pos().y()) /
                        self.height() * self.maximum())

        self.setValue(value)
        self.clicked.emit(value)


class SliderWidget(QWidget):
    """ Color picker slider widget """

    brightnessChanged = pyqtSignal(int)
    saturationChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedWidth(250)
        self.vBoxLayout = QVBoxLayout(self)
        self.brightnessLayout = QHBoxLayout()
        self.saturationLayout = QHBoxLayout()
        self.brightnessSlider = Slider(Qt.Horizontal)
        self.saturationSlider = Slider(Qt.Horizontal)
        self.brightnessIcon = QToolButton()
        self.saturationIcon = QToolButton()

        self.brightnessSlider.setObjectName('brightnessSlider')
        self.saturationSlider.setObjectName('saturationSlider')
        self.brightnessIcon.setObjectName('brightnessIcon')
        self.saturationIcon.setObjectName('saturationIcon')

        # initialize layout
        self.vBoxLayout.setSpacing(0)
        self.brightnessLayout.addWidget(self.brightnessSlider)
        self.brightnessLayout.addSpacing(4)
        self.brightnessLayout.addWidget(self.brightnessIcon)
        self.saturationLayout.addWidget(self.saturationSlider)
        self.saturationLayout.addSpacing(4)
        self.saturationLayout.addWidget(self.saturationIcon)
        self.vBoxLayout.addLayout(self.brightnessLayout)
        self.vBoxLayout.addLayout(self.saturationLayout)

        # connect signal to slot
        self.brightnessSlider.valueChanged.connect(self.brightnessChanged)
        self.saturationSlider.valueChanged.connect(self.saturationChanged)

    def setColor(self, color: QColor):
        """ set the color of slider """
        h = color.hue()
        self.setStyleSheet(f"""
           #brightnessSlider::groove{{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, x3:2, y3:0, stop:0 hsv({h}, 100, 100), stop:1 hsv({h},255,255));}}
           #saturationSlider::groove{{background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, x3:2, y3:0, stop:0 hsv({h}, 0, 200), stop:1 hsv({h},255,255));}}
        """)


class ColorWidget(QWidget):
    """ Color widget """

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.resize(55, 55)
        self.move(int(parent.width()/2-55/2), int(parent.height()/2-55/2))
        self.color = QColor(255, 0, 0)
        self.setAttribute(Qt.WA_TranslucentBackground)

    def setColor(self, color: QColor):
        self.color = color
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawEllipse(self.rect())


class ColorCircle(QWidget):
    """ Color circle """

    colorChanged = pyqtSignal(QColor)

    def __init__(self, startColor=QColor(0, 255, 255), parent=None):
        super().__init__(parent=parent)
        self.color = startColor  # type:QColor
        self.setFixedSize(250, 250)

        self.hueCircle = QLabel(self)
        self.hueCircle.setPixmap(QPixmap(
            'resource/wheel.png').scaled(250, 250, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.hueCircle.resize(250, 250)

        self.colorWidget = ColorWidget(self.hueCircle)
        self.mouseDot = QLabel(self.hueCircle)
        self.mouseDot.resize(30, 30)
        self.mouseDot.setObjectName("mouseDot")

        self.setColor(startColor)

    def setColor(self, color: QColor):
        """ set color """
        self.color = color
        self.colorWidget.setColor(color)
        self.__setMouseDotPosition(color.hue())
        self.colorChanged.emit(self.color)

    def setHue(self, hue):
        """ set hue """
        c = self.color
        c.setHsv(hue, c.saturation(), c.value())
        self.setColor(c)

    def setSaturation(self, saturation):
        """ set saturation """
        c = self.color
        c.setHsv(c.hue(), saturation, c.value())
        self.setColor(c)

    def setBrightness(self, brightness):
        """ set brightness """
        c = self.color
        c.setHsv(c.hue(), c.saturation(), brightness)
        self.setColor(c)

    def __setMouseDotPosition(self, hue):
        radius = self.height() / 2 - self.mouseDot.height() / 2 + 2
        angle = math.radians(hue)
        dy = math.cos(angle) * radius
        dx = math.sin(angle) * radius
        self.mouseDot.move(self.width()/2 + dx - self.mouseDot.width() / 2,
                           self.height()/2 - dy - self.mouseDot.height() / 2)

    def mousePressEvent(self, e: QMouseEvent):
        self.__handleEvent(e)

    def mouseMoveEvent(self, e: QMouseEvent):
        self.__handleEvent(e)

    def __handleEvent(self, e):
        x = e.x() - self.width()/2
        y = e.y() - self.height()/2
        if y == 0 and x < 0:
            angle = 270
        elif y == 0 and x > 0:
            angle = 90
        elif y == x == 0:
            angle = 0
        else:
            tangente = x / y
            angle = math.degrees(math.atan(tangente))
            if x >= 0 >= y:
                angle = -round(angle)
            if x >= 0 <= y:
                angle = 180 - round(angle)
            if x <= 0 <= y:
                angle = 180 - round(angle)
            if x <= 0 >= y:
                angle = 360 - round(angle)

        self.setHue(angle)


class ColorPickerPanel(QWidget):
    """ Color picker panel """

    colorChanged = pyqtSignal(QColor)

    def __init__(self, startColor=QColor(255, 0, 0), parent=None):
        super().__init__(parent=parent)
        self.setWindowFlags(
            Qt.Popup | Qt.NoDropShadowWindowHint | Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        with open('resource/color_picker.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

        self.hBoxLayout = QHBoxLayout(self)
        self.container = QFrame(self)
        self.vBoxLayout = QVBoxLayout(self.container)
        self.sliderWidget = SliderWidget()
        self.colorCircle = ColorCircle(startColor)
        self.defaultColorPanel = DefaultColorPanel()

        # add shadow
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setBlurRadius(32)
        self.shadowEffect.setColor(QColor(0, 0, 0, 70))
        self.shadowEffect.setOffset(0, 5)
        self.container.setGraphicsEffect(self.shadowEffect)

        # initialize layout
        self.hBoxLayout.setContentsMargins(20, 15, 20, 30)
        self.hBoxLayout.addWidget(self.container)
        self.vBoxLayout.setContentsMargins(15, 15, 15, 10)
        self.vBoxLayout.addWidget(self.colorCircle)
        self.vBoxLayout.addWidget(self.sliderWidget)
        self.vBoxLayout.addWidget(self.defaultColorPanel)

        # connect signal to slot
        self.defaultColorPanel.colorSelected.connect(self.colorCircle.setColor)
        self.sliderWidget.brightnessChanged.connect(
            self.colorCircle.setBrightness)
        self.sliderWidget.saturationChanged.connect(
            self.colorCircle.setSaturation)
        self.colorCircle.colorChanged.connect(self.__onColorchanged)

        self.sliderWidget.setColor(startColor)

    def __onColorchanged(self, color: QColor):
        self.sliderWidget.setColor(color)
        self.colorChanged.emit(color)


class ColorPicker(QWidget):
    """ Color picker """

    colorChanged = pyqtSignal(QColor)

    def __init__(self, color: QColor, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(40, 30)
        self.color = color
        self.colorPickerPanel = ColorPickerPanel(color, self)
        self.colorPickerPanel.colorChanged.connect(self.__onColorChanged)
        self.colorPickerPanel.hide()
        self.setCursor(Qt.PointingHandCursor)

    def __onColorChanged(self, color: QColor):
        self.color = color
        self.update()
        self.colorChanged.emit(color)

    def mousePressEvent(self, e):
        pos = self.mapToGlobal(QPoint())
        self.colorPickerPanel.move(pos+QPoint(50, -20))
        self.colorPickerPanel.show()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawRoundedRect(self.rect(), 5, 5)
