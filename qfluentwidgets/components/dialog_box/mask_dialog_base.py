# coding:utf-8
from PySide2.QtCore import QEasingCurve, QPropertyAnimation, Qt, QEvent, QPoint
from PySide2.QtGui import QColor, QResizeEvent
from PySide2.QtWidgets import (QDialog, QGraphicsDropShadowEffect,
                             QGraphicsOpacityEffect, QHBoxLayout, QWidget, QFrame)

from ...common.config import isDarkTheme


class MaskDialogBase(QDialog):
    """ Dialog box base class with a mask """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._isClosableOnMaskClicked = False
        self._isDraggable = False
        self._dragPos = QPoint()
        self._hBoxLayout = QHBoxLayout(self)
        self.windowMask = QWidget(self)

        # dialog box in the center of mask, all widgets take it as parent
        self.widget = QFrame(self, objectName='centerWidget')
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(0, 0, parent.width(), parent.height())

        c = 0 if isDarkTheme() else 255
        self.windowMask.resize(self.size())
        self.windowMask.setStyleSheet(f'background:rgba({c}, {c}, {c}, 0.6)')
        self._hBoxLayout.addWidget(self.widget)
        self.setShadowEffect()

        self.window().installEventFilter(self)
        self.windowMask.installEventFilter(self)
        self.widget.installEventFilter(self)

    def setShadowEffect(self, blurRadius=60, offset=(0, 10), color=QColor(0, 0, 0, 100)):
        """ add shadow to dialog """
        shadowEffect = QGraphicsDropShadowEffect(self.widget)
        shadowEffect.setBlurRadius(blurRadius)
        shadowEffect.setOffset(*offset)
        shadowEffect.setColor(color)
        self.widget.setGraphicsEffect(None)
        self.widget.setGraphicsEffect(shadowEffect)

    def setMaskColor(self, color: QColor):
        """ set the color of mask """
        self.windowMask.setStyleSheet(f"""
            background: rgba({color.red()}, {color.green()}, {color.blue()}, {color.alpha()})
        """)

    def showEvent(self, e):
        """ fade in """
        opacityEffect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacityEffect)
        opacityAni = QPropertyAnimation(opacityEffect, b'opacity', self)
        opacityAni.setStartValue(0)
        opacityAni.setEndValue(1)
        opacityAni.setDuration(200)
        opacityAni.setEasingCurve(QEasingCurve.InSine)
        opacityAni.finished.connect(lambda: self.setGraphicsEffect(None))
        opacityAni.start()
        super().showEvent(e)

    def done(self, code):
        """ fade out """
        self.widget.setGraphicsEffect(None)
        opacityEffect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacityEffect)
        opacityAni = QPropertyAnimation(opacityEffect, b'opacity', self)
        opacityAni.setStartValue(1)
        opacityAni.setEndValue(0)
        opacityAni.setDuration(100)
        opacityAni.finished.connect(lambda: self._onDone(code))
        opacityAni.start()

    def _onDone(self, code):
        self.setGraphicsEffect(None)
        QDialog.done(self, code)

    def isClosableOnMaskClicked(self):
        return self._isClosableOnMaskClicked

    def setClosableOnMaskClicked(self, isClosable: bool):
        self._isClosableOnMaskClicked = isClosable

    def setDraggable(self, draggable: bool):
        self._isDraggable = draggable

    def isDraggable(self) -> bool:
        return self._isDraggable

    def resizeEvent(self, e):
        self.windowMask.resize(self.size())

    def eventFilter(self, obj, e: QEvent):
        if obj is self.window():
            if e.type() == QEvent.Resize:
                self.resize(e.size())
        elif obj is self.windowMask:
            if e.type() == QEvent.MouseButtonRelease and e.button() == Qt.LeftButton \
                    and self.isClosableOnMaskClicked():
                self.reject()
        elif obj is self.widget and self.isDraggable():
            if e.type() == QEvent.MouseButtonPress and e.button() == Qt.LeftButton:
                if not self.widget.childrenRegion().contains(e.pos()):
                    self._dragPos = e.pos()
                    return True
            elif e.type() == QEvent.MouseMove and not self._dragPos.isNull():
                pos = self.widget.pos() + e.pos() - self._dragPos
                pos.setX(max(0, min(pos.x(), self.width() - self.widget.width())))
                pos.setY(max(0, min(pos.y(), self.height() - self.widget.height())))

                self.widget.move(pos)
                return True
            elif e.type() == QEvent.MouseButtonRelease:
                self._dragPos = QPoint()

        return super().eventFilter(obj, e)
