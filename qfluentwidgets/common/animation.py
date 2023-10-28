# coding: utf-8
from enum import Enum
from PySide2.QtCore import QEasingCurve, QEvent, QObject, QPropertyAnimation, Property, Signal, QPoint, QPointF
from PySide2.QtGui import QMouseEvent, QEnterEvent, QColor
from PySide2.QtWidgets import QWidget, QLineEdit, QGraphicsDropShadowEffect

from .config import qconfig


class AnimationBase(QObject):
    """ Animation base class """

    def __init__(self, parent: QWidget):
        super().__init__(parent=parent)
        parent.installEventFilter(self)

    def _onHover(self, e: QEnterEvent):
        pass

    def _onLeave(self, e: QEvent):
        pass

    def _onPress(self, e: QMouseEvent):
        pass

    def _onRelease(self, e: QMouseEvent):
        pass

    def eventFilter(self, obj, e: QEvent):
        if obj is self.parent():
            if e.type() == QEvent.MouseButtonPress:
                self._onPress(e)
            elif e.type() == QEvent.MouseButtonRelease:
                self._onRelease(e)
            elif e.type() == QEvent.Enter:
                self._onHover(e)
            elif e.type() == QEvent.Leave:
                self._onLeave(e)

        return super().eventFilter(obj, e)


class TranslateYAnimation(AnimationBase):

    valueChanged = Signal(float)

    def __init__(self, parent: QWidget, offset=2):
        super().__init__(parent)
        self._y = 0
        self.maxOffset = offset
        self.ani = QPropertyAnimation(self, b'y', self)

    def getY(self):
        return self._y

    def setY(self, y):
        self._y = y
        self.parent().update()
        self.valueChanged.emit(y)

    def _onPress(self, e):
        """ arrow down """
        self.ani.setEndValue(self.maxOffset)
        self.ani.setEasingCurve(QEasingCurve.OutQuad)
        self.ani.setDuration(150)
        self.ani.start()

    def _onRelease(self, e):
        """ arrow up """
        self.ani.setEndValue(0)
        self.ani.setDuration(500)
        self.ani.setEasingCurve(QEasingCurve.OutElastic)
        self.ani.start()

    y = Property(float, getY, setY)


class BackgroundAnimationWidget:
    """ Background animation widget """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.isHover = False
        self.isPressed = False
        self.bgColorObject = BackgroundColorObject(self)
        self.backgroundColorAni = QPropertyAnimation(
            self.bgColorObject, b'backgroundColor', self)
        self.backgroundColorAni.setDuration(120)
        self.installEventFilter(self)

        qconfig.themeChanged.connect(self._updateBackgroundColor)

    def eventFilter(self, obj, e):
        if obj is self:
            if e.type() == QEvent.Type.EnabledChange:
                if self.isEnabled():
                    self.setBackgroundColor(self._normalBackgroundColor())
                else:
                    self.setBackgroundColor(self._disabledBackgroundColor())

        return super().eventFilter(obj, e)

    def mousePressEvent(self, e):
        self.isPressed = True
        self._updateBackgroundColor()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        self._updateBackgroundColor()
        super().mouseReleaseEvent(e)

    def enterEvent(self, e):
        self.isHover = True
        self._updateBackgroundColor()

    def leaveEvent(self, e):
        self.isHover = False
        self._updateBackgroundColor()

    def focusInEvent(self, e):
        super().focusInEvent(e)
        self._updateBackgroundColor()

    def _normalBackgroundColor(self):
        return QColor(0, 0, 0, 0)

    def _hoverBackgroundColor(self):
        return self._normalBackgroundColor()

    def _pressedBackgroundColor(self):
        return self._normalBackgroundColor()

    def _focusInBackgroundColor(self):
        return self._normalBackgroundColor()

    def _disabledBackgroundColor(self):
        return self._normalBackgroundColor()

    def _updateBackgroundColor(self):
        if not self.isEnabled():
            color = self._disabledBackgroundColor()
        elif isinstance(self, QLineEdit) and self.hasFocus():
            color = self._focusInBackgroundColor()
        elif self.isPressed:
            color = self._pressedBackgroundColor()
        elif self.isHover:
            color = self._hoverBackgroundColor()
        else:
            color = self._normalBackgroundColor()

        self.backgroundColorAni.stop()
        self.backgroundColorAni.setEndValue(color)
        self.backgroundColorAni.start()

    def getBackgroundColor(self):
        return self.bgColorObject.backgroundColor

    def setBackgroundColor(self, color: QColor):
        self.bgColorObject.backgroundColor = color

    @property
    def backgroundColor(self):
        return self.getBackgroundColor()


class BackgroundColorObject(QObject):
    """ Background color object """

    def __init__(self, parent: BackgroundAnimationWidget):
        super().__init__(parent)
        self._backgroundColor = parent._normalBackgroundColor()

    @Property(QColor)
    def backgroundColor(self):
        return self._backgroundColor

    @backgroundColor.setter
    def backgroundColor(self, color: QColor):
        self._backgroundColor = color
        self.parent().update()

class DropShadowAnimation(QPropertyAnimation):
    """ Drop shadow animation """

    def __init__(self, parent: QWidget, normalColor=QColor(0, 0, 0, 0), hoverColor=QColor(0, 0, 0, 75)):
        super().__init__(parent=parent)
        self.normalColor = normalColor
        self.hoverColor = hoverColor
        self.offset = QPoint(0, 0)
        self.blurRadius = 38
        self.isHover = False

        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setColor(self.normalColor)

        parent.installEventFilter(self)

    def setBlurRadius(self, radius: int):
        self.blurRadius = radius

    def setOffset(self, dx: int, dy: int):
        self.offset = QPoint(dx, dy)

    def setNormalColor(self, color: QColor):
        self.normalColor = color

    def setHoverColor(self, color: QColor):
        self.hoverColor = color

    def setColor(self, color):
        pass

    def _createShadowEffect(self):
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setOffset(self.offset)
        self.shadowEffect.setBlurRadius(self.blurRadius)
        self.shadowEffect.setColor(self.normalColor)

        self.setTargetObject(self.shadowEffect)
        self.setStartValue(self.shadowEffect.color())
        self.setPropertyName(b'color')
        self.setDuration(150)

        return self.shadowEffect

    def eventFilter(self, obj, e):
        if obj is self.parent() and self.parent().isEnabled():
            if e.type() in [QEvent.Type.Enter]:
                self.isHover = True

                if self.state() != QPropertyAnimation.State.Running:
                    self.parent().setGraphicsEffect(self._createShadowEffect())

                self.setEndValue(self.hoverColor)
                self.start()
            elif e.type() in [QEvent.Type.Leave, QEvent.Type.MouseButtonPress]:
                self.isHover = False
                if self.parent().graphicsEffect():
                    self.finished.connect(self._onAniFinished)
                    self.setEndValue(self.normalColor)
                    self.start()

        return super().eventFilter(obj, e)

    def _onAniFinished(self):
        self.finished.disconnect()
        self.shadowEffect = None
        self.parent().setGraphicsEffect(None)


class FluentAnimationSpeed(Enum):
    """ Fluent animation speed """
    FAST = 0
    MEDIUM = 1
    SLOW = 2


class FluentAnimationType(Enum):
    """ Fluent animation type """
    FAST_INVOKE = 0
    STRONG_INVOKE = 1
    FAST_DISMISS = 2
    SOFT_DISMISS = 3
    POINT_TO_POINT = 4
    FADE_IN_OUT = 5


class FluentAnimationProperty(Enum):
    """ Fluent animation property """
    POSITION = "position"
    SCALE = "scale"
    ANGLE = "angle"
    OPACITY = "opacity"



class FluentAnimationProperObject(QObject):
    """ Fluent animation property object """

    objects = {}

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def getValue(self):
        return 0

    def setValue(self):
        pass

    @classmethod
    def register(cls, name):
        """ register menu animation manager

        Parameters
        ----------
        name: Any
            the name of manager, it should be unique
        """
        def wrapper(Manager):
            if name not in cls.objects:
                cls.objects[name] = Manager

            return Manager

        return wrapper

    @classmethod
    def create(cls, propertyType: FluentAnimationProperty, parent=None):
        if propertyType not in cls.objects:
            raise ValueError(f"`{propertyType}` has not been registered")

        return cls.objects[propertyType](parent)


@FluentAnimationProperObject.register(FluentAnimationProperty.POSITION)
class PositionObject(FluentAnimationProperObject):
    """ Position object """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._position = QPoint()

    def getValue(self):
        return self._position

    def setValue(self, pos: QPoint):
        self._position = pos
        self.parent().update()

    position = Property(QPoint, getValue, setValue)


@FluentAnimationProperObject.register(FluentAnimationProperty.SCALE)
class ScaleObject(FluentAnimationProperObject):
    """ Scale object """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._scale = 1

    def getValue(self):
        return self._scale

    def setValue(self, scale: float):
        self._scale = scale
        self.parent().update()

    scale = Property(float, getValue, setValue)


@FluentAnimationProperObject.register(FluentAnimationProperty.ANGLE)
class AngleObject(FluentAnimationProperObject):
    """ Angle object """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._angle = 0

    def getValue(self):
        return self._angle

    def setValue(self, angle: float):
        self._angle = angle
        self.parent().update()

    angle = Property(float, getValue, setValue)


@FluentAnimationProperObject.register(FluentAnimationProperty.OPACITY)
class OpacityObject(FluentAnimationProperObject):
    """ Opacity object """

    def __init__(self, parent=None):
        super().__init__(parent)
        self._opacity = 0

    def getValue(self):
        return self._opacity

    def setValue(self, opacity: float):
        self._opacity = opacity
        self.parent().update()

    opacity = Property(float, getValue, setValue)


class FluentAnimation(QPropertyAnimation):
    """ Fluent animation base """

    animations = {}

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setSpeed(FluentAnimationSpeed.FAST)
        self.setEasingCurve(self.curve())

    @classmethod
    def createBezierCurve(cls, x1, y1, x2, y2):
        curve = QEasingCurve(QEasingCurve.BezierSpline)
        curve.addCubicBezierSegment(QPointF(x1, y1), QPointF(x2, y2), QPointF(1, 1))
        return curve

    @classmethod
    def curve(cls):
        return cls.createBezierCurve(0, 0, 1, 1)

    def setSpeed(self, speed: FluentAnimationSpeed):
        """ set the speed of animation """
        self.setDuration(self.speedToDuration(speed))

    def speedToDuration(self, speed: FluentAnimationSpeed):
        return 100

    def startAnimation(self, endValue, startValue=None):
        self.stop()

        if startValue is None:
            self.setStartValue(self.value())
        else:
            self.setStartValue(startValue)

        self.setEndValue(endValue)
        self.start()

    def value(self):
        return self.targetObject().getValue()

    def setValue(self, value):
        self.targetObject().setValue(value)

    @classmethod
    def register(cls, name):
        """ register menu animation manager

        Parameters
        ----------
        name: Any
            the name of manager, it should be unique
        """
        def wrapper(Manager):
            if name not in cls.animations:
                cls.animations[name] = Manager

            return Manager

        return wrapper

    @classmethod
    def create(cls, aniType: FluentAnimationType, propertyType: FluentAnimationProperty,
               speed=FluentAnimationSpeed.FAST, value=None, parent=None) -> "FluentAnimation":
        if aniType not in cls.animations:
            raise ValueError(f"`{aniType}` has not been registered.")

        obj = FluentAnimationProperObject.create(propertyType, parent)
        ani = cls.animations[aniType](parent)

        ani.setSpeed(speed)
        ani.setTargetObject(obj)
        ani.setPropertyName(propertyType.value.encode())

        if value is not None:
            ani.setValue(value)

        return ani


@FluentAnimation.register(FluentAnimationType.FAST_INVOKE)
class FastInvokeAnimation(FluentAnimation):
    """ Fast invoke animation """

    @classmethod
    def curve(cls):
        return cls.createBezierCurve(0, 0, 0, 1)

    def speedToDuration(self, speed: FluentAnimationSpeed):
        if speed == FluentAnimationSpeed.FAST:
            return 187
        if speed == FluentAnimationSpeed.MEDIUM:
            return 333

        return 500


@FluentAnimation.register(FluentAnimationType.STRONG_INVOKE)
class StrongInvokeAnimation(FluentAnimation):
    """ Strong invoke animation """

    @classmethod
    def curve(cls):
        return cls.createBezierCurve(0.13, 1.62, 0, 0.92)

    def speedToDuration(self, speed: FluentAnimationSpeed):
        return 667


@FluentAnimation.register(FluentAnimationType.FAST_DISMISS)
class FastDismissAnimation(FastInvokeAnimation):
    """ Fast dismiss animation """


@FluentAnimation.register(FluentAnimationType.SOFT_DISMISS)
class SoftDismissAnimation(FluentAnimation):
    """ Soft dismiss animation """

    @classmethod
    def curve(cls):
        return cls.createBezierCurve(1, 0, 1, 1)

    def speedToDuration(self, speed: FluentAnimationSpeed):
        return 167


@FluentAnimation.register(FluentAnimationType.POINT_TO_POINT)
class PointToPointAnimation(FastDismissAnimation):
    """ Point to point animation """

    @classmethod
    def curve(cls):
        return cls.createBezierCurve(0.55, 0.55, 0, 1)


@FluentAnimation.register(FluentAnimationType.FADE_IN_OUT)
class FadeInOutAnimation(FluentAnimation):
    """ Fade in/out animation """

    def speedToDuration(self, speed: FluentAnimationSpeed):
        return 83