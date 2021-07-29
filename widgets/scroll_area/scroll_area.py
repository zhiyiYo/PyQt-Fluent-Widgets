# coding:utf-8
from collections import deque
from enum import Enum
from math import cos, pi

from PyQt5.QtCore import QDateTime, Qt, QTimer, QT_VERSION_STR
from PyQt5.QtGui import QWheelEvent
from PyQt5.QtWidgets import QApplication, QScrollArea


class ScrollArea(QScrollArea):
    """ 一个可以平滑滚动的区域 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.fps = 60
        self.duration = 400
        self.stepsTotal = 0
        self.stepRatio = 1.5
        self.acceleration = 1
        self.lastWheelEvent = None
        self.scrollStamps = deque()
        self.stepsLeftQueue = deque()
        self.smoothMoveTimer = QTimer(self)
        self.smoothMode = SmoothMode(SmoothMode.COSINE)
        self.smoothMoveTimer.timeout.connect(self.__smoothMove)

    def setSMoothMode(self, smoothMode):
        """ 设置滚动模式 """
        self.smoothMode = smoothMode

    def wheelEvent(self, e: QWheelEvent):
        """ 实现平滑滚动效果 """
        if self.smoothMode == SmoothMode.NO_SMOOTH or QT_VERSION_STR != '5.13.2':
            super().wheelEvent(e)
            return
            
        # 将当前时间点插入队尾
        now = QDateTime.currentDateTime().toMSecsSinceEpoch()
        self.scrollStamps.append(now)
        while now - self.scrollStamps[0] > 500:
            self.scrollStamps.popleft()
        # 根据未处理完的事件调整移动速率增益
        accerationRatio = min(len(self.scrollStamps) / 15, 1)
        if not self.lastWheelEvent:
            self.lastWheelEvent = QWheelEvent(e)
        else:
            self.lastWheelEvent = e
        # 计算步数
        self.stepsTotal = self.fps * self.duration / 1000
        # 计算每一个事件对应的移动距离
        delta = e.angleDelta().y() * self.stepRatio
        if self.acceleration > 0:
            delta += delta * self.acceleration * accerationRatio
        # 将移动距离和步数组成列表，插入队列等待处理
        self.stepsLeftQueue.append([delta, self.stepsTotal])
        # 定时器的溢出时间t=1000ms/帧数
        self.smoothMoveTimer.start(1000 / self.fps)

    def __smoothMove(self):
        """ 计时器溢出时进行平滑滚动 """
        totalDelta = 0
        # 计算所有未处理完事件的滚动距离，定时器每溢出一次就将步数-1
        for i in self.stepsLeftQueue:
            totalDelta += self.__subDelta(i[0], i[1])
            i[1] -= 1
        # 如果事件已处理完，就将其移出队列
        while self.stepsLeftQueue and self.stepsLeftQueue[0][1] == 0:
            self.stepsLeftQueue.popleft()
        # 构造滚轮事件
        e = QWheelEvent(self.lastWheelEvent.pos(),
                        self.lastWheelEvent.globalPos(),
                        self.lastWheelEvent.pos(),
                        self.lastWheelEvent.globalPos(),
                        round(totalDelta),
                        Qt.Vertical,
                        self.lastWheelEvent.buttons(),
                        Qt.NoModifier)
        # 将构造出来的滚轮事件发送给app处理
        QApplication.sendEvent(self.verticalScrollBar(), e)
        # 如果队列已空，停止滚动
        if not self.stepsLeftQueue:
            self.smoothMoveTimer.stop()

    def __subDelta(self, delta, stepsLeft):
        """ 计算每一步的插值 """
        m = self.stepsTotal / 2
        x = abs(self.stepsTotal - stepsLeft - m)
        # 根据滚动模式计算插值
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
    """ 滚动模式 """
    NO_SMOOTH = 0
    CONSTANT = 1
    LINEAR = 2
    QUADRATI = 3
    COSINE = 4
