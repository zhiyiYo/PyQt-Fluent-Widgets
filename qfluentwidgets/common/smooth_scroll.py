# coding:utf-8
from collections import deque
from enum import Enum
from math import cos, pi, ceil

from PyQt5.QtCore import QDateTime, Qt, QTimer, QPoint, QObject, QElapsedTimer
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import QApplication, QScrollArea, QAbstractScrollArea


class SmoothScroll:
    """ Scroll smoothly """

    def __init__(self, widget: QScrollArea, orient=Qt.Vertical, dynamicEngineEnabled=True):
        """
        Parameters
        ----------
        widget: QScrollArea
            scroll area to scroll smoothly

        orient: Orientation
            scroll orientation

        dynamicEngineEnabled: bool
            whether to choose scroll engine dynamically based on the screen dpi
        """
        self.widget = widget
        self.orient = orient

        self.dynamicEngineEnabled = dynamicEngineEnabled
        self.widthThreshold = 2560

        self.smoothMode = SmoothMode(SmoothMode.LINEAR)
        self.fixedStepScrollEngine = FixedStepSmoothScrollEngine(widget, orient)
        self.adaptiveScrollEngine = AdaptiveSmoothScrollEngine(widget, orient)

    def setDynamicEngineEnabled(self, isEnabled: bool):
        """ set whether to use dynamic engine """
        self.dynamicEngineEnabled = isEnabled

    def setSmoothMode(self, smoothMode):
        """ set smooth mode """
        self.smoothMode = smoothMode
        self.fixedStepScrollEngine.setSmoothMode(smoothMode)
        self.adaptiveScrollEngine.setSmoothMode(smoothMode)

    def wheelEvent(self, e):
        # only process the wheel events triggered by mouse, fixes issue #75
        delta = e.angleDelta().y() if e.angleDelta().y() != 0 else e.angleDelta().x()
        if self.smoothMode == SmoothMode.NO_SMOOTH or abs(delta) % 120 != 0:
            QAbstractScrollArea.wheelEvent(self.widget, e)
            return

        engine = self._chooseScrollEngine()
        engine.wheelEvent(e, delta)

    def _chooseScrollEngine(self) -> "SmoothScrollEngineBase":
        """ choose scroll engine """
        # ellapse time driven adaptive scroll engine for HiDPI screen
        if self.dynamicEngineEnabled and self.widget.width()*self.widget.devicePixelRatioF() > self.widthThreshold:
            return self.adaptiveScrollEngine

        return self.fixedStepScrollEngine


class SmoothMode(Enum):
    """ Smooth mode """
    NO_SMOOTH = 0
    CONSTANT = 1
    LINEAR = 2
    QUADRATI = 3
    COSINE = 4


class SmoothScrollEngineBase(QObject):

    def __init__(self, widget: QScrollArea, orient=Qt.Vertical):
        super().__init__(widget)
        self.widget = widget
        self.orient = orient
        self.fps = 60
        self.duration = 400
        self.stepsTotal = 0
        self.stepRatio = 1.5
        self.acceleration = 1
        self.lastWheelEvent = None
        self.scrollStamps = deque()
        self.stepsLeftQueue = deque()
        self.smoothMoveTimer = QTimer(widget)
        self.smoothMode = SmoothMode(SmoothMode.LINEAR)
        self.smoothMoveTimer.timeout.connect(self._smoothMove)

    def setSmoothMode(self, smoothMode):
        """ set smooth mode """
        self.smoothMode = smoothMode

    def wheelEvent(self, e: QWheelEvent, delta: int):
        raise NotImplementedError

    def _smoothMove(self):
        if not self.stepsLeftQueue:
            return

        # send interpolated scroll event to scroll bar
        totalDelta = self._getTotalDelta()
        self.sendScrollEventToScrollBar(totalDelta)

        # stop scrolling if the queque is empty
        if not self.stepsLeftQueue:
            self.smoothMoveTimer.stop()

    def _getTotalDelta(self) -> float:
        raise NotImplementedError

    def sendScrollEventToScrollBar(self, totalDelta):
        # construct wheel event
        if self.orient == Qt.Orientation.Vertical:
            p = QPoint(0, round(totalDelta))
            bar = self.widget.verticalScrollBar()
        else:
            p = QPoint(round(totalDelta), 0)
            bar = self.widget.horizontalScrollBar()

        e = QWheelEvent(
            self.lastWheelEvent.pos(),
            self.lastWheelEvent.globalPos(),
            QPoint(),
            p,
            round(totalDelta),
            self.orient,
            self.lastWheelEvent.buttons(),
            Qt.KeyboardModifier.NoModifier
        )

        # send wheel event to app
        QApplication.sendEvent(bar, e)


class FixedStepSmoothScrollEngine(SmoothScrollEngineBase):
    """ Scroll smoothly (fixed step) """

    def wheelEvent(self, e: QWheelEvent, delta: int):
        # push current time to queque
        now = QDateTime.currentDateTime().toMSecsSinceEpoch()
        self.scrollStamps.append(now)
        while now - self.scrollStamps[0] > 500:
            self.scrollStamps.popleft()

        # adjust the acceration ratio based on unprocessed events
        accerationRatio = min(len(self.scrollStamps) / 15, 1)
        if not self.lastWheelEvent:
            self.lastWheelEvent = QWheelEvent(e)
        else:
            self.lastWheelEvent = e

        # get the number of steps
        self.stepsTotal = self.fps * self.duration / 1000

        # get the moving distance corresponding to each event
        delta = delta * self.stepRatio
        if self.acceleration > 0:
            delta += delta * self.acceleration * accerationRatio

        # form a list of moving distances and steps, and insert it into the queue for processing.
        self.stepsLeftQueue.append([delta, self.stepsTotal])

        # overflow time of timer: 1000ms/frames
        self.smoothMoveTimer.start(int(1000 / self.fps))

    def _getTotalDelta(self):
        """ scroll smoothly when timer time out """
        totalDelta = 0

        # Calculate the scrolling distance of all unprocessed events,
        # the timer will reduce the number of steps by 1 each time it overflows.
        for i in self.stepsLeftQueue:
            totalDelta += self._subDelta(i[0], i[1])
            i[1] -= 1

        # If the event has been processed, move it out of the queue
        while self.stepsLeftQueue and self.stepsLeftQueue[0][1] == 0:
            self.stepsLeftQueue.popleft()

        return totalDelta

    def _subDelta(self, delta, stepsLeft):
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


class AdaptiveSmoothScrollEngine(SmoothScrollEngineBase):
    """ Scroll smoothly (time-based, adaptive, HiDPI friendly) """

    def __init__(self, widget: QScrollArea, orient=Qt.Vertical):
        super().__init__(widget, orient)
        self.elapsedTimer = QElapsedTimer()
        self.maxQueueSize = 3
        self.minDuration = 120

    def setSmoothMode(self, smoothMode):
        """ set smooth mode """
        self.smoothMode = smoothMode

    def wheelEvent(self, e, delta: int):
        now = QDateTime.currentDateTime().toMSecsSinceEpoch()
        self.scrollStamps.append(now)
        while self.scrollStamps and now - self.scrollStamps[0] > 500:
            self.scrollStamps.popleft()

        accelerationRatio = min(len(self.scrollStamps) / 15, 1)

        self.lastWheelEvent = QWheelEvent(e)

        # Calculate adaptive duration based on queue pressure
        queuePressure = len(self.stepsLeftQueue)
        pressureRatio = min(queuePressure / self.maxQueueSize, 1)

        effectiveDuration = self.duration * (1 - 0.6 * pressureRatio)
        effectiveDuration = max(self.minDuration, effectiveDuration)

        # Calculate delta
        delta = delta * self.stepRatio
        if self.acceleration > 0:
            delta += delta * self.acceleration * accelerationRatio

        # Merge events if queue is full
        if len(self.stepsLeftQueue) >= self.maxQueueSize:
            last = self.stepsLeftQueue[-1]
            last[0] += delta
            last[1] = max(last[1], effectiveDuration)
        else:
            self.stepsLeftQueue.append([delta, effectiveDuration])

        if not self.elapsedTimer.isValid():
            self.elapsedTimer.start()
        else:
            self.elapsedTimer.restart()

        # Start timer with adaptive fps
        self.smoothMoveTimer.start(int(1000 / self.fps))

    def _getTotalDelta(self):
        dt = self.elapsedTimer.restart()  # elapsed time in ms
        totalDelta = 0.0

        for item in self.stepsLeftQueue:
            remainingDelta, remainingTime = item

            if remainingTime <= 0:
                continue

            consumeTime = min(dt, remainingTime)
            ratio = consumeTime / remainingTime
            subDelta = self._subDelta(remainingDelta, ratio)

            item[0] -= subDelta
            item[1] -= consumeTime
            totalDelta += subDelta

        # Remove finished items
        while self.stepsLeftQueue and self.stepsLeftQueue[0][1] <= 0:
            self.stepsLeftQueue.popleft()

        return totalDelta

    def _subDelta(self, delta, ratio):
        """ Calculate interpolated delta for current frame """
        if self.smoothMode == SmoothMode.CONSTANT:
            return delta * ratio
        if self.smoothMode == SmoothMode.LINEAR:
            return delta * ratio
        if self.smoothMode == SmoothMode.QUADRATI:
            return delta * (1 - (1 - ratio) ** 2)
        if self.smoothMode == SmoothMode.COSINE:
            return delta * (1 - cos(ratio * pi)) / 2

        return delta * ratio
