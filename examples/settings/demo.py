# coding:utf-8
import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication, QLabel, QHBoxLayout

from qfluentwidgets import dpi_manager
from qframelesswindow import FramelessWindow, TitleBar
from qframelesswindow.titlebar import TitleBarButton
from setting_interface import SettingInterface, cfg


class CustomTitleBar(TitleBar):
    """ Custom title bar """

    def __init__(self, parent):
        super().__init__(parent)
        # add window icon
        self.iconLabel = QLabel(self)
        self.iconLabel.setFixedSize(22, 22)
        self.hBoxLayout.insertSpacing(0, 10)
        self.hBoxLayout.insertWidget(1, self.iconLabel, 0, Qt.AlignLeft)
        self.window().windowIconChanged.connect(self.setIcon)

        # add title label
        self.titleLabel = QLabel(self)
        self.hBoxLayout.insertWidget(2, self.titleLabel, 0, Qt.AlignLeft)
        self.titleLabel.setStyleSheet(f"""
            QLabel{{
                background: transparent;
                font: 15px 'Segoe UI';
                padding: 0 3px;
                color: {'white' if cfg.theme == 'dark' else 'black'}
            }}
        """)
        self.window().windowTitleChanged.connect(self.setTitle)

        # customize title bar button
        if cfg.theme == 'dark':
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
        self.iconLabel.setPixmap(icon.pixmap(22, 22))


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

        self.resize(1350, 980)
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

        self.titleBar.raise_()


if __name__ == '__main__':
    # enable high dpi scale
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    if cfg.get(cfg.dpiScale) == "Auto":
        os.environ["QT_SCALE_FACTOR"] = str(max(1, dpi_manager.scale-0.25))
    else:
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
