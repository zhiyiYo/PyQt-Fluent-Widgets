# coding: utf-8
from PyQt6.QtCore import QEasingCurve, QEvent, QObject, QPropertyAnimation, pyqtProperty, pyqtSignal
from PyQt6.QtGui import QMouseEvent, QEnterEvent
from PyQt6.QtWidgets import QWidget



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
            if e.type() == QEvent.Type.MouseButtonPress:
                self._onPress(e)
            elif e.type() == QEvent.Type.MouseButtonRelease:
                self._onRelease(e)
            elif e.type() == QEvent.Type.Enter:
                self._onHover(e)
            elif e.type() == QEvent.Type.Leave:
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
        self.ani.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.ani.setDuration(150)
        self.ani.start()

    def _onRelease(self, e):
        """ arrow up """
        self.ani.setEndValue(0)
        self.ani.setDuration(500)
        self.ani.setEasingCurve(QEasingCurve.Type.OutElastic)
        self.ani.start()

