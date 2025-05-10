# coding:utf-8
from PySide6.QtCore import QSize, Qt, Signal, QPoint, QRectF, QPropertyAnimation, Property, QEasingCurve
from PySide6.QtGui import QColor, QMouseEvent, QPainter, QPainterPath
from PySide6.QtWidgets import QProxyStyle, QSlider, QStyle, QStyleOptionSlider, QWidget

from ...common.style_sheet import FluentStyleSheet, themeColor, isDarkTheme
from ...common.color import autoFallbackThemeColor
from ...common.overload import singledispatchmethod



class SliderHandle(QWidget):
    """ Slider handle """

    pressed = Signal()
    released = Signal()

    def __init__(self, parent: QSlider):
        super().__init__(parent=parent)
        self.setFixedSize(22, 22)
        self._radius = 5
        self.lightHandleColor = QColor()
        self.darkHandleColor = QColor()
        self.radiusAni = QPropertyAnimation(self, b'radius', self)
        self.radiusAni.setDuration(100)

    @Property(int)
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, r):
        self._radius = r
        self.update()

    def setHandleColor(self, light, dark):
        self.lightHandleColor = QColor(light)
        self.darkHandleColor = QColor(dark)
        self.update()

    def enterEvent(self, e):
        self._startAni(6)

    def leaveEvent(self, e):
        self._startAni(5)

    def mousePressEvent(self, e):
        self._startAni(4)
        self.pressed.emit()

    def mouseReleaseEvent(self, e):
        self._startAni(6)
        self.released.emit()

    def _startAni(self, radius):
        self.radiusAni.stop()
        self.radiusAni.setStartValue(self.radius)
        self.radiusAni.setEndValue(radius)
        self.radiusAni.start()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        # draw outer circle
        isDark = isDarkTheme()
        painter.setPen(QColor(0, 0, 0, 90 if isDark else 25))
        painter.setBrush(QColor(69, 69, 69) if isDark else Qt.GlobalColor.white)
        painter.drawEllipse(self.rect().adjusted(1, 1, -1, -1))

        # draw innert circle
        painter.setBrush(autoFallbackThemeColor(self.lightHandleColor, self.darkHandleColor))
        painter.drawEllipse(QPoint(11, 11), self.radius, self.radius)



class Slider(QSlider):
    """ A slider can be clicked

    Constructors
    ------------
    * Slider(`parent`: QWidget = None)
    * Slider(`orient`: Qt.Orientation, `parent`: QWidget = None)
    """

    clicked = Signal(int)

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._postInit()

    @__init__.register
    def _(self, orientation: Qt.Orientation, parent: QWidget = None):
        super().__init__(orientation, parent=parent)
        self._postInit()

    def _postInit(self):
        self.handle = SliderHandle(self)
        self._pressedPos = QPoint()
        self.lightGrooveColor = QColor()
        self.darkGrooveColor = QColor()
        self.setOrientation(self.orientation())

        self.handle.pressed.connect(self.sliderPressed)
        self.handle.released.connect(self.sliderReleased)
        self.valueChanged.connect(self._adjustHandlePos)

    def setThemeColor(self, light, dark):
        self.lightGrooveColor = QColor(light)
        self.darkGrooveColor = QColor(dark)
        self.handle.setHandleColor(light, dark)
        self.update()

    def setOrientation(self, orientation: Qt.Orientation) -> None:
        super().setOrientation(orientation)
        if orientation == Qt.Orientation.Horizontal:
            self.setMinimumHeight(22)
        else:
            self.setMinimumWidth(22)

    def mousePressEvent(self, e: QMouseEvent):
        self._pressedPos = e.pos()
        self.setValue(self._posToValue(e.pos()))
        self.clicked.emit(self.value())

    def mouseMoveEvent(self, e: QMouseEvent):
        self.setValue(self._posToValue(e.pos()))
        self._pressedPos = e.pos()
        self.sliderMoved.emit(self.value())

    @property
    def grooveLength(self):
        l = self.width() if self.orientation() == Qt.Orientation.Horizontal else self.height()
        return l - self.handle.width()

    def _adjustHandlePos(self):
        total = max(self.maximum() - self.minimum(), 1)
        delta = int((self.value() - self.minimum()) / total * self.grooveLength)

        if self.orientation() == Qt.Orientation.Vertical:
            self.handle.move(0, delta)
        else:
            self.handle.move(delta, 0)

    def _posToValue(self, pos: QPoint):
        pd = self.handle.width() / 2
        gs = max(self.grooveLength, 1)
        v = pos.x() if self.orientation() == Qt.Orientation.Horizontal else pos.y()
        return int((v - pd) / gs * (self.maximum() - self.minimum()) + self.minimum())

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor(255, 255, 255, 115) if isDarkTheme() else QColor(0, 0, 0, 100))

        if self.orientation() == Qt.Orientation.Horizontal:
            self._drawHorizonGroove(painter)
        else:
            self._drawVerticalGroove(painter)

    def _drawHorizonGroove(self, painter: QPainter):
        w, r = self.width(), self.handle.width() / 2
        painter.drawRoundedRect(QRectF(r, r-2, w-r*2, 4), 2, 2)

        if self.maximum() - self.minimum() == 0:
            return

        painter.setBrush(autoFallbackThemeColor(self.lightGrooveColor, self.darkGrooveColor))
        aw = (self.value() - self.minimum()) / (self.maximum() - self.minimum()) * (w - r*2)
        painter.drawRoundedRect(QRectF(r, r-2, aw, 4), 2, 2)

    def _drawVerticalGroove(self, painter: QPainter):
        h, r = self.height(), self.handle.width() / 2
        painter.drawRoundedRect(QRectF(r-2, r, 4, h-2*r), 2, 2)

        if self.maximum() - self.minimum() == 0:
            return

        painter.setBrush(autoFallbackThemeColor(self.lightGrooveColor, self.darkGrooveColor))
        ah = (self.value() - self.minimum()) / (self.maximum() - self.minimum()) * (h - r*2)
        painter.drawRoundedRect(QRectF(r-2, r, 4, ah), 2, 2)

    def resizeEvent(self, e):
        self._adjustHandlePos()


class ClickableSlider(QSlider):
    """ A slider can be clicked """

    clicked = Signal(int)

    def mousePressEvent(self, e: QMouseEvent):
        super().mousePressEvent(e)

        if self.orientation() == Qt.Horizontal:
            value = int(e.pos().x() / self.width() * self.maximum())
        else:
            value = int((self.height()-e.pos().y()) /
                        self.height() * self.maximum())

        self.setValue(value)
        self.clicked.emit(self.value())



class HollowHandleStyle(QProxyStyle):
    """ Hollow handle style """

    def __init__(self, config: dict = None):
        """
        Parameters
        ----------
        config: dict
            style config
        """
        super().__init__()
        self.config = {
            "groove.height": 3,
            "sub-page.color": QColor(255, 255, 255),
            "add-page.color": QColor(255, 255, 255, 64),
            "handle.color": QColor(255, 255, 255),
            "handle.ring-width": 4,
            "handle.hollow-radius": 6,
            "handle.margin": 4
        }
        config = config if config else {}
        self.config.update(config)

        # get handle size
        w = self.config["handle.margin"]+self.config["handle.ring-width"] + \
            self.config["handle.hollow-radius"]
        self.config["handle.size"] = QSize(2*w, 2*w)

    def subControlRect(self, cc: QStyle.ComplexControl, opt: QStyleOptionSlider, sc: QStyle.SubControl, widget: QSlider):
        """ get the rectangular area occupied by the sub control """
        if cc != self.ComplexControl.CC_Slider or widget.orientation() != Qt.Horizontal \
                or sc == self.SubControl.SC_SliderTickmarks:
            return super().subControlRect(cc, opt, sc, widget)

        rect = widget.rect()

        if sc == self.SubControl.SC_SliderGroove:
            h = self.config["groove.height"]
            grooveRect = QRectF(0, (rect.height()-h)//2, rect.width(), h)
            return grooveRect.toRect()

        elif sc == self.SubControl.SC_SliderHandle:
            size = self.config["handle.size"]
            x = self.sliderPositionFromValue(
                widget.minimum(), widget.maximum(), widget.value(), rect.width())

            # solve the situation that the handle runs out of slider
            x *= (rect.width()-size.width())/rect.width()
            sliderRect = QRectF(x, 0, size.width(), size.height())
            return sliderRect.toRect()

    def drawComplexControl(self, cc: QStyle.ComplexControl, opt: QStyleOptionSlider, painter: QPainter, widget: QSlider):
        """ draw sub control """
        if cc != self.ComplexControl.CC_Slider or widget.orientation() != Qt.Horizontal:
            return super().drawComplexControl(cc, opt, painter, widget)

        grooveRect = self.subControlRect(cc, opt, self.SubControl.SC_SliderGroove, widget)
        handleRect = self.subControlRect(cc, opt, self.SubControl.SC_SliderHandle, widget)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        # paint groove
        painter.save()
        painter.translate(grooveRect.topLeft())

        # paint the crossed part
        w = handleRect.x()-grooveRect.x()
        h = self.config['groove.height']
        painter.setBrush(self.config["sub-page.color"])
        painter.drawRect(0, 0, w, h)

        # paint the uncrossed part
        x = w+self.config['handle.size'].width()
        painter.setBrush(self.config["add-page.color"])
        painter.drawRect(x, 0, grooveRect.width()-w, h)
        painter.restore()

        # paint handle
        ringWidth = self.config["handle.ring-width"]
        hollowRadius = self.config["handle.hollow-radius"]
        radius = ringWidth + hollowRadius

        path = QPainterPath()
        path.moveTo(0, 0)
        center = handleRect.center() + QPoint(1, 1)
        path.addEllipse(center, radius, radius)
        path.addEllipse(center, hollowRadius, hollowRadius)

        handleColor = self.config["handle.color"]  # type:QColor
        handleColor.setAlpha(255 if opt.activeSubControls !=
                             self.SubControl.SC_SliderHandle else 153)
        painter.setBrush(handleColor)
        painter.drawPath(path)

        # press handle
        if widget.isSliderDown():
            handleColor.setAlpha(255)
            painter.setBrush(handleColor)
            painter.drawEllipse(handleRect)
