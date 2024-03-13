# coding:utf-8
import sys

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout
from qfluentwidgets import (CaptionLabel, BodyLabel, StrongBodyLabel, SubtitleLabel, TitleLabel,
                            LargeTitleLabel, DisplayLabel, setTheme, Theme, HyperlinkLabel, setFont)


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(30, 30, 30, 30)
        self.vBoxLayout.setSpacing(20)

        self.hyperlinkLabel = HyperlinkLabel(QUrl('https://github.com/'), 'GitHub')
        # self.hyperlinkLabel.setUrl('https://qfluentwidgets.com')
        # self.hyperlinkLabel.setUnderlineVisible(True)
        # setFont(self.hyperlinkLabel, 18)

        self.vBoxLayout.addWidget(self.hyperlinkLabel)
        self.vBoxLayout.addWidget(CaptionLabel('Caption'))
        self.vBoxLayout.addWidget(BodyLabel('Body'))
        self.vBoxLayout.addWidget(StrongBodyLabel('Body Strong'))
        self.vBoxLayout.addWidget(SubtitleLabel('Subtitle'))
        self.vBoxLayout.addWidget(TitleLabel('Title'))
        self.vBoxLayout.addWidget(LargeTitleLabel('Title Large'))
        self.vBoxLayout.addWidget(DisplayLabel('Display'))

        # customize text color
        # self.vBoxLayout.itemAt(1).widget().setTextColor('#009faa', '#009faa')

        # setTheme(Theme.DARK)
        # self.setStyleSheet("QWidget{background: rgb(32, 32, 32)}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()