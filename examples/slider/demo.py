# coding:utf-8
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QWidget, QSlider

from qfluentwidgets import HollowHandleStyle


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(300, 150)
        self.setStyleSheet("Demo{background: rgb(184, 106, 106)}")

        # customize style
        style = {
            "sub-page.color": QColor(70, 23, 180)
        }
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setStyle(HollowHandleStyle(style))

        # need adjust height
        self.slider.resize(200, 28)
        self.slider.move(50, 61)


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    sys.exit(app.exec_())
