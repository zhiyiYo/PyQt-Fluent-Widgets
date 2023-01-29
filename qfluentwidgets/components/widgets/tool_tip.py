# coding:utf-8
from PySide2.QtCore import QPropertyAnimation, QTimer, Qt, QPoint, QSize
from PySide2.QtGui import QColor
from PySide2.QtWidgets import (QApplication, QFrame, QGraphicsDropShadowEffect,
                             QHBoxLayout, QLabel)

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
        self.ani = QPropertyAnimation(self, b'windowOpacity', self)

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
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint)
        self.setDarkTheme(False)
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

    def setDarkTheme(self, dark=False):
        """ set dark theme """
        self.setProperty('dark', dark)
        self.setStyle(QApplication.style())

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
        desk = QApplication.desktop()
        x = min(max(0, x), desk.width() - self.width() - 4)
        y = min(max(0, y), desk.height() - self.height() - 4)

        self.move(x, y)
