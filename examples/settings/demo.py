# coding:utf-8
import os
import sys
from PySide6.QtCore import Qt, QLocale, QTranslator
from PySide6.QtGui import QIcon, QColor
from PySide6.QtWidgets import QApplication, QHBoxLayout

from qframelesswindow import FramelessWindow, StandardTitleBar
from qframelesswindow.titlebar import TitleBarButton
from setting_interface import SettingInterface
from config import cfg, Language


class CustomTitleBar(StandardTitleBar):
    """ Custom title bar """

    def __init__(self, parent):
        super().__init__(parent)

        self.titleLabel.setStyleSheet(f"""
            QLabel{{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
                color: {'white' if cfg.theme == 'dark' else 'black'}
            }}
        """)

        # customize title bar button
        if cfg.theme == 'dark':
            for button in (self.findChildren(TitleBarButton)):
                button.setNormalColor(Qt.white)
                button.setHoverColor(Qt.white)
                button.setPressedColor(Qt.white)
                if button is not self.closeBtn:
                    button.setHoverBackgroundColor(QColor(255, 255, 255, 26))
                    button.setPressedBackgroundColor(QColor(255, 255, 255, 51))


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
        self.setWindowTitle("PySide6-Fluent-Widgets")

        self.resize(1080, 784)
        desktop = QApplication.primaryScreen().size()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        self.titleBar.raise_()


if __name__ == '__main__':
    # enable dpi scale
    if cfg.get(cfg.dpiScale) != "Auto":
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

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
    app.exec()
