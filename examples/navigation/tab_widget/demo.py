# coding:utf-8
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QVBoxLayout, QApplication, QWidget

from qfluentwidgets import TabWidget, SubtitleLabel, setFont, IconWidget



class TabInterface(QWidget):
    """ Tab interface """

    def __init__(self, text: str, icon, parent=None):
        super().__init__(parent=parent)
        self.iconWidget = IconWidget(icon, self)
        self.label = SubtitleLabel(text, self)
        self.iconWidget.setFixedSize(120, 120)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.setSpacing(30)
        self.vBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(self.label, 0, Qt.AlignCenter)
        setFont(self.label, 24)



class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.tabCount = 1
        self.tabWidget = TabWidget(self)
        self.hBoxLayout = QVBoxLayout(self)

        self.tabWidget.setMovable(True)

        self.initNavigation()
        self.initWindow()

    def initNavigation(self):
        self.hBoxLayout.addWidget(self.tabWidget)

        # add tab
        self.tabWidget.addTab(TabInterface('Heart', 'resource/Heart.png'), 'As long as you love me', icon='resource/Heart.png')

        self.tabWidget.currentChanged.connect(lambda index: print("current index:", index))
        self.tabWidget.tabCloseRequested.connect(self.tabWidget.removeTab)
        self.tabWidget.tabAddRequested.connect(self.addNewPage)

    def initWindow(self):
        self.resize(1100, 750)
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self.setWindowTitle('PyQt-Fluent-Widgets')

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def addNewPage(self):
        text = f'硝子酱一级棒卡哇伊×{self.tabCount}'
        self.tabWidget.addTab(
            TabInterface(text, 'resource/Smiling_with_heart.png'), text, 'resource/Smiling_with_heart.png')
        self.tabCount += 1


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # setTheme(Theme.DARK)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
