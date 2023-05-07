# coding:utf-8
from math import floor

from PyQt5.QtCore import (QEasingCurve, Qt, pyqtSignal, QPropertyAnimation, pyqtProperty,
                          QParallelAnimationGroup, QSequentialAnimationGroup)
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QProgressBar, QWidget

from ...common.style_sheet import themeColor, isDarkTheme



class ProgressBar(QProgressBar):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(4)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        # draw background
        c = 255 if isDarkTheme() else 0
        painter.setPen(QColor(c, c, c, 155))
        y =  floor(self.height() / 2)
        painter.drawLine(0, y, self.width(), y)

        if self.minimum() == self.maximum():
            return

        # draw bar
        painter.setPen(Qt.NoPen)
        painter.setBrush(themeColor())
        w = int(self.value() / (self.maximum() - self.minimum()) * self.width())
        r = self.height() / 2
        painter.drawRoundedRect(0, 0, w, self.height(), r, r)


class IndeterminateProgressBar(QProgressBar):
    """ Indeterminate progress bar """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._shortPos = 0
        self._longPos = 0
        self.shortBarAni = QPropertyAnimation(self, b'shortPos', self)
        self.longBarAni = QPropertyAnimation(self, b'longPos', self)

        self._isError = False

        self.aniGroup = QParallelAnimationGroup(self)
        self.longBarAniGroup = QSequentialAnimationGroup(self)

        self.shortBarAni.setDuration(833)
        self.longBarAni.setDuration(1167)
        self.shortBarAni.setStartValue(0)
        self.longBarAni.setStartValue(0)
        self.shortBarAni.setEndValue(1.45)
        self.longBarAni.setEndValue(1.65)
        self.longBarAni.setEasingCurve(QEasingCurve.OutQuad)

        self.aniGroup.addAnimation(self.shortBarAni)
        self.longBarAniGroup.addPause(785)
        self.longBarAniGroup.addAnimation(self.longBarAni)
        self.aniGroup.addAnimation(self.longBarAniGroup)
        self.aniGroup.setLoopCount(-1)

        self.setFixedHeight(4)

    @pyqtProperty(float)
    def shortPos(self):
        return self._shortPos

    @shortPos.setter
    def shortPos(self, p):
        self._shortPos = p
        self.update()

    @pyqtProperty(float)
    def longPos(self):
        return self._longPos

    @longPos.setter
    def longPos(self, p):
        self._longPos = p
        self.update()

    def showEvent(self, e):
        super().showEvent(e)
        self.start()

    def start(self):
        self.shortPos = 0
        self.longPos = 0
        self.aniGroup.start()
        self.update()

    def pause(self):
        self.aniGroup.pause()
        self.update()

    def resume(self):
        self.aniGroup.resume()
        self.update()

    def setPaused(self, isPaused: bool):
        self.aniGroup.setPaused(isPaused)
        self.update()

    def isPaused(self):
        return self.aniGroup.state() == QParallelAnimationGroup.Paused

    def error(self):
        self._isError = True
        self.aniGroup.stop()
        self.update()

    def setError(self, isError: bool):
        self._isError = isError
        if isError:
            self.error()
        else:
            self.start()

    def isError(self):
        return self._isError

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)

        if self.aniGroup.state() == QPropertyAnimation.Running:
            painter.setBrush(themeColor())
        elif self.aniGroup.state() == QPropertyAnimation.Paused:
            painter.setBrush(
                QColor(252, 225, 0) if isDarkTheme() else QColor(157, 93, 0))
        elif self._isError:
            painter.setBrush(QColor(196, 43, 28))

        # draw short bar
        x = int((self.shortPos - 0.4) * self.width())
        w = int(0.4 * self.width())
        r = self.height() / 2
        painter.drawRoundedRect(x, 0, w, self.height(), r, r)

        # draw long bar
        x = int((self.longPos - 0.6) * self.width())
        w = int(0.6 * self.width())
        r = self.height() / 2
        painter.drawRoundedRect(x, 0, w, self.height(), r, r)
