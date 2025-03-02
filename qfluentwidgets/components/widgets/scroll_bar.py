# coding:utf-8
from PySide6.QtCore import (QEvent, QEasingCurve, Qt, Signal, QPropertyAnimation, Property, QRectF,
                          QTimer, QPoint, QObject)
from PySide6.QtGui import QPainter, QColor, QMouseEvent
from PySide6.QtWidgets import (QWidget, QToolButton, QAbstractScrollArea, QGraphicsOpacityEffect,
                             QHBoxLayout, QVBoxLayout, QApplication, QAbstractItemView, QListView)

from ...common.icon import FluentIcon
from ...common.style_sheet import isDarkTheme
from ...common.smooth_scroll import SmoothScroll

class ArrowButton(QToolButton):
    """ Arrow button """

    def __init__(self, icon: FluentIcon, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(10, 10)
        self._icon = icon
        self.opacity = 1

    def setOpacity(self, opacity):
        self.opacity = opacity
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setOpacity(self.opacity)

        s = 7 if self.isDown() else 8
        x = (self.width() - s) / 2
        self._icon.render(painter, QRectF(x, x, s, s), fill="#858789")


class ScrollBarGroove(QWidget):
    """ Scroll bar groove """

    def __init__(self, orient: Qt.Orientation, parent):
        super().__init__(parent=parent)
        self._opacity = 1

        if orient == Qt.Vertical:
            self.setFixedWidth(12)
            self.upButton = ArrowButton(FluentIcon.CARE_UP_SOLID, self)
            self.downButton = ArrowButton(FluentIcon.CARE_DOWN_SOLID, self)
            self.setLayout(QVBoxLayout(self))
            self.layout().addWidget(self.upButton, 0, Qt.AlignHCenter)
            self.layout().addStretch(1)
            self.layout().addWidget(self.downButton, 0, Qt.AlignHCenter)
            self.layout().setContentsMargins(0, 3, 0, 3)
        else:
            self.setFixedHeight(12)
            self.upButton = ArrowButton(FluentIcon.CARE_LEFT_SOLID, self)
            self.downButton = ArrowButton(FluentIcon.CARE_RIGHT_SOLID, self)
            self.setLayout(QHBoxLayout(self))
            self.layout().addWidget(self.upButton, 0, Qt.AlignVCenter)
            self.layout().addStretch(1)
            self.layout().addWidget(self.downButton, 0, Qt.AlignVCenter)
            self.layout().setContentsMargins(3, 0, 3, 0)

        self.opacityAni = QPropertyAnimation(self, b'opacity', self)
        self.setOpacity(0)

    def fadeIn(self):
        self.opacityAni.stop()
        self.opacityAni.setStartValue(self.opacity)
        self.opacityAni.setEndValue(1)
        self.opacityAni.setDuration(150)
        self.opacityAni.start()

    def fadeOut(self):
        self.opacityAni.stop()
        self.opacityAni.setStartValue(self.opacity)
        self.opacityAni.setEndValue(0)
        self.opacityAni.setDuration(150)
        self.opacityAni.start()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setOpacity(self.opacity)
        painter.setPen(Qt.NoPen)

        if not isDarkTheme():
            painter.setBrush(QColor(252, 252, 252, 217))
        else:
            painter.setBrush(QColor(44, 44, 44, 245))

        painter.drawRoundedRect(self.rect(), 6, 6)

    def setOpacity(self, opacity: float):
        self._opacity = opacity
        self.upButton.setOpacity(opacity)
        self.downButton.setOpacity(opacity)
        self.update()

    def getOpacity(self) -> float:
        return self._opacity

    opacity = Property(float, getOpacity, setOpacity)


class ScrollBarHandle(QWidget):
    """ Scroll bar handle """

    def __init__(self, orient: Qt.Orientation, parent=None):
        super().__init__(parent)
        self.orient = orient
        if orient == Qt.Vertical:
            self.setFixedWidth(3)
        else:
            self.setFixedHeight(3)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        r = self.width() / 2 if self.orient == Qt.Vertical else self.height() / 2
        c = QColor(255, 255, 255, 139) if isDarkTheme() else QColor(0, 0, 0, 114)
        painter.setBrush(c)
        painter.drawRoundedRect(self.rect(), r, r)


class ScrollBar(QWidget):
    """ Fluent scroll bar """

    rangeChanged = Signal(tuple)
    valueChanged = Signal(int)
    sliderPressed = Signal()
    sliderReleased = Signal()
    sliderMoved = Signal()

    def __init__(self, orient: Qt.Orientation, parent: QAbstractScrollArea):
        super().__init__(parent)
        self.groove = ScrollBarGroove(orient, self)
        self.handle = ScrollBarHandle(orient, self)
        self.timer = QTimer(self)

        self._orientation = orient
        self._singleStep = 1
        self._pageStep = 50
        self._padding = 14

        self._minimum = 0
        self._maximum = 0
        self._value = 0

        self._isPressed = False
        self._isEnter = False
        self._isExpanded = False
        self._pressedPos = QPoint()
        self._isForceHidden = False

        if orient == Qt.Vertical:
            self.partnerBar = parent.verticalScrollBar()
            QAbstractScrollArea.setVerticalScrollBarPolicy(parent, Qt.ScrollBarAlwaysOff)
        else:
            self.partnerBar = parent.horizontalScrollBar()
            QAbstractScrollArea.setHorizontalScrollBarPolicy(parent, Qt.ScrollBarAlwaysOff)

        self.__initWidget(parent)

    def __initWidget(self, parent):
        self.groove.upButton.clicked.connect(self._onPageUp)
        self.groove.downButton.clicked.connect(self._onPageDown)
        self.groove.opacityAni.valueChanged.connect(self._onOpacityAniValueChanged)

        self.partnerBar.rangeChanged.connect(self.setRange)
        self.partnerBar.valueChanged.connect(self._onValueChanged)
        self.valueChanged.connect(self.partnerBar.setValue)

        parent.installEventFilter(self)

        self.setRange(self.partnerBar.minimum(), self.partnerBar.maximum())
        self.setVisible(self.maximum() > 0 and not self._isForceHidden)
        self._adjustPos(self.parent().size())

    def _onPageUp(self):
        self.setValue(self.value() - self.pageStep())

    def _onPageDown(self):
        self.setValue(self.value() + self.pageStep())

    def _onValueChanged(self, value):
        self.val = value

    def value(self):
        return self._value

    @Property(int, notify=valueChanged)
    def val(self):
        return self._value

    @val.setter
    def val(self, value: int):
        if value == self.value():
            return

        value = max(self.minimum(), min(value, self.maximum()))
        self._value = value
        self.valueChanged.emit(value)

        # adjust the position of handle
        self._adjustHandlePos()

    def minimum(self):
        return self._minimum

    def maximum(self):
        return self._maximum

    def orientation(self):
        return self._orientation

    def pageStep(self):
        return self._pageStep

    def singleStep(self):
        return self._singleStep

    def isSliderDown(self):
        return self._isPressed

    def setValue(self, value: int):
        self.val = value

    def setMinimum(self, min: int):
        if min == self.minimum():
            return

        self._minimum = min
        self.rangeChanged.emit((min, self.maximum()))

    def setMaximum(self, max: int):
        if max == self.maximum():
            return

        self._maximum = max
        self.rangeChanged.emit((self.minimum(), max))

    def setRange(self, min: int, max: int):
        if min > max or (min == self.minimum() and max == self.maximum()):
            return

        self.setMinimum(min)
        self.setMaximum(max)

        self._adjustHandleSize()
        self._adjustHandlePos()
        self.setVisible(max > 0 and not self._isForceHidden)

        self.rangeChanged.emit((min, max))

    def setPageStep(self, step: int):
        if step >= 1:
            self._pageStep = step

    def setSingleStep(self, step: int):
        if step >= 1:
            self._singleStep = step

    def setSliderDown(self, isDown: bool):
        self._isPressed = True
        if isDown:
            self.sliderPressed.emit()
        else:
            self.sliderReleased.emit()

    def expand(self):
        """ expand scroll bar """
        if self._isExpanded or not self.isEnter:
            return

        self._isExpanded = True
        self.groove.fadeIn()

    def collapse(self):
        """ collapse scroll bar """
        if not self._isExpanded or self.isEnter:
            return

        self._isExpanded = False
        self.groove.fadeOut()

    def enterEvent(self, e):
        self.isEnter = True
        self.timer.stop()
        self.timer.singleShot(200, self.expand)

    def leaveEvent(self, e):
        self.isEnter = False
        self.timer.stop()
        self.timer.singleShot(200, self.collapse)

    def eventFilter(self, obj, e: QEvent):
        if obj is not self.parent():
            return super().eventFilter(obj, e)

        # adjust the position of slider
        if e.type() == QEvent.Resize:
            self._adjustPos(e.size())

        return super().eventFilter(obj, e)

    def resizeEvent(self, e):
        self.groove.resize(self.size())

    def mousePressEvent(self, e: QMouseEvent):
        super().mousePressEvent(e)
        self._isPressed = True
        self._pressedPos = e.pos()

        if self.childAt(e.pos()) is self.handle or not self._isSlideResion(e.pos()):
            return

        if self.orientation() == Qt.Vertical:
            if e.pos().y() > self.handle.geometry().bottom():
                value = e.pos().y() - self.handle.height() - self._padding
            else:
                value = e.pos().y() - self._padding
        else:
            if e.pos().x() > self.handle.geometry().right():
                value = e.pos().x() - self.handle.width() - self._padding
            else:
                value = e.pos().x() - self._padding

        self.setValue(int(value / max(self._slideLength(), 1) * self.maximum()))
        self.sliderPressed.emit()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self._isPressed = False
        self.sliderReleased.emit()

    def mouseMoveEvent(self, e: QMouseEvent):
        if self.orientation() == Qt.Vertical:
            dv = e.pos().y() - self._pressedPos.y()
        else:
            dv = e.pos().x() - self._pressedPos.x()

        # don't use `self.setValue()`, because it could be reimplemented
        dv = int(dv / max(self._slideLength(), 1) * (self.maximum() - self.minimum()))
        ScrollBar.setValue(self, self.value() + dv)

        self._pressedPos = e.pos()
        self.sliderMoved.emit()

    def _adjustPos(self, size):
        if self.orientation() == Qt.Vertical:
            self.resize(12, size.height() - 2)
            self.move(size.width() - 13, 1)
        else:
            self.resize(size.width() - 2, 12)
            self.move(1, size.height() - 13)

    def _adjustHandleSize(self):
        p = self.parent()
        if self.orientation() == Qt.Vertical:
            total = self.maximum() - self.minimum() + p.height()
            s = int(self._grooveLength() * p.height() / max(total, 1))
            self.handle.setFixedHeight(max(30, s))
        else:
            total = self.maximum() - self.minimum() + p.width()
            s = int(self._grooveLength() * p.width() / max(total, 1))
            self.handle.setFixedWidth(max(30, s))

    def _adjustHandlePos(self):
        total = max(self.maximum() - self.minimum(), 1)
        delta = int(self.value() / total * self._slideLength())

        if self.orientation() == Qt.Vertical:
            x = self.width() - self.handle.width() - 3
            self.handle.move(x, self._padding + delta)
        else:
            y = self.height() - self.handle.height() - 3
            self.handle.move(self._padding + delta, y)

    def _grooveLength(self):
        if self.orientation() == Qt.Vertical:
            return self.height() - 2 * self._padding

        return self.width() - 2 * self._padding

    def _slideLength(self):
        if self.orientation() == Qt.Vertical:
            return self._grooveLength() - self.handle.height()

        return self._grooveLength() - self.handle.width()

    def _isSlideResion(self, pos: QPoint):
        if self.orientation() == Qt.Vertical:
            return self._padding <= pos.y() <= self.height() - self._padding

        return self._padding <= pos.x() <= self.width() - self._padding

    def _onOpacityAniValueChanged(self):
        opacity = self.groove.opacity
        if self.orientation() == Qt.Vertical:
            self.handle.setFixedWidth(int(3 + opacity * 3))
        else:
            self.handle.setFixedHeight(int(3 + opacity * 3))

        self._adjustHandlePos()

    def setForceHidden(self, isHidden: bool):
        """ whether to force the scrollbar to be hidden """
        self._isForceHidden = isHidden
        self.setVisible(self.maximum() > 0 and not isHidden)

    def wheelEvent(self, e):
        QApplication.sendEvent(self.parent().viewport(), e)


class SmoothScrollBar(ScrollBar):
    """ Smooth scroll bar """

    def __init__(self, orient: Qt.Orientation, parent):
        super().__init__(orient, parent)
        self.duration = 500
        self.ani = QPropertyAnimation()
        self.ani.setTargetObject(self)
        self.ani.setPropertyName(b"val")
        self.ani.setEasingCurve(QEasingCurve.OutCubic)
        self.ani.setDuration(self.duration)

        self.__value = self.value()

    def setValue(self, value, useAni=True):
        if value == self.value():
            return

        # stop running animation
        self.ani.stop()

        if not useAni:
            self.val = value
            return

        # adjust the duration
        dv = abs(value - self.value())
        if dv < 50:
            self.ani.setDuration(int(self.duration * dv / 70))
        else:
            self.ani.setDuration(self.duration)

        self.ani.setStartValue(self.value())
        self.ani.setEndValue(value)
        self.ani.start()

    def scrollValue(self, value, useAni=True):
        """ scroll the specified distance """
        self.__value += value
        self.__value = max(self.minimum(), self.__value)
        self.__value = min(self.maximum(), self.__value)
        self.setValue(self.__value, useAni)

    def scrollTo(self, value, useAni=True):
        """ scroll to the specified position """
        self.__value = value
        self.__value = max(self.minimum(), self.__value)
        self.__value = min(self.maximum(), self.__value)
        self.setValue(self.__value, useAni)

    def resetValue(self, value):
        self.__value = value

    def mousePressEvent(self, e):
        self.ani.stop()
        super().mousePressEvent(e)
        self.__value = self.value()

    def mouseMoveEvent(self, e):
        self.ani.stop()
        super().mouseMoveEvent(e)
        self.__value = self.value()

    def setScrollAnimation(self, duration, easing=QEasingCurve.OutCubic):
        """ set scroll animation

        Parameters
        ----------
        duration: int
            scroll duration

        easing: QEasingCurve
            animation type
        """
        self.duration = duration
        self.ani.setDuration(duration)
        self.ani.setEasingCurve(easing)


class SmoothScrollDelegate(QObject):
    """ Smooth scroll delegate """

    def __init__(self, parent: QAbstractScrollArea, useAni=False):
        """
        Parameters
        ----------
        parent: QAbstractScrollArea
            the scrolling area being delegated

        useAni: bool
            whether to use `QPropertyAnimation` to achieve smooth scrolling
        """
        super().__init__(parent)
        self.useAni = useAni
        self.vScrollBar = SmoothScrollBar(Qt.Vertical, parent)
        self.hScrollBar = SmoothScrollBar(Qt.Horizontal, parent)
        self.verticalSmoothScroll = SmoothScroll(parent, Qt.Vertical)
        self.horizonSmoothScroll = SmoothScroll(parent, Qt.Horizontal)

        if isinstance(parent, QAbstractItemView):
            parent.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
            parent.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        if isinstance(parent, QListView):
            parent.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
            parent.horizontalScrollBar().setStyleSheet("QScrollBar:horizontal{height: 0px}")

        parent.viewport().installEventFilter(self)
        parent.setVerticalScrollBarPolicy = self.setVerticalScrollBarPolicy
        parent.setHorizontalScrollBarPolicy = self.setHorizontalScrollBarPolicy

    def eventFilter(self, obj, e: QEvent):
        if e.type() == QEvent.Type.Wheel:
            # Check if the vertical scroll is at its limit
            verticalAtEnd = (e.angleDelta().y() < 0 and self.vScrollBar.value() == self.vScrollBar.maximum()) or \
                            (e.angleDelta().y() > 0 and self.vScrollBar.value() == self.vScrollBar.minimum())

            # Check if the horizontal scroll is at its limit
            horizontalAtEnd = (e.angleDelta().x() < 0 and self.hScrollBar.value() == self.hScrollBar.maximum()) or \
                              (e.angleDelta().x() > 0 and self.hScrollBar.value() == self.hScrollBar.minimum())

            if verticalAtEnd or horizontalAtEnd:
                return False

            if e.angleDelta().y() != 0:
                if not self.useAni:
                    self.verticalSmoothScroll.wheelEvent(e)
                else:
                    self.vScrollBar.scrollValue(-e.angleDelta().y())
            else:
                if not self.useAni:
                    self.horizonSmoothScroll.wheelEvent(e)
                else:
                    self.hScrollBar.scrollValue(-e.angleDelta().x())

            e.setAccepted(True)
            return True

        return super().eventFilter(obj, e)

    def setVerticalScrollBarPolicy(self, policy):
        QAbstractScrollArea.setVerticalScrollBarPolicy(self.parent(), Qt.ScrollBarAlwaysOff)
        self.vScrollBar.setForceHidden(policy == Qt.ScrollBarAlwaysOff)

    def setHorizontalScrollBarPolicy(self, policy):
        QAbstractScrollArea.setHorizontalScrollBarPolicy(self.parent(), Qt.ScrollBarAlwaysOff)
        self.hScrollBar.setForceHidden(policy == Qt.ScrollBarAlwaysOff)

