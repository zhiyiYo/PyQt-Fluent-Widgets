import sys

from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

from qfluentwidgetspro.charts import Bar, ChartWidget
from qfluentwidgets import SwitchButton, toggleTheme, qconfig, isDarkTheme


class Demo(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.timer = QTimer(self)
        self.vBoxLayout = QVBoxLayout(self)
        self.switchButton = SwitchButton(self)

        self.chartWidget = ChartWidget(self)

        # https://echarts.apache.org/examples/zh/editor.html?c=bar-simple
        self.option = {
            "title": {
                "text": "条状图",
                "x": "center"
            },
            "tooltip": {},
            "xAxis": {
                "data": ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"],
            },
            "yAxis": {},
            "series": [{
                "name": "销量",
                "type": "bar",
                "data": [5, 20, 36, 10, 10, 20]
            }],
        }

        # render chart
        self.chartWidget.setChartOptions(self.option)

        self.initWindow()

    def initWindow(self):
        self.resize(950, 600)
        self.updateBackgroundColor()

        self.vBoxLayout.setContentsMargins(0, 50, 16, 0)
        self.vBoxLayout.addWidget(self.switchButton, 0, Qt.AlignmentFlag.AlignRight)
        self.vBoxLayout.addWidget(self.chartWidget)

        # connect signal to slots
        self.switchButton.checkedChanged.connect(lambda i: toggleTheme())
        qconfig.themeChanged.connect(self.updateBackgroundColor)

        self.chartWidget.loadFinished.connect(lambda: self.timer.start(100))
        self.timer.timeout.connect(self.increaseData)

    def updateBackgroundColor(self):
        if isDarkTheme():
            self.setStyleSheet("Demo{background: rgb(26, 26, 26)}")
            self.switchButton.setText("深色")
        else:
            self.setStyleSheet("Demo{background: rgb(255, 255, 255)}")
            self.switchButton.setText("浅色")

    def increaseData(self):
        self.option["series"][0]["data"][0] += 1
        self.chartWidget.updateChartOptions(self.option)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()

    w.show()
    app.exec()