# coding:utf-8
import sys
from PySide6.QtCore import QEasingCurve, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication
from qfluentwidgets import SmoothScrollArea, PixmapLabel


class Demo(SmoothScrollArea):

    def __init__(self):
        super().__init__()
        self.label = PixmapLabel(self)
        self.label.setPixmap(QPixmap("resource/shoko.jpg"))

        # customize scroll animation
        self.setScrollAnimation(Qt.Vertical, 500, QEasingCurve.OutQuint)
        self.setScrollAnimation(Qt.Horizontal, 500, QEasingCurve.OutQuint)

        self.horizontalScrollBar().setValue(1900)
        self.setWidget(self.label)
        self.resize(960, 640)

        with open('resource/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()