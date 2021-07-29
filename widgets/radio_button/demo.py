# coding:utf-8
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QRadioButton


class Window(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(200, 100)
        self.btn1 = QRadioButton('按钮1', self)
        self.btn2 = QRadioButton('按钮2', self)
        self.btn1.move(57, 15)
        self.btn2.move(57, 55)
        self.btn1.setChecked(True)
        with open('resource/radio_button.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
