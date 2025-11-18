# coding:utf-8
from typing import Optional
from PyQt5.QtCore import QObject, QPropertyAnimation, QEasingCurve, pyqtProperty, pyqtSignal, QRect, Qt
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget

from ...common.config import isDarkTheme
from ...common.style_sheet import themeColor


class NavigationIndicatorAnimator(QObject):
    """ Navigation indicator transition animator """

    animationFinished = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._isEnabled = True
        self._duration = 300
        
        # animation properties
        self._lastSelectMarkTop = 10.0
        self._lastSelectMarkBottom = 10.0
        self._selectMarkTop = 10.0
        self._selectMarkBottom = 10.0
        
        # control flag for display state
        self._isSelectMarkDisplay = True
        
        # tracking widgets
        self._lastSelectedWidget = None  # type: Optional[QWidget]
        self._currentWidget = None  # type: Optional[QWidget]
        
        # animations - moving up
        self._lastSelectMarkTopAni = QPropertyAnimation(self, b'lastSelectMarkTop', self)
        self._selectMarkBottomAni = QPropertyAnimation(self, b'selectMarkBottom', self)
        
        # animations - moving down
        self._lastSelectMarkBottomAni = QPropertyAnimation(self, b'lastSelectMarkBottom', self)
        self._selectMarkTopAni = QPropertyAnimation(self, b'selectMarkTop', self)
        
        self._initAnimations()
        
    def _initAnimations(self):
        """ initialize animations """
        # moving up animations
        self._lastSelectMarkTopAni.setDuration(self._duration)
        self._lastSelectMarkTopAni.setEasingCurve(QEasingCurve.InOutSine)
        self._lastSelectMarkTopAni.valueChanged.connect(lambda: self.parent().update() if self.parent() else None)
        
        self._selectMarkBottomAni.setDuration(self._duration)
        self._selectMarkBottomAni.setEasingCurve(QEasingCurve.InOutSine)
        self._selectMarkBottomAni.valueChanged.connect(lambda: self.parent().update() if self.parent() else None)
        
        # moving down animations
        self._lastSelectMarkBottomAni.setDuration(self._duration)
        self._lastSelectMarkBottomAni.setEasingCurve(QEasingCurve.InOutSine)
        self._lastSelectMarkBottomAni.valueChanged.connect(lambda: self.parent().update() if self.parent() else None)
        
        self._selectMarkTopAni.setDuration(self._duration)
        self._selectMarkTopAni.setEasingCurve(QEasingCurve.InOutSine)
        self._selectMarkTopAni.valueChanged.connect(lambda: self.parent().update() if self.parent() else None)
        
        # chain animations
        self._lastSelectMarkTopAni.finished.connect(self._onLastTopAnimationFinished)
        self._lastSelectMarkBottomAni.finished.connect(self._onLastBottomAnimationFinished)
        
    def _onLastTopAnimationFinished(self):
        """ handle first phase animation finished, start second phase expansion """
        self._isSelectMarkDisplay = True
        self._lastSelectedWidget = None
        self._selectMarkBottomAni.setStartValue(0)
        self._selectMarkBottomAni.setEndValue(10)
        self._selectMarkBottomAni.start()
        self.animationFinished.emit()
        
    def _onLastBottomAnimationFinished(self):
        """ handle first phase animation finished, start second phase expansion """
        self._isSelectMarkDisplay = True
        self._lastSelectedWidget = None
        self._selectMarkTopAni.setStartValue(0)
        self._selectMarkTopAni.setEndValue(10)
        self._selectMarkTopAni.start()
        self.animationFinished.emit()
        
    def isEnabled(self):
        """ check if animation is enabled """
        return self._isEnabled
        
    def setEnabled(self, enabled: bool):
        """ set animation enabled state """
        self._isEnabled = enabled
        
    def duration(self):
        """ get animation duration """
        return self._duration
        
    def setDuration(self, duration: int):
        """ set animation duration """
        self._duration = max(0, duration)
        for ani in [self._lastSelectMarkTopAni, self._lastSelectMarkBottomAni,
                   self._selectMarkTopAni, self._selectMarkBottomAni]:
            ani.setDuration(self._duration)
            
    def animateTo(self, widget: QWidget):
        """ animate indicator to target widget """
        if not self._isEnabled or not widget:
            self._currentWidget = widget
            if self.parent():
                self.parent().update()
            return
        
        # don't animate if clicking the same item
        if widget == self._currentWidget:
            return
            
        # stop running animations
        self._stopAnimations()
        
        # save last selected widget
        self._lastSelectedWidget = self._currentWidget
        
        # reset animation values
        self._lastSelectMarkTop = 10
        self._lastSelectMarkBottom = 10
        self._selectMarkTop = 10
        self._selectMarkBottom = 10
        
        if not self._lastSelectedWidget:
            # no previous widget, just show current
            self._currentWidget = widget
            if self.parent():
                self.parent().update()
            return
            
        # update current widget
        self._currentWidget = widget
        
        # determine animation direction
        if self._isMovingDown():
            # moving down
            self._lastSelectMarkBottomAni.setStartValue(10)
            self._lastSelectMarkBottomAni.setEndValue(0)
            self._lastSelectMarkBottomAni.start()
            # stop other animations
            self._lastSelectMarkTopAni.stop()
            self._selectMarkTopAni.stop()
            # hide select mark until animation finishes
            self._isSelectMarkDisplay = False
        else:
            # moving up
            self._lastSelectMarkTopAni.setStartValue(10)
            self._lastSelectMarkTopAni.setEndValue(0)
            self._lastSelectMarkTopAni.start()
            # stop other animations
            self._lastSelectMarkBottomAni.stop()
            self._selectMarkBottomAni.stop()
            # hide select mark until animation finishes
            self._isSelectMarkDisplay = False
            
    def _isMovingDown(self):
        """ check if indicator is moving down """
        if not self._lastSelectedWidget or not self._currentWidget:
            return True
            
        # Get global positions to compare
        prev_pos = self._lastSelectedWidget.mapToGlobal(self._lastSelectedWidget.rect().topLeft())
        curr_pos = self._currentWidget.mapToGlobal(self._currentWidget.rect().topLeft())
        
        return curr_pos.y() > prev_pos.y()
        
    def _stopAnimations(self):
        """ stop all running animations """
        for ani in [self._lastSelectMarkTopAni, self._lastSelectMarkBottomAni,
                   self._selectMarkTopAni, self._selectMarkBottomAni]:
            if ani.state() == QPropertyAnimation.Running:
                ani.stop()
                
    def drawIndicator(self, painter: QPainter, widget: QWidget, rect: QRect, color: QColor, leftMargin: int = 0):
        """ draw indicator for widget """
        if not widget:
            return
            
        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        
        # calculate indicator x position based on left margin
        indicatorX = rect.x() + leftMargin + 3
        
        # draw current selected indicator
        if self._isSelectMarkDisplay and self._currentWidget == widget:
            indicatorRect = QRect(indicatorX, 
                                 rect.y() + int(self._selectMarkTop),
                                 3, 
                                 rect.height() - int(self._selectMarkTop) - int(self._selectMarkBottom))
            painter.drawRoundedRect(indicatorRect, 1.5, 1.5)
            
        # draw last selected indicator during animation
        if self._lastSelectedWidget == widget:
            indicatorRect = QRect(indicatorX,
                                 rect.y() + int(self._lastSelectMarkTop),
                                 3,
                                 rect.height() - int(self._lastSelectMarkTop) - int(self._lastSelectMarkBottom))
            painter.drawRoundedRect(indicatorRect, 1.5, 1.5)
    
    def reset(self):
        """ reset animator state """
        self._stopAnimations()
        self._lastSelectedWidget = None
        self._currentWidget = None
        self._lastSelectMarkTop = 10
        self._lastSelectMarkBottom = 10
        self._selectMarkTop = 10
        self._selectMarkBottom = 10
        self._isSelectMarkDisplay = True
        
    # properties
    @pyqtProperty(float)
    def lastSelectMarkTop(self):
        return self._lastSelectMarkTop
        
    @lastSelectMarkTop.setter
    def lastSelectMarkTop(self, value):
        self._lastSelectMarkTop = value
        
    @pyqtProperty(float)
    def lastSelectMarkBottom(self):
        return self._lastSelectMarkBottom
        
    @lastSelectMarkBottom.setter
    def lastSelectMarkBottom(self, value):
        self._lastSelectMarkBottom = value
        
    @pyqtProperty(float)
    def selectMarkTop(self):
        return self._selectMarkTop
        
    @selectMarkTop.setter
    def selectMarkTop(self, value):
        self._selectMarkTop = value
        
    @pyqtProperty(float)
    def selectMarkBottom(self):
        return self._selectMarkBottom
        
    @selectMarkBottom.setter  
    def selectMarkBottom(self, value):
        self._selectMarkBottom = value
