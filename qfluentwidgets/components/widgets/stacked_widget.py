# coding:utf-8
from enum import Enum
from typing import List

from PyQt6.QtCore import (QAbstractAnimation, QEasingCurve, QPoint, QPropertyAnimation,
                          pyqtSignal, QParallelAnimationGroup, Qt, QSequentialAnimationGroup, QRect)
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QStackedWidget, QWidget, QLabel

from ...common.animation import FluentAnimation


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
                        duration: int = 250, easingCurve=QEasingCurve.Type.OutQuad):
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
            raise Exception(f'The index `{index}` is illegal')

        if index == self.currentIndex():
            return

        if not self.isAnimationEnabled:
            return super().setCurrentIndex(index)

        if self._ani and self._ani.state() == QAbstractAnimation.State.Running:
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
                         duration: int = 250, easingCurve=QEasingCurve.Type.OutQuad):
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

    def __setAnimation(self, ani, startValue, endValue, duration, easingCurve=QEasingCurve.Type.Linear):
        """ set the config of animation """
        ani.setEasingCurve(easingCurve)
        ani.setStartValue(startValue)
        ani.setEndValue(endValue)
        ani.setDuration(duration)

    def __onAniFinished(self):
        """ animation finished slot """
        self._ani.finished.disconnect()
        super().setCurrentIndex(self._nextIndex)
        self.aniFinished.emit()


class TransitionStackedWidget(QStackedWidget):

    aniFinished = pyqtSignal()
    aniStart = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._aniGroup = QParallelAnimationGroup(self)
        self._currentSnapshot = self._createSnapshotLabel()
        self._nextSnapshot = self._createSnapshotLabel()
        self._nextIndex = None
        self._isAnimationEnabled = True

        self._aniGroup.finished.connect(self._onAniFinished)

    def setAnimationEnabled(self, isEnabled: bool):
        """ set whether the transition animation is enabled """
        self._isAnimationEnabled = isEnabled

    def isAnimationEnabled(self) -> bool:
        """ return whether the transition animation is enabled """
        return self._isAnimationEnabled

    def addWidget(self, w):
        w.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        return super().addWidget(w)

    def insertWidget(self, index, w):
        w.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        return super().insertWidget(index, w)

    def setCurrentWidget(self, widget: QWidget, duration: int = None, isBack: bool = False):
        """ set current page widget with transition animation

        Parameters
        ----------
        widget: QWidget
            target widget to display

        duration: int
            animation duration in milliseconds, None for default

        isBack: bool
            whether this is a back navigation
        """
        self.setCurrentIndex(self.indexOf(widget), duration, isBack)

    def setCurrentIndex(self, index: int, duration: int = None, isBack: bool = False):
        """ set current page index with transition animation

        Parameters
        ----------
        index: int
            page index

        duration: int
            animation duration in milliseconds, None for default

        isBack: bool
            whether this is a back navigation
        """
        if index < 0 or index >= self.count():
            return

        if index == self.currentIndex():
            return

        if not self.isAnimationEnabled():
            return super().setCurrentIndex(index)

        self._stopAnimation()

        self._nextIndex = index

        # set up animation properties
        self._setUpTransitionAnimation(index, duration, isBack)

        # start transition animation
        self._aniGroup.start()
        self.aniStart.emit()

    def _setUpTransitionAnimation(self, nextIndex: int, duration: int, isBack: bool):
        """ Set up transition animation """
        raise NotImplementedError

    def _stopAnimation(self):
        """ stop running animation """
        if self._aniGroup.state() != QAbstractAnimation.State.Running:
            return

        self._aniGroup.stop()
        self._onAniFinished()

    def _hideSnapshots(self):
        self._currentSnapshot.hide()
        self._nextSnapshot.hide()

    def _onAniFinished(self):
        self._hideSnapshots()
        super().setCurrentIndex(self._nextIndex)
        self.aniFinished.emit()

    def _createSnapshotLabel(self):
        label = QLabel(self)
        label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        effect = QGraphicsOpacityEffect(label)
        label.setGraphicsEffect(effect)
        label.hide()

        return label

    def _renderSnapshot(self, widget: QWidget, label: QLabel):
        # ensure widget has correct size
        widget.resize(self.size())

        # use grab() which works even when widget is hidden
        pixmap = widget.grab()

        # if grab failed, fallback to render with transparent fill
        if pixmap.isNull() or pixmap.size().isEmpty():
            pixmap = QPixmap(widget.size())
            pixmap.fill(Qt.GlobalColor.transparent)
            widget.render(pixmap)

        label.setPixmap(pixmap)
        label.setGeometry(self.rect())
        label.show()
        label.raise_()


class EntranceTransitionStackedWidget(TransitionStackedWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.outDuration = 150
        self.offset = 140

        self.currentFadeOutAni = QPropertyAnimation(self._currentSnapshot.graphicsEffect(), b'opacity', self)
        self.currentSlideOutAni = QPropertyAnimation(self._currentSnapshot, b'pos', self)
        self.nextSlideInAni = QPropertyAnimation(self, b'pos', self)

        self.nextWidgetAniGroup = QSequentialAnimationGroup(self)

        self._aniGroup.addAnimation(self.nextWidgetAniGroup)

    def _setUpTransitionAnimation(self, nextIndex, duration, isBack):
        inDuration = duration or 300
        inCurve = FluentAnimation.createBezierCurve(0.1, 0.9, 0.2, 1.0)
        outCurve = FluentAnimation.createBezierCurve(0.7, 0.0, 1.0, 0.5)

        currentWidget = self.currentWidget()
        nextWidget = self.widget(nextIndex)

        if currentWidget:
            self._renderSnapshot(currentWidget, self._currentSnapshot)
            currentWidget.hide()

            # fade out current widget
            self.currentFadeOutAni.setDuration(self.outDuration)
            self.currentFadeOutAni.setStartValue(1.0)
            self.currentFadeOutAni.setEndValue(0.0)
            self.currentFadeOutAni.setEasingCurve(outCurve)
            self._aniGroup.addAnimation(self.currentFadeOutAni)

            # slide out current widget
            if isBack:
                self.currentSlideOutAni.setDuration(self.outDuration)
                self.currentSlideOutAni.setStartValue(QPoint(0, 0))
                self.currentSlideOutAni.setEndValue(QPoint(0, self.offset))
                self.currentSlideOutAni.setEasingCurve(outCurve)
                self._aniGroup.addAnimation(self.currentSlideOutAni)

        nextWidget.hide()

        # show next widget after outDuration
        if self.nextWidgetAniGroup.animationCount() > 0:
            self.nextWidgetAniGroup.takeAnimation(0)

        if self.nextWidgetAniGroup.indexOfAnimation(self.nextSlideInAni) >= 0:
            self.nextWidgetAniGroup.removeAnimation(self.nextSlideInAni)

        pauseAni = self.nextWidgetAniGroup.addPause(self.outDuration)
        pauseAni.finished.connect(lambda: nextWidget.show())

        if not isBack:
            # slide in next widget
            self.nextSlideInAni.setTargetObject(nextWidget)
            nextWidget.setGeometry(0, self.offset, self.width(), self.height())
            self.nextSlideInAni.setDuration(inDuration)
            self.nextSlideInAni.setStartValue(QPoint(0, self.offset))
            self.nextSlideInAni.setEndValue(QPoint(0, 0))
            self.nextSlideInAni.setEasingCurve(inCurve)
            self.nextWidgetAniGroup.addAnimation(self.nextSlideInAni)
        else:
            # directly show next widget
            nextWidget.setGeometry(self.rect())


class DrillInTransitionStackedWidget(TransitionStackedWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.currentScaleOutAni = QPropertyAnimation(self._currentSnapshot, b'geometry', self)
        self.currentFadeOutAni = QPropertyAnimation(self._currentSnapshot.graphicsEffect(), b'opacity', self)
        self.nextScaleInAni = QPropertyAnimation(self._nextSnapshot, b'geometry', self)
        self.nextFadeInAni = QPropertyAnimation(self._nextSnapshot.graphicsEffect(), b'opacity', self)

    def _setUpTransitionAnimation(self, nextIndex, duration, isBack):
        scaleCurve = FluentAnimation.createBezierCurve(0.1, 0.9, 0.2, 1.0)
        opacityCurve = FluentAnimation.createBezierCurve(0.17, 0.17, 0.0, 1.0)
        backScaleCurve = FluentAnimation.createBezierCurve(0.12, 0.0, 0.0, 1.0)

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

        currentWidget = self.currentWidget()
        nextWidget = self.widget(nextIndex)
        rect = self.rect()

        if currentWidget:
            self._renderSnapshot(currentWidget, self._currentSnapshot)
            self._currentSnapshot.setScaledContents(True)
            currentWidget.hide()

            # scale out current widget
            outW = int(rect.width() * outScale)
            outH = int(rect.height() * outScale)
            outX = (rect.width() - outW) // 2
            outY = (rect.height() - outH) // 2
            outRect = QRect(outX, outY, outW, outH)

            self.currentScaleOutAni.setDuration(outDuration)
            self.currentScaleOutAni.setStartValue(rect)
            self.currentScaleOutAni.setEndValue(outRect)
            self.currentScaleOutAni.setEasingCurve(scaleCurve)
            self._aniGroup.addAnimation(self.currentScaleOutAni)

            # fade out current widget
            self.currentFadeOutAni.setDuration(outDuration)
            self.currentFadeOutAni.setStartValue(1.0)
            self.currentFadeOutAni.setEndValue(0.0)
            self.currentFadeOutAni.setEasingCurve(opacityCurve)
            self._aniGroup.addAnimation(self.currentFadeOutAni)

        # scale in next widget
        self._renderSnapshot(nextWidget, self._nextSnapshot)
        self._nextSnapshot.setScaledContents(True)
        nextWidget.hide()

        inW = int(rect.width() * inScale)
        inH = int(rect.height() * inScale)
        inX = (rect.width() - inW) // 2
        inY = (rect.height() - inH) // 2
        inRect = QRect(inX, inY, inW, inH)

        self._nextSnapshot.setGeometry(inRect)

        self.nextScaleInAni.setDuration(inDuration)
        self.nextScaleInAni.setStartValue(inRect)
        self.nextScaleInAni.setEndValue(rect)
        self.nextScaleInAni.setEasingCurve(inScaleCurve)
        self._aniGroup.addAnimation(self.nextScaleInAni)

        self.nextFadeInAni.setDuration(inDuration)
        self.nextFadeInAni.setStartValue(0.0)
        self.nextFadeInAni.setEndValue(1.0)
        self.nextFadeInAni.setEasingCurve(opacityCurve)
        self._aniGroup.addAnimation(self.nextFadeInAni)
