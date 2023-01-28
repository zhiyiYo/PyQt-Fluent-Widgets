# coding:utf-8
from typing import List

from PyQt6.QtCore import (QAbstractAnimation, QEasingCurve,
                          QParallelAnimationGroup, QPoint, QPropertyAnimation,
                          pyqtSignal)
from PyQt6.QtWidgets import QGraphicsOpacityEffect, QStackedWidget, QWidget


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


class PopUpAniStackedWidget(QStackedWidget):
    """ Stacked widget with pop up animation """

    aniFinished = pyqtSignal()
    aniStart = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__widgetAni_list = []
        self.__nextIndex = None
        self.__currentAniGroup = None
        self.__previousWidget = None
        self.__previousIndex = 0

    def addWidget(self, widget, deltaX: int = 0, deltaY: int = 22, isNeedOpacityAni=False):
        """ add widget to window

        Parameters
        -----------
        widget:
            widget to be added

        deltaX: int
            the x-axis offset from the beginning to the end of animation

        deltaY: int
            the y-axis offset from the beginning to the end of animation

        isNeedOpacityAni: bool
            need fade in and fade out animation or not
        """
        super().addWidget(widget)

        popUpAni = QPropertyAnimation(widget, b'pos')
        aniGroup = QParallelAnimationGroup(self)
        aniGroup.addAnimation(popUpAni)
        self.__widgetAni_list.append({
            'widget': widget,
            'deltaX': deltaX,
            'deltaY': deltaY,
            'aniGroup': aniGroup,
            'popUpAni': popUpAni,
            'isNeedOpacityAni': isNeedOpacityAni
        })

    def setCurrentIndex(self, index: int, isNeedPopOut: bool = False, isShowNextWidgetDirectly: bool = True,
                        duration: int = 250, easingCurve=QEasingCurve.Type.OutQuad):
        """ set current window to display

        Parameters
        ----------
        index: int
            the index of widget to display

        isNeedPopOut: bool
            need pop up animation or not

        isShowNextWidgetDirectly: bool
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

        if self.__currentAniGroup and self.__currentAniGroup.state() == QAbstractAnimation.State.Running:
            return

        # get the index of widget to be displayed
        self.__nextIndex = index
        self.__previousIndex = self.currentIndex()
        self.__previousWidget = self.currentWidget()

        self.__isNeedPopOut = isNeedPopOut

        # get animation
        nextWidgetAni_dict = self.__widgetAni_list[index]
        currentWidgetAni_dict = self.__widgetAni_list[self.currentIndex()]
        self.__currentWidget = self.currentWidget()  # type:QWidget
        self.__nextWidget = nextWidgetAni_dict['widget']  # type:QWidget
        currentPopUpAni = currentWidgetAni_dict['popUpAni']
        nextPopUpAni = nextWidgetAni_dict['popUpAni']
        self.__isNextWidgetNeedOpAni = nextWidgetAni_dict['isNeedOpacityAni']
        self.__isCurrentWidgetNeedOpAni = currentWidgetAni_dict['isNeedOpacityAni']
        self.__currentAniGroup = currentWidgetAni_dict[
            'aniGroup'] if isNeedPopOut else nextWidgetAni_dict['aniGroup']  # type:QParallelAnimationGroup

        # set opacity animation
        if self.__isNextWidgetNeedOpAni:
            nextOpacityEffect = QGraphicsOpacityEffect(self)
            self.__nextOpacityAni = QPropertyAnimation(
                nextOpacityEffect, b'opacity')
            self.__nextWidget.setGraphicsEffect(nextOpacityEffect)
            self.__currentAniGroup.addAnimation(self.__nextOpacityAni)
            self.__setAnimation(self.__nextOpacityAni, 0, 1, duration)

        if self.__isCurrentWidgetNeedOpAni:
            currentOpacityEffect = QGraphicsOpacityEffect(self)
            self.__currentOpacityAni = QPropertyAnimation(
                currentOpacityEffect, b'opacity')
            self.__currentWidget.setGraphicsEffect(currentOpacityEffect)
            self.__currentAniGroup.addAnimation(self.__currentOpacityAni)
            self.__setAnimation(self.__currentOpacityAni, 1, 0, duration)

        if isNeedPopOut:
            deltaX = currentWidgetAni_dict['deltaX']
            deltaY = currentWidgetAni_dict['deltaY']
            pos = self.__currentWidget.pos() + QPoint(deltaX, deltaY)
            self.__setAnimation(
                currentPopUpAni, self.__currentWidget.pos(), pos, duration, easingCurve)
            self.__nextWidget.setVisible(isShowNextWidgetDirectly)
        else:
            deltaX = nextWidgetAni_dict['deltaX']
            deltaY = nextWidgetAni_dict['deltaY']
            pos = self.__nextWidget.pos() + QPoint(deltaX, deltaY)
            self.__setAnimation(nextPopUpAni, pos,
                                QPoint(self.__nextWidget.x(), self.y()), duration, easingCurve)
            super().setCurrentIndex(index)

        # start animation
        self.__currentAniGroup.finished.connect(self.__aniFinishedSlot)
        self.__currentAniGroup.start()
        self.aniStart.emit()

    def setCurrentWidget(self, widget, isNeedPopOut: bool = False, isShowNextWidgetDirectly: bool = True,
                         duration: int = 250, easingCurve=QEasingCurve.Type.OutQuad):
        """ set currect widget

        Parameters
        ----------
        widget:
            the widget to be displayed

        isNeedPopOut: bool
            need pop up animation or not

        isShowNextWidgetDirectly: bool
            whether to show next widget directly when animation started

        duration: int
            animation duration

        easingCurve: QEasingCurve
            the interpolation mode of animation
        """
        self.setCurrentIndex(self.indexOf(
            widget), isNeedPopOut, isShowNextWidgetDirectly, duration, easingCurve)

    def __setAnimation(self, ani: QPropertyAnimation, startValue, endValue, duration, easingCurve=QEasingCurve.Type.Linear):
        """ set the config of animation """
        ani.setEasingCurve(easingCurve)
        ani.setStartValue(startValue)
        ani.setEndValue(endValue)
        ani.setDuration(duration)

    def __aniFinishedSlot(self):
        """ animation finished slot """
        # cancel previously opacity effects to prevent conflicts with the opacity effects of widgets
        if self.__isCurrentWidgetNeedOpAni:
            self.__currentWidget.setGraphicsEffect(None)
            self.__currentAniGroup.removeAnimation(self.__currentOpacityAni)
        if self.__isNextWidgetNeedOpAni:
            self.__nextWidget.setGraphicsEffect(None)
            self.__currentAniGroup.removeAnimation(self.__nextOpacityAni)

        self.__currentAniGroup.disconnect()
        super().setCurrentIndex(self.__nextIndex)
        self.aniFinished.emit()

    @property
    def previousWidget(self):
        return self.__previousWidget

    @property
    def previousIndex(self):
        return self.__previousIndex
