# coding:utf-8
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout

from qfluentwidgets import FluentThemeColor, QConfig, ColorConfigItem, FluentIcon, themeColor
from qfluentwidgetspro import ColorPaletteSettingCard, CustomColorPaletteSettingCard


class Config(QConfig):
    """ Custom config """

    fontColor = ColorConfigItem('Font', 'Color', themeColor())
    backgroundColor = ColorConfigItem('Background', 'Color', FluentThemeColor.DEFAULT_BLUE.color())



class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo{background: rgb(32,32,32)}')
        self.setStyleSheet('Demo2{background: white}')

        self.resize(700, 760)

        config = Config()
        self.fontColorSettingCard = ColorPaletteSettingCard(
            configItem=config.fontColor,
            icon=FluentIcon.PENCIL_INK,
            title='颜色',
            content='改变界面的字体颜色',
            parent=self
        )
        self.bgColorSettingCard = CustomColorPaletteSettingCard(
            configItem=config.backgroundColor,
            icon=FluentIcon.BRUSH,
            title='颜色',
            content='改变界面的背景颜色',
            parent=self
        )

        self.bgColorSettingCard.colorPicker.setIcon(FluentIcon.BACKGROUND_FILL)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.addWidget(self.fontColorSettingCard)
        self.vBoxLayout.addWidget(self.bgColorSettingCard)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w2 = Demo()
    w2.show()
    sys.exit(app.exec())
