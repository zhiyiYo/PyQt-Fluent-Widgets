# coding: utf-8
from PyQt5.QtCore import QEasingCurve, QEvent, QObject, QPropertyAnimation, pyqtProperty, pyqtSignal, QPoint
from PyQt5.QtGui import QMouseEvent, QEnterEvent, QColor
from PyQt5.QtWidgets import QWidget, QLineEdit, QGraphicsDropShadowEffect

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

    valueChanged = pyqtSignal(float)

    def __init__(self, parent: QWidget, offset=2):
        super().__init__(parent)
        self._y = 0
        self.maxOffset = offset
        self.ani = QPropertyAnimation(self, b'y', self)

    @pyqtProperty(float)
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
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

    @pyqtProperty(QColor)
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