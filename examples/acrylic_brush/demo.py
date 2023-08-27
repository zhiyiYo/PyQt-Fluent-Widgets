# coding:utf-8
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainterPath, QPixmap
from PyQt6.QtWidgets import QApplication, QWidget

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
            400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

    def paintEvent(self, e):
        self.acrylicBrush.paint()
        super().paintEvent(e)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()