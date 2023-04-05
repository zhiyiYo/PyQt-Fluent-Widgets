# coding:utf-8
from PySide6.QtCore import QEasingCurve, Qt, QPropertyAnimation
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QScrollArea, QScrollBar

from ...common.smooth_scroll import SmoothScroll


class ScrollArea(QScrollArea):
    """ A scroll area which can scroll smoothly """

    def __init__(self, parent=None, orient=Qt.Vertical):
        """
        Parameters
        ----------
        parent: QWidget
            parent widget

        orient: Orientation
            scroll orientation
        """
        super().__init__(parent)
        self.smoothScroll = SmoothScroll(self, orient)

    def setSmoothMode(self, mode):
        """ set smooth mode

        Parameters
        ----------
        mode: SmoothMode
            smooth scroll mode
        """
        self.smoothScroll.setSmoothMode(mode)

    def wheelEvent(self, e: QWheelEvent):
        self.smoothScroll.wheelEvent(e)
        e.setAccepted(True)


class SmoothScrollBar(QScrollBar):
    """ Smooth scroll bar """

    def __init__(self, parent=None):
        QScrollBar.__init__(self, parent)
        self.duration = 500
        self.ani = QPropertyAnimation()
        self.ani.setTargetObject(self)
        self.ani.setPropertyName(b"value")
        self.ani.setEasingCurve(QEasingCurve.OutCubic)
        self.ani.setDuration(self.duration)

        self.__value = self.value()

    def setValue(self, value):
        if value == self.value():
            return

        # stop running animation
        self.ani.stop()

        # adjust the duration
        dv = abs(value - self.value())
        if dv < 50:
            self.ani.setDuration(self.duration * dv / 70)
        else:
            self.ani.setDuration(self.duration)

        self.ani.setStartValue(self.value())
        self.ani.setEndValue(value)
        self.ani.start()

    def scrollValue(self, value):
        """ scroll the specified distance """
        self.__value += value
        self.__value = max(self.minimum(), self.__value)
        self.__value = min(self.maximum(), self.__value)
        self.setValue(self.__value)

    def scrollTo(self, value):
        """ scroll to the specified position """
        self.__value = value
        self.__value = max(self.minimum(), self.__value)
        self.__value = min(self.maximum(), self.__value)
        self.setValue(self.__value)

    def resetValue(self, value):
        self.__value = value

    def mousePressEvent(self, e):
        self.ani.stop()
        super().mousePressEvent(e)
        self.__value = self.value()

    def mouseReleaseEvent(self, e):
        self.ani.stop()
        super().mouseReleaseEvent(e)
        self.__value = self.value()

    def mouseMoveEvent(self, e):
        self.ani.stop()
        super().mouseMoveEvent(e)
        self.__value = self.value()

    def setScrollAnimation(self, duration, easing=QEasingCurve.OutCubic):
        """ set scroll animation

        Parameters
        ----------
        duration: int
            scroll duration

        easing: QEasingCurve
            animation type
        """
        self.duration = duration
        self.ani.setDuration(duration)
        self.ani.setEasingCurve(easing)


class SmoothScrollArea(QScrollArea):
    """ Smooth scroll area """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hScrollBar = SmoothScrollBar()
        self.vScrollBar = SmoothScrollBar()
        self.hScrollBar.setOrientation(Qt.Horizontal)
        self.vScrollBar.setOrientation(Qt.Vertical)
        self.setVerticalScrollBar(self.vScrollBar)
        self.setHorizontalScrollBar(self.hScrollBar)

    def setScrollAnimation(self, orient, duration, easing=QEasingCurve.OutCubic):
        """ set scroll animation

        Parameters
        ----------
        orient: Orient
            scroll orientation

        duration: int
            scroll duration

        easing: QEasingCurve
            animation type
        """
        bar = self.hScrollBar if orient == Qt.Horizontal else self.vScrollBar
        bar.setScrollAnimation(duration, easing)

    def wheelEvent(self, e):
        if e.modifiers() == Qt.NoModifier:
            self.vScrollBar.scrollValue(-e.angleDelta().y())
        else:
            self.hScrollBar.scrollValue(-e.angleDelta().x())
