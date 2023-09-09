# coding:utf-8
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QHBoxLayout, QLabel

from qfluentwidgets import Action, SystemTrayMenu, MessageBox, setTheme, Theme



class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setIcon(parent.windowIcon())
        self.setToolTip('硝子酱一级棒卡哇伊🥰')

        self.menu = SystemTrayMenu(parent=parent)
        self.menu.addActions([
            Action('🎤   唱'),
            Action('🕺   跳'),
            Action('🤘🏼   RAP'),
            Action('🎶   Music'),
            Action('🏀   篮球', triggered=self.ikun),
        ])
        self.setContextMenu(self.menu)

    def ikun(self):
        content = """巅峰产生虚伪的拥护，黄昏见证真正的使徒🏀

                         ⠀⠰⢷⢿⠄
                   ⠀⠀⠀⠀⠀⣼⣷⣄
                   ⠀⠀⣤⣿⣇⣿⣿⣧⣿⡄
                   ⢴⠾⠋⠀⠀⠻⣿⣷⣿⣿⡀
                   ⠀⢀⣿⣿⡿⢿⠈⣿
                   ⠀⠀⠀⢠⣿⡿⠁⠀⡊⠀⠙
                   ⠀⠀⠀⢿⣿⠀⠀⠹⣿
                   ⠀⠀⠀⠀⠹⣷⡀⠀⣿⡄
                   ⠀⠀⠀⠀⣀⣼⣿⠀⢈⣧
        """
        w = MessageBox(
            title='坤家军！集合！',
            content=content,
            parent=self.parent()
        )
        w.yesButton.setText('献出心脏')
        w.cancelButton.setText('你干嘛~')
        w.exec()


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)

        self.setLayout(QHBoxLayout())
        self.label = QLabel('Right-click system tray icon', self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(self.label)

        self.resize(500, 500)
        self.setStyleSheet('Demo{background: white} QLabel{font-size: 20px}')
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))

        self.systemTrayIcon = SystemTrayIcon(self)
        self.systemTrayIcon.show()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()