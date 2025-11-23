# coding:utf-8
from PyQt5.QtCore import (Qt, QPropertyAnimation, QRectF, QEasingCurve, pyqtProperty, 
                          QPointF, QTimer, QAbstractAnimation, QParallelAnimationGroup, 
                          QSequentialAnimationGroup, QSize)
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtWidgets import QWidget

from ...common.style_sheet import themeColor, isDarkTheme
from ...common.color import autoFallbackThemeColor


class NavigationIndicator(QWidget):
    """ Navigation indicator """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.resize(3, 16)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.hide()

        self._opacity = 0.0
        self._geometry = QRectF(0, 0, 3, 16)
        self._isIndicatorAnimationEnabled = True
        self.lightColor = themeColor()
        self.darkColor = themeColor()
        self.isHorizontal = False
        
        self.aniGroup = QParallelAnimationGroup(self)
        self.aniGroup.finished.connect(self.hide)

    def setIndicatorColor(self, light, dark):
        self.lightColor = QColor(light)
        self.darkColor = QColor(dark)
        self.update()

    def setIndicatorAnimationEnabled(self, enabled: bool):
        """ set whether indicator animation is enabled """
        self._isIndicatorAnimationEnabled = enabled

    def getOpacity(self):
        return self._opacity

    def setOpacity(self, opacity):
        self._opacity = opacity
        self.update()

    def getGeometry(self):
        return QRectF(self.geometry())
        
    def setGeometry(self, geometry: QRectF):
        self._geometry = geometry
        super().setGeometry(geometry.toRect())
        
    def getPos(self):
        return QPointF(super().pos())
        
    def setPos(self, pos: QPointF):
        self._geometry.moveTopLeft(pos)
        self.move(pos.toPoint())
        
    def getLength(self):
        return self.width() if self.isHorizontal else self.height()
        
    def setLength(self, length):
        if self.isHorizontal:
            self._geometry.setWidth(length)
            self.resize(int(length), self.height())
        else:
            self._geometry.setHeight(length)
            self.resize(self.width(), int(length))

    opacity = pyqtProperty(float, getOpacity, setOpacity)
    geometry = pyqtProperty(QRectF, getGeometry, setGeometry)
    pos = pyqtProperty(QPointF, getPos, setPos)
    length = pyqtProperty(float, getLength, setLength)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setOpacity(self._opacity)

        color = autoFallbackThemeColor(self.lightColor, self.darkColor)
        painter.setBrush(color)
        
        # Draw filling the widget
        painter.drawRoundedRect(self.rect(), 1.5, 1.5)
        
    def stopAnimation(self):
        self.aniGroup.stop()
        self.aniGroup.clear()

    def animate(self, startRect: QRectF, endRect: QRectF, isHorizontal=False, useCrossFade=False):
        self.stopAnimation()
        self.isHorizontal = isHorizontal
        
        # If animation is disabled, directly set final state
        if not self._isIndicatorAnimationEnabled:
            self.setGeometry(endRect)
            self.setOpacity(1)
            self.show()
            return
        
        # Determine if same level
        if isHorizontal:
            sameLevel = abs(startRect.y() - endRect.y()) < 1
            dim = startRect.width()
            start = startRect.x()
            end = endRect.x()
        else:
            sameLevel = abs(startRect.x() - endRect.x()) < 1
            dim = startRect.height()
            start = startRect.y()
            end = endRect.y()
            
        if sameLevel and not useCrossFade:
            self._startSlideAnimation(startRect, endRect, start, end, dim)
        else:
            self._startCrossFadeAnimation(startRect, endRect)

    def _startSlideAnimation(self, startRect, endRect, from_, to, dimension):
        """ Animate the indicator using WinUI 3 squash and stretch logic

        Key algorithm:
        1. middleScale = abs(to - from) / dimension + (from < to ? endScale : beginScale)
        2. At 33% progress, the indicator stretches to cover the distance between two items
        """
        self.setGeometry(startRect)
        self.setOpacity(1)
        self.show()

        dist = abs(to - from_)
        midLength = dist + dimension
        isForward = to > from_

        s1 = QSequentialAnimationGroup()
        s2 = QSequentialAnimationGroup()

        posAni1 = QPropertyAnimation(self, b"pos")
        posAni1.setDuration(200)
        posAni2 = QPropertyAnimation(self, b"pos")
        posAni2.setDuration(400)

        lenAni1 = QPropertyAnimation(self, b"length")
        lenAni1.setDuration(200)
        lenAni2 = QPropertyAnimation(self, b"length")
        lenAni2.setDuration(400)

        startPos = startRect.topLeft()
        endPos = endRect.topLeft()

        if isForward:
            # 0->0.33: Head moves to B (len increases), Pos stays at A
            posAni1.setStartValue(startPos)
            posAni1.setEndValue(startPos)
            lenAni1.setStartValue(dimension)
            lenAni1.setEndValue(midLength)

            # 0.33->1.0: Tail moves to B (len decreases), Pos moves to B
            posAni2.setStartValue(startPos)
            posAni2.setEndValue(endPos)
            lenAni2.setStartValue(midLength)
            lenAni2.setEndValue(dimension)

        else:
            # 0->0.33: Head moves to A (len increases), Pos moves to B
            # Note: For backward, "Head" is top. Top moves from A to B.
            posAni1.setStartValue(startPos)
            posAni1.setEndValue(endPos)
            lenAni1.setStartValue(dimension)
            lenAni1.setEndValue(midLength)

            # 0.33->1.0: Tail moves to B (len decreases), Pos stays at B
            posAni2.setStartValue(endPos)
            posAni2.setEndValue(endPos)
            lenAni2.setStartValue(midLength)
            lenAni2.setEndValue(dimension)

        # Curves
        curve1 = QEasingCurve(QEasingCurve.BezierSpline)
        curve1.addCubicBezierSegment(QPointF(0.9, 0.1), QPointF(1.0, 0.2), QPointF(1.0, 1.0))

        curve2 = QEasingCurve(QEasingCurve.BezierSpline)
        curve2.addCubicBezierSegment(QPointF(0.1, 0.9), QPointF(0.2, 1.0), QPointF(1.0, 1.0))

        posAni1.setEasingCurve(curve1)
        lenAni1.setEasingCurve(curve1)
        posAni2.setEasingCurve(curve2)
        lenAni2.setEasingCurve(curve2)

        s1.addAnimation(posAni1)
        s1.addAnimation(posAni2)
        s2.addAnimation(lenAni1)
        s2.addAnimation(lenAni2)

        self.aniGroup.addAnimation(s1)
        self.aniGroup.addAnimation(s2)
        self.aniGroup.start()

    def _startCrossFadeAnimation(self, startRect, endRect):
        self.setGeometry(endRect)
        self.setOpacity(1)
        self.show()

        # Determine growth direction based on relative position
        # WinUI 3 logic: Grow from top/bottom edge depending on direction
        isNextBelow = endRect.y() > startRect.y() if not self.isHorizontal else endRect.x() > startRect.x()
        
        if self.isHorizontal:
            dim = endRect.width()
            startGeo = QRectF(endRect.x() + (0 if isNextBelow else dim), endRect.y(), 0, endRect.height())
        else:
            dim = endRect.height()
            startGeo = QRectF(endRect.x(), endRect.y() + (0 if isNextBelow else dim), endRect.width(), 0)

        self.setGeometry(startGeo)

        lenAni = QPropertyAnimation(self, b"length")
        lenAni.setDuration(600)
        lenAni.setStartValue(0)
        lenAni.setEndValue(dim)
        lenAni.setEasingCurve(QEasingCurve.OutQuint)

        posAni = QPropertyAnimation(self, b"pos")
        posAni.setDuration(600)
        posAni.setStartValue(startGeo.topLeft())
        posAni.setEndValue(endRect.topLeft())
        posAni.setEasingCurve(QEasingCurve.OutQuint)

        self.aniGroup.addAnimation(lenAni)
        self.aniGroup.addAnimation(posAni)
        self.aniGroup.start()
