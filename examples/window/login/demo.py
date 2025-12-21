import sys

from PyQt5.QtCore import Qt, QTranslator, QLocale, QRect
from PyQt5.QtGui import QIcon, QPixmap, QColor
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import setThemeColor, FluentTranslator, setTheme, Theme, SplitTitleBar, isDarkTheme, FluentWidget
from Ui_LoginWindow import Ui_Form


class LoginWindow(FluentWidget, Ui_Form):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        setThemeColor('#28afe9')

        if sys.platform != "darwin":
            self.titleBar.titleLabel.setTextColor(Qt.GlobalColor.white, Qt.GlobalColor.white)

        # place the title on top layer
        self.titleBar.raise_()

        self.label.setScaledContents(False)

        self.setWindowTitle('PyQt-Fluent-Widget')
        self.setWindowIcon(QIcon(":/images/logo.png"))
        self.resize(1000, 650)

        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        pixmap = QPixmap(":/images/background.jpg").scaled(
            self.label.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    # use dark theme mode
    # setTheme(Theme.DARK)

    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    # Internationalization
    translator = FluentTranslator(QLocale())
    app.installTranslator(translator)

    w = LoginWindow()
    w.show()
    app.exec_()