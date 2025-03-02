# coding:utf-8
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel, QSizePolicy

from qfluentwidgets import Pivot, setTheme, Theme, SegmentedWidget, FluentIcon


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        self.setStyleSheet("""
            Demo{background: white}
            QLabel{
                font: 20px 'Segoe UI';
                background: rgb(242,242,242);
                border-radius: 8px;
            }
        """)
        self.resize(400, 400)

        self.pivot = SegmentedWidget(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.songInterface = QLabel('Song Interface', self)
        self.albumInterface = QLabel('Album Interface', self)
        self.artistInterface = QLabel('Artist Interface', self)

        # add items to pivot
        self.addSubInterface(self.songInterface, 'songInterface', 'Song')
        self.addSubInterface(self.albumInterface, 'albumInterface', 'Album')
        self.addSubInterface(self.artistInterface, 'artistInterface', 'Artist')

        self.vBoxLayout.addWidget(self.pivot)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(30, 10, 30, 30)

        self.stackedWidget.setCurrentWidget(self.songInterface)
        self.pivot.setCurrentItem(self.songInterface.objectName())
        self.pivot.currentItemChanged.connect(
            lambda k:  self.stackedWidget.setCurrentWidget(self.findChild(QWidget, k)))

    def addSubInterface(self, widget: QLabel, objectName, text):
        widget.setObjectName(objectName)
        widget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(routeKey=objectName, text=text)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()