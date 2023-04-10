# coding:utf-8
import sys
from qtfluentwidgets.components.widgets.acrylic_label import AcrylicLabel
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QApplication


app = QApplication(sys.argv)
w = AcrylicLabel(20, QColor(105, 114, 168, 102))
w.setImage('resource/埃罗芒阿老师.jpg')
w.show()
app.exec_()
