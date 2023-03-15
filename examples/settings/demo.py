# coding:utf-8
import os
import sys
from PyQt6.QtCore import Qt, QLocale, QTranslator
from PyQt6.QtGui import QIcon, QColor
from PyQt6.QtWidgets import QApplication, QHBoxLayout

from qframelesswindow import FramelessWindow, StandardTitleBar
from qfluentwidgets import isDarkTheme
from setting_interface import SettingInterface
from config import cfg, Language



class Window(FramelessWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setTitleBar(StandardTitleBar(self))

        self.hBoxLayout = QHBoxLayout(self)
        self.settingInterface = SettingInterface(self)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.settingInterface)

        self.setWindowIcon(QIcon("resource/logo.png"))
        self.setWindowTitle("PyQt-Fluent-Widgets")

        self.resize(1080, 784)
        size = QApplication.screens()[0].size()
        w, h = size.width(), size.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        self.titleBar.raise_()

        self.setQss()
        cfg.themeChanged.connect(self.setQss)

    def setQss(self):
        theme = 'dark' if isDarkTheme() else 'light'
        with open(f'resource/qss/{theme}/demo.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())


if __name__ == '__main__':
    # enable dpi scale
    if cfg.get(cfg.dpiScale) != "Auto":
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    # create application
    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

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
    app.exec()
