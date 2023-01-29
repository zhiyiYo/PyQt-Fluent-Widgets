# coding:utf-8
from collections import deque
from enum import Enum
from math import cos, pi

from PySide6.QtCore import QDateTime, QEasingCurve, Qt, QTimer, QPoint, Signal, QPropertyAnimation, QPointF
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import QApplication, QScrollArea, QScrollBar


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
        self.orient = orient
        self.fps = 60
        self.duration = 400
        self.stepsTotal = 0
        self.stepRatio = 1.5
        self.acceleration = 1
        self.lastWheelPos = 0
        self.lastWheelGlobalPos = 0
        self.scrollStamps = deque()
        self.stepsLeftQueue = deque()
        self.smoothMoveTimer = QTimer(self)
        self.smoothMode = SmoothMode(SmoothMode.LINEAR)
        self.smoothMoveTimer.timeout.connect(self.__smoothMove)

    def setSmoothMode(self, smoothMode):
        """ set smooth mode """
        self.smoothMode = smoothMode

    def wheelEvent(self, e: QWheelEvent):
        if self.smoothMode == SmoothMode.NO_SMOOTH:
            super().wheelEvent(e)
            return

        # push current time to queque
        now = QDateTime.currentDateTime().toMSecsSinceEpoch()
        self.scrollStamps.append(now)
        while now - self.scrollStamps[0] > 500:
            self.scrollStamps.popleft()

        # adjust the acceration ratio based on unprocessed events
        accerationRatio = min(len(self.scrollStamps) / 15, 1)
        self.lastWheelPos = e.position()
        self.lastWheelGlobalPos = e.globalPosition()

        # get the number of steps
        self.stepsTotal = self.fps * self.duration / 1000

        # get the moving distance corresponding to each event
        delta = e.angleDelta().y() * self.stepRatio
        if self.acceleration > 0:
            delta += delta * self.acceleration * accerationRatio

        # form a list of moving distances and steps, and insert it into the queue for processing.
        self.stepsLeftQueue.append([delta, self.stepsTotal])

        # overflow time of timer: 1000ms/frames
        self.smoothMoveTimer.start(1000 / self.fps)

    def __smoothMove(self):
        """ scroll smoothly when timer time out """
        totalDelta = 0

        # Calculate the scrolling distance of all unprocessed events,
        # the timer will reduce the number of steps by 1 each time it overflows.
        for i in self.stepsLeftQueue:
            totalDelta += self.__subDelta(i[0], i[1])
            i[1] -= 1

        # If the event has been processed, move it out of the queue
        while self.stepsLeftQueue and self.stepsLeftQueue[0][1] == 0:
            self.stepsLeftQueue.popleft()

        # construct wheel event
        if self.orient == Qt.Orientation.Vertical:
            pixelDelta = QPoint(round(totalDelta), 0)
            bar = self.verticalScrollBar()
        else:
            pixelDelta = QPoint(0, round(totalDelta))
            bar = self.horizontalScrollBar()

        e = QWheelEvent(
            self.lastWheelPos,
            self.lastWheelGlobalPos,
            pixelDelta,
            QPoint(totalDelta, 0),
            Qt.MouseButton.LeftButton,
            Qt.KeyboardModifier.NoModifier,
            Qt.ScrollPhase.ScrollBegin,
            False,
        )

        # send wheel event to app
        QApplication.sendEvent(bar, e)

        # stop scrolling if the queque is empty
        if not self.stepsLeftQueue:
            self.smoothMoveTimer.stop()

    def __subDelta(self, delta, stepsLeft):
        """ get the interpolation for each step """
        m = self.stepsTotal / 2
        x = abs(self.stepsTotal - stepsLeft - m)

        res = 0
        if self.smoothMode == SmoothMode.NO_SMOOTH:
            res = 0
        elif self.smoothMode == SmoothMode.CONSTANT:
            res = delta / self.stepsTotal
        elif self.smoothMode == SmoothMode.LINEAR:
            res = 2 * delta / self.stepsTotal * (m - x) / m
        elif self.smoothMode == SmoothMode.QUADRATI:
            res = 3 / 4 / m * (1 - x * x / m / m) * delta
        elif self.smoothMode == SmoothMode.COSINE:
            res = (cos(x * pi / m) + 1) / (2 * m) * delta

        return res


class SmoothMode(Enum):
    """ Smooth mode """
    NO_SMOOTH = 0
    CONSTANT = 1
    LINEAR = 2
    QUADRATI = 3
    COSINE = 4


class SmoothScrollBar(QScrollBar):
    """ Smooth scroll bar """

    scrollFinished = Signal()

    def __init__(self, parent=None):
        QScrollBar.__init__(self, parent)
        self.ani = QPropertyAnimation()
        self.ani.setTargetObject(self)
        self.ani.setPropertyName(b"value")
        self.ani.setEasingCurve(QEasingCurve.OutCubic)
        self.ani.setDuration(500)
        self.ani.finished.connect(self.scrollFinished)

    def setValue(self, value: int):
        if value == self.value():
            return

        # stop running animation
        self.ani.stop()
        self.scrollFinished.emit()

        self.ani.setStartValue(self.value())
        self.ani.setEndValue(value)
        self.ani.start()

    def scrollValue(self, value: int):
        """ scroll the specified distance """
        value += self.value()
        self.scrollTo(value)

    def scrollTo(self, value: int):
        """ scroll to the specified position """
        value = min(self.maximum(), max(self.minimum(), value))
        self.setValue(value)

    def mousePressEvent(self, e):
        self.ani.stop()
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.ani.stop()
        super().mouseReleaseEvent(e)

    def mouseMoveEvent(self, e):
        self.ani.stop()
        super().mouseMoveEvent(e)


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
        bar.ani.setDuration(duration)
        bar.ani.setEasingCurve(easing)

    def wheelEvent(self, e):
        if e.modifiers() == Qt.NoModifier:
            self.vScrollBar.scrollValue(-e.angleDelta().y())
        else:
            self.hScrollBar.scrollValue(-e.angleDelta().x())
