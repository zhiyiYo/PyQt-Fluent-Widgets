# coding:utf-8
from enum import Enum
from typing import List

from PyQt5.QtCore import (QAbstractAnimation, QEasingCurve, QParallelAnimationGroup,
                          QPoint, QPointF, QPropertyAnimation, QRect, QSequentialAnimationGroup,
                          QSize, pyqtSignal, Qt)
from PyQt5.QtGui import QPixmap, QTransform
from PyQt5.QtWidgets import QApplication, QGraphicsOpacityEffect, QLabel, QStackedWidget, QWidget


class TransitionType(Enum):
    """ Page transition type """
    DEFAULT = 0
    ENTRANCE = 1
    DRILL_IN = 2
    SUPPRESS = 3
    SLIDE_RIGHT = 4
    SLIDE_LEFT = 5


class OpacityAniStackedWidget(QStackedWidget):
    """ Stacked widget with fade in and fade out animation """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__nextIndex = 0
        self.__effects = []  # type:List[QPropertyAnimation]
        self.__anis = []     # type:List[QPropertyAnimation]

    def addWidget(self, w: QWidget):
        super().addWidget(w)

        effect = QGraphicsOpacityEffect(self)
        effect.setOpacity(1)
        ani = QPropertyAnimation(effect, b'opacity', self)
        ani.setDuration(220)
        ani.finished.connect(self.__onAniFinished)
        self.__anis.append(ani)
        self.__effects.append(effect)
        w.setGraphicsEffect(effect)

    def setCurrentIndex(self, index: int):
        index_ = self.currentIndex()
        if index == index_:
            return

        if index > index_:
            ani = self.__anis[index]
            ani.setStartValue(0)
            ani.setEndValue(1)
            super().setCurrentIndex(index)
        else:
            ani = self.__anis[index_]
            ani.setStartValue(1)
            ani.setEndValue(0)

        self.widget(index_).show()
        self.__nextIndex = index
        ani.start()

    def setCurrentWidget(self, w: QWidget):
        self.setCurrentIndex(self.indexOf(w))

    def __onAniFinished(self):
        super().setCurrentIndex(self.__nextIndex)


class PopUpAniInfo:
    """ Pop up ani info """

    def __init__(self, widget: QWidget, deltaX: int, deltaY, ani: QPropertyAnimation):
        self.widget = widget
        self.deltaX = deltaX
        self.deltaY = deltaY
        self.ani = ani


class PopUpAniStackedWidget(QStackedWidget):
    """ Stacked widget with pop up animation """

    aniFinished = pyqtSignal()
    aniStart = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.aniInfos = []  # type: List[PopUpAniInfo]
        self.isAnimationEnabled = True
        self._nextIndex = None
        self._ani = None

    def addWidget(self, widget, deltaX=0, deltaY=76):
        """ add widget to window

        Parameters
        -----------
        widget:
            widget to be added

        deltaX: int
            the x-axis offset from the beginning to the end of animation

        deltaY: int
            the y-axis offset from the beginning to the end of animation
        """
        super().addWidget(widget)

        self.aniInfos.append(PopUpAniInfo(
            widget=widget,
            deltaX=deltaX,
            deltaY=deltaY,
            ani=QPropertyAnimation(widget, b'pos'),
        ))

    def removeWidget(self, widget: QWidget):
        index = self.indexOf(widget)
        if index == -1:
            return

        self.aniInfos.pop(index)
        super().removeWidget(widget)

    def setAnimationEnabled(self, isEnabled: bool):
        """set whether the pop animation is enabled"""
        self.isAnimationEnabled = isEnabled

    def setCurrentIndex(self, index: int, needPopOut: bool = False, showNextWidgetDirectly: bool = True,
                        duration: int = 250, easingCurve=QEasingCurve.OutQuad):
        """ set current window to display

        Parameters
        ----------
        index: int
            the index of widget to display

        isNeedPopOut: bool
            need pop up animation or not

        showNextWidgetDirectly: bool
            whether to show next widget directly when animation started

        duration: int
            animation duration

        easingCurve: QEasingCurve
            the interpolation mode of animation
        """
        if index < 0 or index >= self.count():
            return

        if index == self.currentIndex():
            return

        if not self.isAnimationEnabled:
            return super().setCurrentIndex(index)

        if self._ani and self._ani.state() == QAbstractAnimation.Running:
            self._ani.stop()
            self.__onAniFinished()

        # get the index of widget to be displayed
        self._nextIndex = index

        # get animation
        nextAniInfo = self.aniInfos[index]
        currentAniInfo = self.aniInfos[self.currentIndex()]

        currentWidget = self.currentWidget()
        nextWidget = nextAniInfo.widget
        ani = currentAniInfo.ani if needPopOut else nextAniInfo.ani
        self._ani = ani

        if needPopOut:
            deltaX, deltaY = currentAniInfo.deltaX, currentAniInfo.deltaY
            pos = currentWidget.pos() + QPoint(deltaX, deltaY)
            self.__setAnimation(ani, currentWidget.pos(), pos, duration, easingCurve)
            nextWidget.setVisible(showNextWidgetDirectly)
        else:
            deltaX, deltaY = nextAniInfo.deltaX, nextAniInfo.deltaY
            pos = nextWidget.pos() + QPoint(deltaX, deltaY)
            self.__setAnimation(ani, pos, QPoint(nextWidget.x(), 0), duration, easingCurve)
            super().setCurrentIndex(index)

        # start animation
        ani.finished.connect(self.__onAniFinished)
        ani.start()
        self.aniStart.emit()

    def setCurrentWidget(self, widget, needPopOut: bool = False, showNextWidgetDirectly: bool = True,
                         duration: int = 250, easingCurve=QEasingCurve.OutQuad):
        """ set currect widget

        Parameters
        ----------
        widget:
            the widget to be displayed

        isNeedPopOut: bool
            need pop up animation or not

        showNextWidgetDirectly: bool
            whether to show next widget directly when animation started

        duration: int
            animation duration

        easingCurve: QEasingCurve
            the interpolation mode of animation
        """
        self.setCurrentIndex(
            self.indexOf(widget), needPopOut, showNextWidgetDirectly, duration, easingCurve)

    def __setAnimation(self, ani, startValue, endValue, duration, easingCurve=QEasingCurve.Linear):
        """ set the config of animation """
        ani.setEasingCurve(easingCurve)
        ani.setStartValue(startValue)
        ani.setEndValue(endValue)
        ani.setDuration(duration)

    def __onAniFinished(self):
        """ animation finished slot """
        self._ani.disconnect()
        super().setCurrentIndex(self._nextIndex)
        self.aniFinished.emit()


class _BezierEasingCurve(QEasingCurve):
    """ Custom bezier easing curve """

    def __init__(self, x1: float, y1: float, x2: float, y2: float):
        super().__init__(QEasingCurve.BezierSpline)
        self.addCubicBezierSegment(QPointF(x1, y1), QPointF(x2, y2), QPointF(1, 1))


class TransitionStackedWidget(QStackedWidget):
    """ Stacked widget with WinUI 3 style page transitions """

    aniFinished = pyqtSignal()
    aniStart = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._aniGroup = None
        self._currentSnapshot = None
        self._nextSnapshot = None
        self._defaultTransition = TransitionType.ENTRANCE
        self._isAnimationEnabled = True

    def setAnimationEnabled(self, isEnabled: bool):
        """ set whether the transition animation is enabled """
        self._isAnimationEnabled = isEnabled

    def isAnimationEnabled(self) -> bool:
        """ return whether the transition animation is enabled """
        return self._isAnimationEnabled

    def setDefaultTransition(self, transition: TransitionType):
        """ set the default transition type

        Parameters
        ----------
        transition: TransitionType
            default transition type for page switching
        """
        self._defaultTransition = transition

    def defaultTransition(self) -> TransitionType:
        """ return the default transition type """
        return self._defaultTransition

    def setCurrentIndex(self, index: int, transition: TransitionType = None,
                        duration: int = None, isBack: bool = False):
        """ set current page index with transition animation

        Parameters
        ----------
        index: int
            page index

        transition: TransitionType
            transition animation type, None to use default

        duration: int
            animation duration in milliseconds, None for default

        isBack: bool
            whether this is a back navigation
        """
        if index < 0 or index >= self.count():
            return

        if index == self.currentIndex():
            return

        self._stopAnimation()

        # use default transition if not specified
        if transition is None:
            transition = self._defaultTransition

        # skip animation if disabled or suppressed
        if not self._isAnimationEnabled or transition == TransitionType.SUPPRESS:
            super().setCurrentIndex(index)
            return

        currentWidget = self.currentWidget()
        nextWidget = self.widget(index)

        super().setCurrentIndex(index)

        if currentWidget:
            currentWidget.show()
            currentWidget.raise_()

        nextWidget.show()
        nextWidget.raise_()

        if transition in (TransitionType.DEFAULT, TransitionType.ENTRANCE):
            self._createEntranceAnimation(currentWidget, nextWidget, duration, isBack)
        elif transition == TransitionType.DRILL_IN:
            self._createDrillInAnimation(currentWidget, nextWidget, duration, isBack)
        elif transition == TransitionType.SLIDE_RIGHT:
            self._createSlideAnimation(currentWidget, nextWidget, duration, isBack, fromRight=True)
        elif transition == TransitionType.SLIDE_LEFT:
            self._createSlideAnimation(currentWidget, nextWidget, duration, isBack, fromRight=False)

        if self._aniGroup:
            self._aniGroup.finished.connect(self._onAnimationFinished)
            self._aniGroup.start()
            self.aniStart.emit()

    def setCurrentWidget(self, widget: QWidget, transition: TransitionType = None,
                         duration: int = None, isBack: bool = False):
        """ set current page widget with transition animation

        Parameters
        ----------
        widget: QWidget
            target widget to display

        transition: TransitionType
            transition animation type, None to use default

        duration: int
            animation duration in milliseconds, None for default

        isBack: bool
            whether this is a back navigation
        """
        self.setCurrentIndex(self.indexOf(widget), transition, duration, isBack)

    def _stopAnimation(self):
        """ stop running animation """
        if self._aniGroup and self._aniGroup.state() == QAbstractAnimation.Running:
            self._aniGroup.stop()
            self._cleanupSnapshots()

        self._aniGroup = None

    def _cleanupSnapshots(self):
        """ cleanup snapshot labels """
        if self._currentSnapshot:
            self._currentSnapshot.hide()
            self._currentSnapshot.deleteLater()
            self._currentSnapshot = None

        if self._nextSnapshot:
            self._nextSnapshot.hide()
            self._nextSnapshot.deleteLater()
            self._nextSnapshot = None

    def _renderSnapshot(self, widget: QWidget) -> QLabel:
        """ render widget to a snapshot label

        Parameters
        ----------
        widget: QWidget
            widget to render

        Returns
        -------
        QLabel
            snapshot label with rendered pixmap
        """
        # ensure widget has correct size
        widget.resize(self.size())

        # use grab() which works even when widget is hidden
        pixmap = widget.grab()

        # if grab failed, fallback to render with transparent fill
        if pixmap.isNull() or pixmap.size().isEmpty():
            pixmap = QPixmap(widget.size())
            pixmap.fill(Qt.transparent)
            widget.render(pixmap)

        snapshot = QLabel(self)
        snapshot.setAttribute(Qt.WA_TranslucentBackground)
        snapshot.setPixmap(pixmap)
        snapshot.setGeometry(self.rect())
        snapshot.show()
        snapshot.raise_()

        return snapshot

    def _onAnimationFinished(self):
        """ animation finished handler """
        # ensure current widget is visible and opaque before cleaning up snapshots
        currentWidget = self.currentWidget()
        if currentWidget:
            currentWidget.show()
            effect = currentWidget.graphicsEffect()
            if effect:
                effect.setOpacity(1.0)
            currentWidget.move(0, 0)

        self._cleanupSnapshots()

        for i in range(self.count()):
            if i != self.currentIndex():
                w = self.widget(i)
                if w:
                    w.hide()
                    effect = w.graphicsEffect()
                    if effect:
                        effect.setOpacity(1.0)
                    w.move(0, 0)

        self._aniGroup = None
        self.aniFinished.emit()

    def _createEntranceAnimation(self, currentWidget: QWidget, nextWidget: QWidget,
                                  duration: int, isBack: bool):
        """ create entrance transition animation using snapshots

        WinUI 3 Parameters:
        - translationOffset: 140px
        - outDuration: 150ms, inDuration: 300ms
        - inCurve: cubic-bezier(0.1, 0.9, 0.2, 1.0)
        - outCurve: cubic-bezier(0.7, 0.0, 1.0, 0.5)
        - opacity: discrete change at outDuration
        """
        offset = 140
        outDuration = 150
        inDuration = duration or 300
        inCurve = _BezierEasingCurve(0.1, 0.9, 0.2, 1.0)
        outCurve = _BezierEasingCurve(0.7, 0.0, 1.0, 0.5)
        rect = self.rect()

        self._aniGroup = QParallelAnimationGroup(self)

        # create snapshot for currentWidget
        if currentWidget:
            self._currentSnapshot = self._renderSnapshot(currentWidget)
            currentWidget.hide()

            currentEffect = QGraphicsOpacityEffect(self._currentSnapshot)
            self._currentSnapshot.setGraphicsEffect(currentEffect)

            fadeOut = QPropertyAnimation(currentEffect, b'opacity', self)
            fadeOut.setDuration(outDuration)
            fadeOut.setStartValue(1.0)
            fadeOut.setEndValue(0.0)
            fadeOut.setEasingCurve(outCurve)
            self._aniGroup.addAnimation(fadeOut)

            if isBack:
                slideOut = QPropertyAnimation(self._currentSnapshot, b'pos', self)
                slideOut.setDuration(outDuration)
                slideOut.setStartValue(QPoint(0, 0))
                slideOut.setEndValue(QPoint(0, offset))
                slideOut.setEasingCurve(outCurve)
                self._aniGroup.addAnimation(slideOut)

        # create snapshot for nextWidget
        self._nextSnapshot = self._renderSnapshot(nextWidget)
        nextWidget.hide()

        nextEffect = QGraphicsOpacityEffect(self._nextSnapshot)
        self._nextSnapshot.setGraphicsEffect(nextEffect)
        nextEffect.setOpacity(0.0)

        # discrete opacity: invisible during outDuration, then instantly visible
        opacitySeq = QSequentialAnimationGroup(self)
        waitAni = QPropertyAnimation(nextEffect, b'opacity', self)
        waitAni.setDuration(outDuration)
        waitAni.setStartValue(0.0)
        waitAni.setEndValue(0.0)
        opacitySeq.addAnimation(waitAni)

        showAni = QPropertyAnimation(nextEffect, b'opacity', self)
        showAni.setDuration(1)
        showAni.setStartValue(1.0)
        showAni.setEndValue(1.0)
        opacitySeq.addAnimation(showAni)
        self._aniGroup.addAnimation(opacitySeq)

        if not isBack:
            self._nextSnapshot.move(0, offset)

            # position: wait during outDuration, then slide with inCurve
            posSeq = QSequentialAnimationGroup(self)

            waitPos = QPropertyAnimation(self._nextSnapshot, b'pos', self)
            waitPos.setDuration(outDuration)
            waitPos.setStartValue(QPoint(0, offset))
            waitPos.setEndValue(QPoint(0, offset))
            posSeq.addAnimation(waitPos)

            slideIn = QPropertyAnimation(self._nextSnapshot, b'pos', self)
            slideIn.setDuration(inDuration)
            slideIn.setStartValue(QPoint(0, offset))
            slideIn.setEndValue(QPoint(0, 0))
            slideIn.setEasingCurve(inCurve)
            posSeq.addAnimation(slideIn)

            self._aniGroup.addAnimation(posSeq)
        else:
            self._nextSnapshot.setGeometry(rect)

    def _createDrillInAnimation(self, currentWidget: QWidget, nextWidget: QWidget,
                                 duration: int, isBack: bool):
        """ create drill-in transition animation using snapshots

        WinUI 3 Parameters:
        NavigatingTo: scale 0.94->1.0, 783ms scale, 333ms opacity
        NavigatingAway: scale 1.0->1.04, 100ms
        BackNavigatingTo: scale 1.06->1.0, 333ms
        BackNavigatingAway: scale 1.0->0.96, 100ms
        """
        scaleCurve = _BezierEasingCurve(0.1, 0.9, 0.2, 1.0)
        opacityCurve = _BezierEasingCurve(0.17, 0.17, 0.0, 1.0)
        backScaleCurve = _BezierEasingCurve(0.12, 0.0, 0.0, 1.0)

        self._aniGroup = QParallelAnimationGroup(self)
        rect = self.rect()

        if isBack:
            inScale = 1.06
            outScale = 0.96
            inDuration = duration or 333
            outDuration = 100
            inScaleCurve = backScaleCurve
        else:
            inScale = 0.94
            outScale = 1.04
            # shortened from 783ms to 333ms for better responsiveness
            inDuration = duration or 333
            outDuration = 100
            inScaleCurve = scaleCurve

        opacityDuration = inDuration

        if currentWidget:
            self._currentSnapshot = self._renderSnapshot(currentWidget)
            self._currentSnapshot.setScaledContents(True)
            currentWidget.hide()

            outW = int(rect.width() * outScale)
            outH = int(rect.height() * outScale)
            outX = (rect.width() - outW) // 2
            outY = (rect.height() - outH) // 2
            outRect = QRect(outX, outY, outW, outH)

            scaleOut = QPropertyAnimation(self._currentSnapshot, b'geometry', self)
            scaleOut.setDuration(outDuration)
            scaleOut.setStartValue(rect)
            scaleOut.setEndValue(outRect)
            scaleOut.setEasingCurve(scaleCurve)
            self._aniGroup.addAnimation(scaleOut)

            outEffect = QGraphicsOpacityEffect(self._currentSnapshot)
            self._currentSnapshot.setGraphicsEffect(outEffect)
            fadeOut = QPropertyAnimation(outEffect, b'opacity', self)
            fadeOut.setDuration(outDuration)
            fadeOut.setStartValue(1.0)
            fadeOut.setEndValue(0.0)
            fadeOut.setEasingCurve(opacityCurve)
            self._aniGroup.addAnimation(fadeOut)

        self._nextSnapshot = self._renderSnapshot(nextWidget)
        self._nextSnapshot.setScaledContents(True)
        nextWidget.hide()

        inW = int(rect.width() * inScale)
        inH = int(rect.height() * inScale)
        inX = (rect.width() - inW) // 2
        inY = (rect.height() - inH) // 2
        inRect = QRect(inX, inY, inW, inH)

        self._nextSnapshot.setGeometry(inRect)

        scaleIn = QPropertyAnimation(self._nextSnapshot, b'geometry', self)
        scaleIn.setDuration(inDuration)
        scaleIn.setStartValue(inRect)
        scaleIn.setEndValue(rect)
        scaleIn.setEasingCurve(inScaleCurve)
        self._aniGroup.addAnimation(scaleIn)

        inEffect = QGraphicsOpacityEffect(self._nextSnapshot)
        self._nextSnapshot.setGraphicsEffect(inEffect)
        inEffect.setOpacity(0.0)
        fadeIn = QPropertyAnimation(inEffect, b'opacity', self)
        fadeIn.setDuration(opacityDuration)
        fadeIn.setStartValue(0.0)
        fadeIn.setEndValue(1.0)
        fadeIn.setEasingCurve(opacityCurve)
        self._aniGroup.addAnimation(fadeIn)

    def _createSlideAnimation(self, currentWidget: QWidget, nextWidget: QWidget,
                               duration: int, isBack: bool, fromRight: bool):
        """ create slide transition animation using snapshots

        WinUI 3 Parameters:
        - exitOffset: 150px, entranceOffset: 200px
        - outDuration: 150ms, inDuration: 300ms
        - inCurve: cubic-bezier(0.1, 0.9, 0.2, 1.0)
        - outCurve: cubic-bezier(0.7, 0.0, 1.0, 0.5)
        - opacity: discrete change at outDuration
        """
        exitOffset = 150
        entranceOffset = 200
        outDuration = 150
        inDuration = duration or 300
        inCurve = _BezierEasingCurve(0.1, 0.9, 0.2, 1.0)
        outCurve = _BezierEasingCurve(0.7, 0.0, 1.0, 0.5)
        rect = self.rect()

        # direction factor: FromRight=-1, FromLeft=1
        factor = -1 if fromRight else 1

        self._aniGroup = QParallelAnimationGroup(self)

        # calculate slide positions based on WinUI 3 exact behavior
        if isBack:
            # BackNavigatingAway: slide to entranceOffset * factor
            # BackNavigatingTo: slide from exitOffset * factor
            slideOutEnd = int(entranceOffset * factor)
            slideInStart = int(exitOffset * factor)
        else:
            # NavigatingAway: slide to exitOffset * factor
            # NavigatingTo: slide from entranceOffset * factor (negative = opposite side)
            slideOutEnd = int(exitOffset * factor)
            slideInStart = int(-entranceOffset * factor)

        # create snapshot for currentWidget
        if currentWidget:
            self._currentSnapshot = self._renderSnapshot(currentWidget)
            currentWidget.hide()

            currentEffect = QGraphicsOpacityEffect(self._currentSnapshot)
            self._currentSnapshot.setGraphicsEffect(currentEffect)

            # discrete opacity: visible until outDuration, then instantly hidden
            fadeOutSeq = QSequentialAnimationGroup(self)
            holdVisible = QPropertyAnimation(currentEffect, b'opacity', self)
            holdVisible.setDuration(outDuration - 1)
            holdVisible.setStartValue(1.0)
            holdVisible.setEndValue(1.0)
            fadeOutSeq.addAnimation(holdVisible)

            hideAni = QPropertyAnimation(currentEffect, b'opacity', self)
            hideAni.setDuration(1)
            hideAni.setStartValue(0.0)
            hideAni.setEndValue(0.0)
            fadeOutSeq.addAnimation(hideAni)
            self._aniGroup.addAnimation(fadeOutSeq)

            slideOut = QPropertyAnimation(self._currentSnapshot, b'pos', self)
            slideOut.setDuration(outDuration)
            slideOut.setStartValue(QPoint(0, 0))
            slideOut.setEndValue(QPoint(slideOutEnd, 0))
            slideOut.setEasingCurve(outCurve)
            self._aniGroup.addAnimation(slideOut)

        # create snapshot for nextWidget
        self._nextSnapshot = self._renderSnapshot(nextWidget)
        nextWidget.hide()

        nextEffect = QGraphicsOpacityEffect(self._nextSnapshot)
        self._nextSnapshot.setGraphicsEffect(nextEffect)
        nextEffect.setOpacity(0.0)

        # discrete opacity: invisible during outDuration, then instantly visible
        opacitySeq = QSequentialAnimationGroup(self)
        waitAni = QPropertyAnimation(nextEffect, b'opacity', self)
        waitAni.setDuration(outDuration)
        waitAni.setStartValue(0.0)
        waitAni.setEndValue(0.0)
        opacitySeq.addAnimation(waitAni)

        showAni = QPropertyAnimation(nextEffect, b'opacity', self)
        showAni.setDuration(1)
        showAni.setStartValue(1.0)
        showAni.setEndValue(1.0)
        opacitySeq.addAnimation(showAni)
        self._aniGroup.addAnimation(opacitySeq)

        self._nextSnapshot.move(slideInStart, 0)

        # position: wait during outDuration, then slide with inCurve
        posSeq = QSequentialAnimationGroup(self)

        waitPos = QPropertyAnimation(self._nextSnapshot, b'pos', self)
        waitPos.setDuration(outDuration)
        waitPos.setStartValue(QPoint(slideInStart, 0))
        waitPos.setEndValue(QPoint(slideInStart, 0))
        posSeq.addAnimation(waitPos)

        slideIn = QPropertyAnimation(self._nextSnapshot, b'pos', self)
        slideIn.setDuration(inDuration)
        slideIn.setStartValue(QPoint(slideInStart, 0))
        slideIn.setEndValue(QPoint(0, 0))
        slideIn.setEasingCurve(inCurve)
        posSeq.addAnimation(slideIn)

        self._aniGroup.addAnimation(posSeq)
