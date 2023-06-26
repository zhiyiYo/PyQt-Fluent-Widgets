# coding:utf-8
from PyQt6.QtCore import Qt

from qfluentwidgets import PushButton, Dialog, MessageBox, ColorDialog, TeachingTip, TeachingTipTailPosition, InfoBarIcon
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
        self.setObjectName('dialogInterface')

        button = PushButton(self.tr('Show dialog'))
        button.clicked.connect(self.showDialog)
        self.addExampleCard(
            self.tr('A frameless message box'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PyQt6/examples/dialog/demo.py'
        )

        button = PushButton(self.tr('Show dialog'))
        button.clicked.connect(self.showMessageDialog)
        self.addExampleCard(
            self.tr('A message box with mask'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PyQt6/examples/message_dialog/demo.py'
        )

        button = PushButton(self.tr('Show dialog'))
        button.clicked.connect(self.showColorDialog)
        self.addExampleCard(
            self.tr('A color dialog'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PyQt6/examples/color_dialog/demo.py'
        )

        self.teachingButton = PushButton(self.tr('Show teaching tip'))
        self.teachingButton.clicked.connect(self.showBottomTeachingTip)
        self.addExampleCard(
            self.tr('A teaching tip'),
            self.teachingButton,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/teaching_tip/demo.py'
        )

        self.teachingRightButton = PushButton(self.tr('Show teaching tip'))
        self.teachingRightButton.clicked.connect(self.showLeftBottomTeachingTip)
        self.addExampleCard(
            self.tr('A teaching tip with image and button'),
            self.teachingRightButton,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/teaching_tip/demo.py'
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
        w = ColorDialog(Qt.GlobalColor.cyan, self.tr('Choose color'), self.window())
        w.colorChanged.connect(lambda c: print(c.name()))
        w.exec()

    def showBottomTeachingTip(self):
        TeachingTip.create(
            target=self.teachingButton,
            icon=InfoBarIcon.SUCCESS,
            title='Lesson 4',
            content=self.tr("With respect, let's advance towards a new stage of the spin."),
            isClosable=True,
            tailPosition=TeachingTipTailPosition.BOTTOM,
            duration=-1,
            parent=self
        )

    def showLeftBottomTeachingTip(self):
        t = TeachingTip(
            target=self.teachingRightButton,
            icon=None,
            title='Lesson 5',
            content=self.tr("The shortest shortcut is to take a detour."),
            image=":/gallery/images/Gyro.jpg",
            isClosable=True,
            tailPosition=TeachingTipTailPosition.LEFT_BOTTOM,
            duration=3000,
            parent=self.window()
        )
        button = PushButton('Action')
        button.setFixedWidth(120)
        t.addWidget(button, align=Qt.AlignmentFlag.AlignRight)
        t.show()