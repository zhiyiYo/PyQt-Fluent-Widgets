# coding:utf-8
import os
import sys
from PyQt5.QtCore import Qt, QLocale, QTranslator
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout

from qframelesswindow import FramelessWindow, TitleBar
from qframelesswindow.titlebar import TitleBarButton
from qfluentwidgets import isDarkTheme
from setting_interface import SettingInterface
from config import cfg, Language


class CustomTitleBar(TitleBar):
    """ Custom title bar """

    def __init__(self, parent):
        super().__init__(parent)
        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(20, 20)
        self.hBoxLayout.insertSpacing(0, 8)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignLeft)
        self.titleLabel.setStyleSheet(f"""
            QLabel{{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: {'white' if isDarkTheme() else 'black'}
            }}
        """)
        self.window().windowTitleChanged.connect(self.setTitle)

        # customize title bar button
        if isDarkTheme():
            for button in (self.findChildren(TitleBarButton)):
                button.setNormalColor(Qt.white)
                button.setHoverColor(Qt.white)
                button.setPressedColor(Qt.white)
                if button is not self.closeBtn:
                    button.setHoverBackgroundColor(QColor(255, 255, 255, 26))
                    button.setPressedBackgroundColor(QColor(255, 255, 255, 51))

    def setTitle(self, title):
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setIcon(self, icon):
        self.iconLabel.setPixmap(icon.pixmap(20, 20))


class Window(FramelessWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # change the default title bar if you like
        self.setTitleBar(CustomTitleBar(self))

        self.hBoxLayout = QHBoxLayout(self)
        self.settingInterface = SettingInterface(self)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.settingInterface)

        self.setWindowIcon(QIcon("resource/logo.png"))
        self.setWindowTitle("PyQt-Fluent-Widgets")

        self.resize(1080, 784)
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        self.titleBar.raise_()


if __name__ == '__main__':
    # enable dpi scale
    if cfg.get(cfg.dpiScale) == "Auto":
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    else:
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # create application
    app = QApplication(sys.argv)

    # internationalization
    translator = QTranslator()
    language = cfg.get(cfg.language)

    if language == Language.AUTO:
        translator.load(QLocale.system(), "resource/i18n/qfluentwidgets_")
    elif language != Language.ENGLISH:
        translator.load(f"resource/i18n/qfluentwidgets_{language.value}.qm")

    app.installTranslator(translator)

    # create main window
    w = Window()
    w.show()

    app.exec_()
