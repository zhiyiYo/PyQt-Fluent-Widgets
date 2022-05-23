# coding:utf-8
from PyQt5.QtCore import QFile, QPropertyAnimation, QTimer, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import (QApplication, QFrame, QGraphicsDropShadowEffect,
                             QHBoxLayout, QLabel)


class ToolTip(QFrame):

    def __init__(self, text='', parent=None):
        super().__init__(parent=parent)
        self.__text = text
        self.__duration = 1000
        self.timer = QTimer(self)
        self.hBox = QHBoxLayout(self)
        self.label = QLabel(text, self)
        self.ani = QPropertyAnimation(self, b'windowOpacity', self)

        # set layout
        self.hBox.addWidget(self.label)
        self.hBox.setContentsMargins(10, 7, 10, 7)

        # add shadow
        self.shadowEffect = QGraphicsDropShadowEffect(self)
        self.shadowEffect.setBlurRadius(32)
        self.shadowEffect.setColor(QColor(0, 0, 0, 60))
        self.shadowEffect.setOffset(0, 5)
        self.setGraphicsEffect(self.shadowEffect)

        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide)

        # set style
        self.setAttribute(Qt.WA_StyledBackground)
        self.setDarkTheme(False)
        self.__setQss()

    def text(self):
        return self.__text

    def setText(self, text: str):
        """ set text on tooltip """
        self.__text = text
        self.label.setText(text)
        self.label.adjustSize()
        self.adjustSize()

    def duration(self):
        return self.__duration

    def setDuration(self, duration: int):
        """ set tooltip duration in milliseconds """
        self.__duration = abs(duration)

    def __setQss(self):
        """ set style sheet """
        f = QFile("resource/tooltip.qss")
        f.open(QFile.ReadOnly)
        self.setStyleSheet(str(f.readAll(), encoding='utf-8'))
        f.close()

        self.label.adjustSize()
        self.adjustSize()

    def setDarkTheme(self, dark=False):
        """ set dark theme """
        dark = 'true' if dark else 'false'
        self.setProperty('dark', dark)
        self.label.setProperty('dark', dark)
        self.setStyle(QApplication.style())

    def showEvent(self, e):
        self.timer.stop()
        self.timer.start(self.__duration)
        super().showEvent(e)

    def hideEvent(self, e):
        self.timer.stop()
        super().hideEvent(e)