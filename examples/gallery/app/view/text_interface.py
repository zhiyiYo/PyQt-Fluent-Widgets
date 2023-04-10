# coding:utf-8
from qfluentwidgets import LineEdit, SpinBox, DoubleSpinBox, TimeEdit, DateTimeEdit, DateEdit, TextEdit

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

        # spin box
        lineEdit = LineEdit(self)
        lineEdit.setText(self.tr('ko no dio da！'))
        lineEdit.setClearButtonEnabled(True)
        self.addExampleCard(
            title=self.tr("A LineEdit with a clear button"),
            widget=lineEdit,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/line_edit/demo.py'
        )

        # spin box
        self.addExampleCard(
            title=self.tr("A SpinBox with a spin button"),
            widget=SpinBox(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/spin_box/demo.py'
        )

        # double spin box
        self.addExampleCard(
            title=self.tr("A DoubleSpinBox with a spin button"),
            widget=DoubleSpinBox(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/spin_box/demo.py'
        )

        # date edit
        self.addExampleCard(
            title=self.tr("A DateEdit with a spin button"),
            widget=DateEdit(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/spin_box/demo.py'
        )

        # time edit
        self.addExampleCard(
            title=self.tr("A TimeEdit with a spin button"),
            widget=TimeEdit(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/spin_box/demo.py'
        )

        # date time edit
        self.addExampleCard(
            title=self.tr("A DateTimeEdit with a spin button"),
            widget=DateTimeEdit(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/spin_box/demo.py'
        )

        # text edit
        textEdit = TextEdit(self)
        textEdit.setMarkdown(
            "## Steel Ball Run \n * Johnny Joestar 🦄 \n * Gyro Zeppeli 🐴 ")
        textEdit.setFixedHeight(150)
        self.addExampleCard(
            title=self.tr("A simple TextEdit"),
            widget=textEdit,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/line_edit/demo.py',
            stretch=1
        )
