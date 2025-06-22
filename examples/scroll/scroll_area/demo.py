# coding:utf-8
import sys
from PySide2.QtCore import QEasingCurve, Qt
from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication
from qfluentwidgets import SmoothScrollArea, PixmapLabel, ScrollBarHandleDisplayMode


class Demo(SmoothScrollArea):

    def __init__(self):
        super().__init__()
        self.label = PixmapLabel(self)
        self.label.setPixmap(QPixmap("resource/shoko.jpg"))

        # display the handle only when mouse hover the scroll bar region
        # self.delegate.vScrollBar.setHandleDisplayMode(ScrollBarHandleDisplayMode.ON_HOVER)

        # customize scroll animation
        self.setScrollAnimation(Qt.Vertical, 500, QEasingCurve.OutQuint)
        self.setScrollAnimation(Qt.Horizontal, 500, QEasingCurve.OutQuint)

        self.horizontalScrollBar().setValue(1900)
        self.setWidget(self.label)
        self.resize(1200, 800)

        with open('resource/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()