# coding:utf-8

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWidgets import QSlider


class Slider(QSlider):
    """ 可点击的滑动条 """

    clicked = pyqtSignal()

    def __init__(self, QtOrientation, parent=None):
        super().__init__(QtOrientation, parent=parent)

    def mousePressEvent(self, e: QMouseEvent):
        """ 鼠标点击时移动到鼠标所在处 """
        super().mousePressEvent(e)
        if self.orientation() == Qt.Horizontal:
            value = int(e.pos().x() / self.width() * self.maximum())
        else:
            value = int((self.height()-e.pos().y()) /
                        self.height() * self.maximum())
        self.setValue(value)
        self.clicked.emit()
