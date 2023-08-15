# coding:utf-8
import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QCompleter

from qfluentwidgets import LineEdit, PushButton, SearchLineEdit, setTheme, Theme


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # self.setStyleSheet("Demo {background: rgb(32, 32, 32)}")
        # setTheme(Theme.DARK)

        self.hBoxLayout = QHBoxLayout(self)
        self.lineEdit = SearchLineEdit(self)
        self.button = PushButton('Search', self)

        # add completer
        stands = [
            "Star Platinum", "Hierophant Green",
            "Made in Haven", "King Crimson",
            "Silver Chariot", "Crazy diamond",
            "Metallica", "Another One Bites The Dust",
            "Heaven's Door", "Killer Queen",
            "The Grateful Dead", "Stone Free",
            "The World", "Sticky Fingers",
            "Ozone Baby", "Love Love Deluxe",
            "Hermit Purple", "Gold Experience",
            "King Nothing", "Paper Moon King",
            "Scary Monster", "Mandom",
            "20th Century Boy", "Tusk Act 4",
            "Ball Breaker", "Sex Pistols",
            "D4C • Love Train", "Born This Way",
            "SOFT & WET", "Paisley Park",
            "Wonder of U", "Walking Heart",
            "Cream Starter", "November Rain",
            "Smooth Operators", "The Matte Kudasai"
        ]
        self.completer = QCompleter(stands, self.lineEdit)
        self.completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.completer.setMaxVisibleItems(10)
        self.lineEdit.setCompleter(self.completer)

        self.resize(400, 400)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.lineEdit, 0, Qt.AlignmentFlag.AlignCenter)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignCenter)

        self.lineEdit.setFixedSize(200, 33)
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setPlaceholderText('Search stand')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()