# coding:utf-8
import sys

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QApplication

from qfluentwidgets.components.widgets.acrylic_label import AcrylicLabel


app = QApplication(sys.argv)
w = AcrylicLabel(20, QColor(105, 114, 168, 102))
w.setImage('resource/埃罗芒阿老师.jpg')
w.show()
app.exec()
