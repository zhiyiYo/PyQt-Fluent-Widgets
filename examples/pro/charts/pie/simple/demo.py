# coding: utf-8
import sys
import json

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

from qfluentwidgetspro.charts import Bar, ChartWidget
from qfluentwidgets import SwitchButton, toggleTheme, qconfig, isDarkTheme


class Demo(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.switchButton = SwitchButton(self)

        self.chartWidget = ChartWidget(self)

        # https://echarts.apache.org/examples/zh/editor.html?c=pie-simple
        with open('resource/option.json', 'r', encoding='utf-8') as f:
            self.option = json.load(f)

        # render chart
        self.chartWidget.setChartOptions(self.option)

        self.initWindow()

    def initWindow(self):
        self.resize(950, 600)
        self.updateBackgroundColor()

        self.vBoxLayout.setContentsMargins(0, 50, 16, 0)
        self.vBoxLayout.addWidget(
            self.switchButton, 0, Qt.AlignmentFlag.AlignRight)
        self.vBoxLayout.addWidget(self.chartWidget)

        # connect signal to slots
        self.switchButton.checkedChanged.connect(lambda i: toggleTheme())
        qconfig.themeChanged.connect(self.updateBackgroundColor)

    def updateBackgroundColor(self):
        if isDarkTheme():
            self.setStyleSheet("Demo{background: rgb(26, 26, 26)}")
            self.switchButton.setText("深色")
        else:
            self.setStyleSheet("Demo{background: rgb(255, 255, 255)}")
            self.switchButton.setText("浅色")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()

    w.show()
    app.exec()
