# coding:utf-8
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QAction, QHBoxLayout, QLabel
from qfluentwidgets import RoundMenu
from qfluentwidgets import MenuIconFactory as MIF


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.label = QLabel('Right-click your mouse', self)
        self.label.setAlignment(Qt.AlignCenter)
        self.layout().addWidget(self.label)
        self.resize(400, 400)

        self.setStyleSheet('Demo{background: white} QLabel{font: 20px "Segoe UI"}')

    def contextMenuEvent(self, e):
        menu = RoundMenu(parent=self)

        # add actions
        menu.addAction(QAction(MIF.create(MIF.COPY), 'Copy'))
        menu.addAction(QAction(MIF.create(MIF.CUT), 'Cut'))

        submenu = RoundMenu("Add To", self)
        submenu.setIcon(MIF.create(MIF.ADD))
        menu.addMenu(submenu)

        # add actions
        menu.addAction(QAction(MIF.create(MIF.PASTE), 'Paste'))
        menu.addAction(QAction(MIF.create(MIF.CANCEL), 'Undo'))

        # add separator
        menu.addSeparator()
        menu.addAction(QAction(f'Select all'))
        menu.exec(e.globalPos())


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()
