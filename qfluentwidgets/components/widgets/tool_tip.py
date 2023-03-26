# coding:utf-8
from PyQt6.QtCore import QPropertyAnimation, QEvent, QObject, QPoint, QTimer, Qt
from PyQt6.QtGui import QColor, QCursor
from PyQt6.QtWidgets import (QApplication, QFrame, QGraphicsDropShadowEffect,
                             QHBoxLayout, QLabel, QWidget)

from ...common import setStyleSheet


class ToolTip(QFrame):
    """ Tool tip """

    def __init__(self, text='', parent=None):
        super().__init__(parent=parent)
        self.__text = text
        self.__duration = 1000
        self.container = QFrame(self)
        self.timer = QTimer(self)

        self.setLayout(QHBoxLayout())
        self.containerLayout = QHBoxLayout(self.container)
        self.label = QLabel(text, self)

        # set layout
        self.layout().setContentsMargins(12, 8, 12, 12)
        self.layout().addWidget(self.container)
        self.containerLayout.addWidget(self.label)
        self.containerLayout.setContentsMargins(8, 6, 8, 6)

        # add shadow
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setBlurRadius(25)
        self.shadowEffect.setColor(QColor(0, 0, 0, 60))
        self.shadowEffect.setOffset(0, 5)
        self.container.setGraphicsEffect(self.shadowEffect)

        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide)

        # set style
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setWindowFlags(Qt.WindowType.Tool | Qt.WindowType.FramelessWindowHint)
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

    def setDuration(self, duration):
        """ set tooltip duration in milliseconds """
        self.__duration = abs(duration)

    def __setQss(self):
        """ set style sheet """
        self.container.setObjectName("container")
        self.label.setObjectName("contentLabel")
        setStyleSheet(self, 'tool_tip')
        self.label.adjustSize()
        self.adjustSize()

    def showEvent(self, e):
        self.timer.stop()
        self.timer.start(self.__duration)
        super().showEvent(e)

    def hideEvent(self, e):
        self.timer.stop()
        super().hideEvent(e)

    def adjustPos(self, pos, size):
        """ adjust the position of tooltip relative to widget

        Parameters
        ----------
        pos: QPoint
            global position of widget

        size: QSize
            size of widget
        """
        x = pos.x() + size.width()//2 - self.width()//2
        y = pos.y() - self.height()

        # adjust postion to prevent tooltips from appearing outside the screen
        rect = QApplication.screenAt(QCursor.pos()).availableGeometry()
        x = min(max(0, x) if QCursor().pos().x() >= 0 else x, rect.width() - self.width() - 4)
        y = min(max(0, y), rect.height() - self.height() - 4)

        self.move(x, y)


class ToolTipFilter(QObject):
    """ Tool button with a tool tip """

    def __init__(self, parent: QWidget, showDelay=300):
        """
        Parameters
        ----------
        parent: QWidget
            the widget to install tool tip

        showDelay: int
            show tool tip after how long the mouse hovers in milliseconds
        """
        super().__init__(parent=parent)
        self.isEnter = False
        self._tooltip = None
        self._tooltipDelay = showDelay
        self.timer = QTimer(self)

    def eventFilter(self, obj: QObject, e: QEvent) -> bool:
        if e.type() == QEvent.Type.ToolTip:
            return True
        elif e.type() in [QEvent.Type.Hide, QEvent.Type.Leave]:
            self.hideToolTip()
        elif e.type() == QEvent.Type.Enter:
            self.isEnter = True
            parent = self.parent()  # type: QWidget
            if parent.isWidgetType() and parent.toolTip():
                if self._tooltip is None:
                    self._tooltip = ToolTip(parent.toolTip(), parent.window())

                t = parent.toolTipDuration() if parent.toolTipDuration() > 0 else 1000
                self._tooltip.setDuration(t)

                # show the tool tip after delay
                QTimer.singleShot(self._tooltipDelay, self.showToolTip)

        return super().eventFilter(obj, e)

    def hideToolTip(self):
        """ hide tool tip """
        self.isEnter = False
        if self._tooltip:
            self._tooltip.hide()

    def showToolTip(self):
        """ show tool tip """
        if not self.isEnter:
            return

        parent = self.parent()  # type: QWidget
        self._tooltip.setText(parent.toolTip())
        self._tooltip.adjustPos(parent.mapToGlobal(QPoint()), parent.size())
        self._tooltip.show()

    def setToolTipDelay(self, delay: int):
        """ set the delay of tool tip """
        self._tooltipDelay = delay
