# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QCompleter
from qfluentwidgets import (LineEdit, SpinBox, DoubleSpinBox, TimeEdit, DateTimeEdit, DateEdit,
                            TextEdit, SearchLineEdit, PasswordLineEdit)

from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class TextInterface(GalleryInterface):
    """ Text interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.text,
            subtitle="qfluentwidgets.components.widgets",
            parent=parent
        )
        self.setObjectName('textInterface')

        # line edit
        lineEdit = LineEdit(self)
        lineEdit.setText(self.tr('ko no dio da！'))
        lineEdit.setClearButtonEnabled(True)
        self.addExampleCard(
            title=self.tr("A LineEdit with a clear button"),
            widget=lineEdit,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/text/line_edit/demo.py'
        )

        # line edit with completer
        lineEdit = SearchLineEdit(self)
        lineEdit.setPlaceholderText(self.tr('Type a stand name'))
        lineEdit.setClearButtonEnabled(True)
        lineEdit.setFixedWidth(230)
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
        completer = QCompleter(stands, lineEdit)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        completer.setMaxVisibleItems(10)
        lineEdit.setCompleter(completer)

        self.addExampleCard(
            title=self.tr("A autosuggest line edit"),
            widget=lineEdit,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/text/line_edit/demo.py'
        )

        # password line edit
        passwordLineEdit = PasswordLineEdit(self)
        passwordLineEdit.setFixedWidth(230)
        passwordLineEdit.setPlaceholderText(self.tr("Enter your password"))
        self.addExampleCard(
            title=self.tr("A password line edit"),
            widget=passwordLineEdit,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/text/line_edit/demo.py'
        )

        # spin box
        self.addExampleCard(
            title=self.tr("A SpinBox with a spin button"),
            widget=SpinBox(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/text/spin_box/demo.py'
        )

        # double spin box
        self.addExampleCard(
            title=self.tr("A DoubleSpinBox with a spin button"),
            widget=DoubleSpinBox(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/text/spin_box/demo.py'
        )

        # date edit
        self.addExampleCard(
            title=self.tr("A DateEdit with a spin button"),
            widget=DateEdit(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/text/spin_box/demo.py'
        )

        # time edit
        self.addExampleCard(
            title=self.tr("A TimeEdit with a spin button"),
            widget=TimeEdit(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/text/spin_box/demo.py'
        )

        # date time edit
        self.addExampleCard(
            title=self.tr("A DateTimeEdit with a spin button"),
            widget=DateTimeEdit(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/text/spin_box/demo.py'
        )

        # text edit
        textEdit = TextEdit(self)
        textEdit.setMarkdown(
            "## Steel Ball Run \n * Johnny Joestar 🦄 \n * Gyro Zeppeli 🐴 ")
        textEdit.setFixedHeight(150)
        self.addExampleCard(
            title=self.tr("A simple TextEdit"),
            widget=textEdit,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/text/line_edit/demo.py',
            stretch=1
        )
