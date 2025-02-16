# coding:utf-8
from typing import List

from PyQt6.QtCore import (QAbstractAnimation, QEasingCurve, QPoint, QPropertyAnimation,
                          pyqtSignal)
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QStackedWidget, QWidget


class OpacityAniStackedWidget(QStackedWidget):
    """ Stacked widget with fade in and fade out animation """

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.__create_animations()

    def setCurrentIndex(self, index: int) -> None:
        if index == self.currentIndex(): return
        if not self.widget(index): return # avoids going to nonexisting index
        
        # Current index hides, target index shows
        self.currentWidget().setGraphicsEffect(self._opacity1)
        self.widget(index).setGraphicsEffect(self._opacity2)

        # Show target index (currently invisible)
        super().setCurrentIndex(index)

        # Start animations
        self._opacityUp.finished.connect(
            lambda: self.rst_effects(self.currentWidget(), self.widget(index)))
        self._opacityDown.start(QAbstractAnimation.DeletionPolicy.KeepWhenStopped)
        self._opacityUp.start(QAbstractAnimation.DeletionPolicy.KeepWhenStopped)

    def rst_effects(self, w_hidden: QWidget, w_shown: QWidget) -> None:
        w_hidden.setGraphicsEffect(None)
        w_shown.setGraphicsEffect(None)
        self.__create_animations()

    def __create_animations(self) -> None:

        self._opacity1 = QGraphicsOpacityEffect(self)
        self._opacity2 = QGraphicsOpacityEffect(self)
        self._opacity2.setOpacity(0.0)

        ## Animation for both opacities
        self._opacityDown = QPropertyAnimation(self._opacity1, b'opacity')
        self._opacityDown.setStartValue(1.0)
        self._opacityDown.setEndValue(0.0)

        self._opacityUp = QPropertyAnimation(self._opacity2, b'opacity')
        self._opacityUp.setStartValue(0.0)
        self._opacityUp.setEndValue(1.0)

    def setDuration(self, ms: int) -> None:
        """Sets the duration of the transition between widgets"""
        self._opacityUp.setDuration(ms)
        self._opacityDown.setDuration(ms)

    def setCurrentWidget(self, w: QWidget) -> None:
        self.setCurrentIndex(self.indexOf(w))

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
