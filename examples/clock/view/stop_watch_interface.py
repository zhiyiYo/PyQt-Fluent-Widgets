# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter, QColor
from PySide6.QtWidgets import QWidget

from qfluentwidgets import FluentIcon, setFont
from view.Ui_StopWatchInterface import Ui_StopWatchInterface


class StopWatchInterface(Ui_StopWatchInterface, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.startButton.setIcon(FluentIcon.POWER_BUTTON)
        self.flagButton.setIcon(FluentIcon.FLAG)
        self.restartButton.setIcon(FluentIcon.CANCEL)

        setFont(self.timeLabel, 100)
        self.timeLabel.setTextColor(QColor(95, 95, 95), QColor(206, 206, 206))
        self.hourLabel.setTextColor(QColor(95, 95, 95), QColor(206, 206, 206))
        self.minuteLabel.setTextColor(QColor(95, 95, 95), QColor(206, 206, 206))
        self.secondLabel.setTextColor(QColor(95, 95, 95), QColor(206, 206, 206))

