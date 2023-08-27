# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainterPath, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget

from qfluentwidgets.components.widgets.acrylic_label import AcrylicBrush


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.resize(400, 400)
        self.acrylicBrush = AcrylicBrush(self, 15)

        path = QPainterPath()
        path.addEllipse(0, 0, 400, 400)
        self.acrylicBrush.setClipPath(path)

        self.acrylicBrush.setImage(QPixmap('resource/shoko.png').scaled(
            400, 400, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def paintEvent(self, e):
        self.acrylicBrush.paint()
        super().paintEvent(e)



if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()