# coding:utf-8
from enum import Enum

from PyQt5.QtCore import QEvent, QObject, QPoint, QTimer, Qt, QPropertyAnimation, QSize
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import (QApplication, QFrame, QGraphicsDropShadowEffect,
                             QHBoxLayout, QLabel, QWidget)

from ...common import FluentStyleSheet
from ...common.screen import getCurrentScreenGeometry


class ToolTipPosition(Enum):
    """ Info bar position """

    TOP = 0
    BOTTOM = 1
    LEFT = 2
    RIGHT = 3
    TOP_LEFT = 4
    TOP_RIGHT = 5
    BOTTOM_LEFT = 6
    BOTTOM_RIGHT = 7


class ToolTip(QFrame):
    """ Tool tip """

    def __init__(self, text='', parent=None):
        """
        Parameters
        ----------
        text: str
            the text of tool tip

        parent: QWidget
            parent widget
        """
        super().__init__(parent=parent)
        self.__text = text
        self.__duration = 1000

        self.container = self._createContainer()
        self.timer = QTimer(self)

        self.setLayout(QHBoxLayout())
        self.containerLayout = QHBoxLayout(self.container)
        self.label = QLabel(text, self)

        # set layout
        self.layout().setContentsMargins(12, 8, 12, 12)
        self.layout().addWidget(self.container)
        self.containerLayout.addWidget(self.label)
        self.containerLayout.setContentsMargins(8, 6, 8, 6)

        # add opacity effect
        self.opacityAni = QPropertyAnimation(self, b'windowOpacity', self)
        self.opacityAni.setDuration(150)

        # add shadow
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setBlurRadius(25)
        self.shadowEffect.setColor(QColor(0, 0, 0, 60))
        self.shadowEffect.setOffset(0, 5)
        self.container.setGraphicsEffect(self.shadowEffect)

        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide)

        # set style
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.__setQss()

    def text(self):
        return self.__text

    def setText(self, text):
        """ set text on tooltip """
        self.__text = text
        self.label.setText(text)
        self.container.adjustSize()
        self.adjustSize()

    def duration(self):
        return self.__duration

    def setDuration(self, duration: int):
        """ set tooltip duration in milliseconds

        Parameters
        ----------
        duration: int
            display duration in milliseconds, if `duration <= 0`, tooltip won't disappear automatically
        """
        self.__duration = duration

    def __setQss(self):
        """ set style sheet """
        self.container.setObjectName("container")
        self.label.setObjectName("contentLabel")
        FluentStyleSheet.TOOL_TIP.apply(self)
        self.label.adjustSize()
        self.adjustSize()

    def _createContainer(self):
        return QFrame(self)

    def showEvent(self, e):
        self.opacityAni.setStartValue(0)
        self.opacityAni.setEndValue(1)
        self.opacityAni.start()

        self.timer.stop()
        if self.duration() > 0:
            self.timer.start(self.__duration + self.opacityAni.duration())

        super().showEvent(e)

    def hideEvent(self, e):
        self.timer.stop()
        super().hideEvent(e)

    def adjustPos(self, widget, position: ToolTipPosition):
        """ adjust the position of tooltip relative to widget """
        manager = ToolTipPositionManager.make(position)
        self.move(manager.position(self, widget))


class ToolTipPositionManager:
    """ Tooltip position manager """

    def position(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = self._pos(tooltip, parent)
        x, y = pos.x(), pos.y()

        rect = getCurrentScreenGeometry()
        x = max(rect.left(), min(pos.x(), rect.right() - tooltip.width() - 4))
        y = max(rect.top(), min(pos.y(), rect.bottom() - tooltip.height() - 4))

        return QPoint(x, y)

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        raise NotImplementedError

    @staticmethod
    def make(position: ToolTipPosition):
        """ mask info bar manager according to the display position """
        managers = {
            ToolTipPosition.TOP: TopToolTipManager,
            ToolTipPosition.BOTTOM: BottomToolTipManager,
            ToolTipPosition.LEFT: LeftToolTipManager,
            ToolTipPosition.RIGHT: RightToolTipManager,
            ToolTipPosition.TOP_RIGHT: TopRightToolTipManager,
            ToolTipPosition.BOTTOM_RIGHT: BottomRightToolTipManager,
            ToolTipPosition.TOP_LEFT: TopLeftToolTipManager,
            ToolTipPosition.BOTTOM_LEFT: BottomLeftToolTipManager,
        }

        if position not in managers:
            raise ValueError(f'`{position}` is an invalid info bar position.')

        return managers[position]()


class TopToolTipManager(ToolTipPositionManager):
    """ Top tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget):
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() + parent.width()//2 - tooltip.width()//2
        y = pos.y() - tooltip.height()
        return QPoint(x, y)


class BottomToolTipManager(ToolTipPositionManager):
    """ Bottom tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() + parent.width()//2 - tooltip.width()//2
        y = pos.y() + parent.height()
        return QPoint(x, y)


class LeftToolTipManager(ToolTipPositionManager):
    """ Left tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() - tooltip.width()
        y = pos.y() + (parent.height() - tooltip.height()) // 2
        return QPoint(x, y)


class RightToolTipManager(ToolTipPositionManager):
    """ Right tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() + parent.width()
        y = pos.y() + (parent.height() - tooltip.height()) // 2
        return QPoint(x, y)


class TopRightToolTipManager(ToolTipPositionManager):
    """ Top right tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() + parent.width() - tooltip.width() + \
            tooltip.layout().contentsMargins().right()
        y = pos.y() - tooltip.height()
        return QPoint(x, y)


class TopLeftToolTipManager(ToolTipPositionManager):
    """ Top left tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() - tooltip.layout().contentsMargins().left()
        y = pos.y() - tooltip.height()
        return QPoint(x, y)


class BottomRightToolTipManager(ToolTipPositionManager):
    """ Bottom right tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() + parent.width() - tooltip.width() + \
            tooltip.layout().contentsMargins().right()
        y = pos.y() + parent.height()
        return QPoint(x, y)


class BottomLeftToolTipManager(ToolTipPositionManager):
    """ Bottom left tooltip position manager """

    def _pos(self, tooltip: ToolTip, parent: QWidget) -> QPoint:
        pos = parent.mapToGlobal(QPoint())
        x = pos.x() - tooltip.layout().contentsMargins().left()
        y = pos.y() + parent.height()
        return QPoint(x, y)


class ToolTipFilter(QObject):
    """ Tool tip filter """

    def __init__(self, parent: QWidget, showDelay=300, position=ToolTipPosition.TOP):
        """
        Parameters
        ----------
        parent: QWidget
            the widget to install tool tip

        showDelay: int
            show tool tip after how long the mouse hovers in milliseconds

        position: TooltipPosition
            where to show the tooltip
        """
        super().__init__(parent=parent)
        self.isEnter = False
        self._tooltip = None
        self._tooltipDelay = showDelay
        self.position = position
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.showToolTip)

    def eventFilter(self, obj: QObject, e: QEvent) -> bool:
        if e.type() == QEvent.ToolTip:
            return True
        elif e.type() in [QEvent.Hide, QEvent.Leave]:
            self.hideToolTip()
        elif e.type() == QEvent.Enter:
            self.isEnter = True
            parent = self.parent()  # type: QWidget
            if self._canShowToolTip():
                if self._tooltip is None:
                    self._tooltip = self._createToolTip()

                t = parent.toolTipDuration() if parent.toolTipDuration() > 0 else -1
                self._tooltip.setDuration(t)

                # show the tool tip after delay
                self.timer.start(self._tooltipDelay)
        elif e.type() == QEvent.MouseButtonPress:
            self.hideToolTip()

        return super().eventFilter(obj, e)

    def _createToolTip(self):
        return ToolTip(self.parent().toolTip(), self.parent().window())

    def hideToolTip(self):
        """ hide tool tip """
        self.isEnter = False
        self.timer.stop()
        if self._tooltip:
            self._tooltip.hide()

    def showToolTip(self):
        """ show tool tip """
        if not self.isEnter:
            return

        parent = self.parent()  # type: QWidget
        self._tooltip.setText(parent.toolTip())
        self._tooltip.adjustPos(parent, self.position)
        self._tooltip.show()

    def setToolTipDelay(self, delay: int):
        """ set the delay of tool tip """
        self._tooltipDelay = delay

    def _canShowToolTip(self) -> bool:
        parent = self.parent()  # type: QWidget
        return parent.isWidgetType() and parent.toolTip() and parent.isEnabled()
