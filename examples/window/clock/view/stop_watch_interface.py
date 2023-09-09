# coding:utf-8
from PyQt6.QtWidgets import QWidget
from qfluentwidgets import FluentIcon

from view.Ui_StopWatchInterface import Ui_StopWatchInterface


class StopWatchInterface(Ui_StopWatchInterface, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.startButton.setIcon(FluentIcon.POWER_BUTTON)
        self.flagButton.setIcon(FluentIcon.FLAG)
        self.restartButton.setIcon(FluentIcon.CANCEL)
