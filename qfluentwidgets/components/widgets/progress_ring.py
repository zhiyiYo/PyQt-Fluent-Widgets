# coding:utf-8
from PySide2.QtCore import (Qt, QRectF, QEasingCurve, QPropertyAnimation, QParallelAnimationGroup,
                          QSequentialAnimationGroup, Property)
from PySide2.QtGui import QColor, QPen, QPainter, QFont
from PySide2.QtWidgets import QProgressBar

from .progress_bar import ProgressBar
from ...common.font import setFont
from ...common.style_sheet import themeColor, isDarkTheme


class ProgressRing(ProgressBar):
    """ Progress ring """

    def __init__(self, parent=None, useAni=True):
        super().__init__(parent, useAni=useAni)
        self.lightBackgroundColor = QColor(0, 0, 0, 34)
        self.darkBackgroundColor = QColor(255, 255, 255, 34)
        self._strokeWidth = 6

        self.setTextVisible(False)
        self.setFixedSize(100, 100)
        setFont(self)

    def getStrokeWidth(self):
        return self._strokeWidth

    def setStrokeWidth(self, w: int):
        self._strokeWidth = w
        self.update()

    def _drawText(self, painter: QPainter, text: str):
        """ draw text """
        painter.setFont(self.font())
        painter.setPen(Qt.white if isDarkTheme() else Qt.black)
        painter.drawText(self.rect(), Qt.AlignCenter, text)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        cw = self._strokeWidth    # circle thickness
        w = min(self.height(), self.width()) - cw
        rc = QRectF(cw/2, self.height()/2 - w/2, w, w)

        # draw background
        bc = self.darkBackgroundColor if isDarkTheme() else self.lightBackgroundColor
        pen = QPen(bc, cw, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.drawArc(rc, 0, 360*16)

        if self.maximum() <= self.minimum():
            return

        # draw bar
        pen.setColor(self.barColor())
        painter.setPen(pen)
        degree = int(self.val / (self.maximum() - self.minimum()) * 360)
        painter.drawArc(rc, 90*16, -degree*16)

        # draw text
        if self.isTextVisible():
            self._drawText(painter, self.valText())

    strokeWidth = Property(int, getStrokeWidth, setStrokeWidth)


class IndeterminateProgressRing(QProgressBar):
    """ Indeterminate progress ring """

    def __init__(self, parent=None, start=True):
        super().__init__(parent=parent)
        self.lightBackgroundColor = QColor(0, 0, 0, 0)
        self.darkBackgroundColor = QColor(255, 255, 255, 0)
        self._lightBarColor = QColor()
        self._darkBarColor = QColor()
        self._strokeWidth = 6

        self._startAngle = -180
        self._spanAngle = 0

        self.startAngleAni1 = QPropertyAnimation(self, b'startAngle', self)
        self.startAngleAni2 = QPropertyAnimation(self, b'startAngle', self)
        self.spanAngleAni1 = QPropertyAnimation(self, b'spanAngle', self)
        self.spanAngleAni2 = QPropertyAnimation(self, b'spanAngle', self)

        self.startAngleAniGroup = QSequentialAnimationGroup(self)
        self.spanAngleAniGroup = QSequentialAnimationGroup(self)
        self.aniGroup = QParallelAnimationGroup(self)

        # initialize start angle animation
        self.startAngleAni1.setDuration(1000)
        self.startAngleAni1.setStartValue(0)
        self.startAngleAni1.setEndValue(450)

        self.startAngleAni2.setDuration(1000)
        self.startAngleAni2.setStartValue(450)
        self.startAngleAni2.setEndValue(1080)

        self.startAngleAniGroup.addAnimation(self.startAngleAni1)
        self.startAngleAniGroup.addAnimation(self.startAngleAni2)

        # initialize span angle animation
        self.spanAngleAni1.setDuration(1000)
        self.spanAngleAni1.setStartValue(0)
        self.spanAngleAni1.setEndValue(180)

        self.spanAngleAni2.setDuration(1000)
        self.spanAngleAni2.setStartValue(180)
        self.spanAngleAni2.setEndValue(0)

        self.spanAngleAniGroup.addAnimation(self.spanAngleAni1)
        self.spanAngleAniGroup.addAnimation(self.spanAngleAni2)

        self.aniGroup.addAnimation(self.startAngleAniGroup)
        self.aniGroup.addAnimation(self.spanAngleAniGroup)
        self.aniGroup.setLoopCount(-1)

        self.setFixedSize(80, 80)

        if start:
            self.start()

    @Property(int)
    def startAngle(self):
        return self._startAngle

    @startAngle.setter
    def startAngle(self, angle: int):
        self._startAngle = angle
        self.update()

    @Property(int)
    def spanAngle(self):
        return self._spanAngle

    @spanAngle.setter
    def spanAngle(self, angle: int):
        self._spanAngle = angle
        self.update()

    def getStrokeWidth(self):
        return self._strokeWidth

    def setStrokeWidth(self, w: int):
        self._strokeWidth = w
        self.update()

    def start(self):
        """ start spin """
        self._startAngle = 0
        self._spanAngle = 0
        self.aniGroup.start()

    def stop(self):
        """ stop spin """
        self.aniGroup.stop()
        self.startAngle = 0
        self.spanAngle = 0

    def lightBarColor(self):
        return self._lightBarColor if self._lightBarColor.isValid() else themeColor()

    def darkBarColor(self):
        return self._darkBarColor if self._darkBarColor.isValid() else themeColor()

    def setCustomBarColor(self, light, dark):
        """ set the custom bar color

        Parameters
        ----------
        light, dark: str | Qt.GlobalColor | QColor
            bar color in light/dark theme mode
        """
        self._lightBarColor = QColor(light)
        self._darkBarColor = QColor(dark)
        self.update()

    def setCustomBackgroundColor(self, light, dark):
        """ set the custom background color

        Parameters
        ----------
        light, dark: str | Qt.GlobalColor | QColor
            background color in light/dark theme mode
        """
        self.lightBackgroundColor = QColor(light)
        self.darkBackgroundColor = QColor(dark)
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        cw = self._strokeWidth
        w = min(self.height(), self.width()) - cw
        rc = QRectF(cw/2, self.height()/2 - w/2, w, w)

        # draw background
        bc = self.darkBackgroundColor if isDarkTheme() else self.lightBackgroundColor
        pen = QPen(bc, cw, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin)
        painter.setPen(pen)
        painter.drawArc(rc, 0, 360*16)

        # draw bar
        pen.setColor(self.darkBarColor() if isDarkTheme() else self.lightBarColor())
        painter.setPen(pen)

        startAngle = -self.startAngle + 180
        painter.drawArc(rc, (startAngle % 360)*16, -self.spanAngle*16)

    strokeWidth = Property(int, getStrokeWidth, setStrokeWidth)