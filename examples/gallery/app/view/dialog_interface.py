# coding:utf-8
from PyQt5.QtCore import Qt

from qfluentwidgets import PushButton, Dialog, MessageBox, ColorDialog
from ..common.translator import Translator
from .gallery_interface import GalleryInterface


class DialogInterface(GalleryInterface):
    """ Dialog interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.dialogs,
            subtitle='qfluentwidgets.components.dialog_box',
            parent=parent
        )

        button = PushButton(self.tr('Show dialog'))
        button.clicked.connect(self.showDialog)
        self.addExampleCard(
            self.tr('A frameless message box'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/dialog/demo.py'
        )

        button = PushButton(self.tr('Show dialog'))
        button.clicked.connect(self.showMessageDialog)
        self.addExampleCard(
            self.tr('A message box with mask'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/message_dialog/demo.py'
        )

        button = PushButton(self.tr('Show dialog'))
        button.clicked.connect(self.showColorDialog)
        self.addExampleCard(
            self.tr('A color dialog'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/color_dialog/demo.py'
        )

    def showDialog(self):
        title = self.tr('This is a frameless message dialog')
        content = self.tr(
            "If the content of the message box is veeeeeeeeeeeeeeeeeeeeeeeeeery long, it will automatically wrap like this.")
        w = Dialog(title, content, self.window())
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')

    def showMessageDialog(self):
        title = self.tr('This is a message dialog with mask')
        content = self.tr(
            "If the content of the message box is veeeeeeeeeeeeeeeeeeeeeeeeeery long, it will automatically wrap like this.")
        w = MessageBox(title, content, self.window())
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')

    def showColorDialog(self):
        w = ColorDialog(Qt.cyan, self.tr('Choose color'), self.window())
        w.colorChanged.connect(lambda c: print(c.name()))
        w.exec()