# coding:utf-8
from PyQt5.QtCore import Qt, QUrl

from qfluentwidgets import (PushButton, Dialog, MessageBox, ColorDialog, TeachingTip, TeachingTipTailPosition,
                            InfoBarIcon, Flyout, FlyoutView, TeachingTipView, FlyoutAnimationType, SubtitleLabel,
                            LineEdit, MessageBoxBase)
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
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/dialog_flyout/dialog/demo.py'
        )

        button = PushButton(self.tr('Show dialog'))
        button.clicked.connect(self.showMessageDialog)
        self.addExampleCard(
            self.tr('A message box with mask'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/dialog_flyout/message_dialog/demo.py'
        )

        button = PushButton(self.tr('Show dialog'))
        button.clicked.connect(self.showCustomDialog)
        self.addExampleCard(
            self.tr('A custom message box'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/dialog_flyout/custom_message_box/demo.py'
        )

        button = PushButton(self.tr('Show dialog'))
        button.clicked.connect(self.showColorDialog)
        self.addExampleCard(
            self.tr('A color dialog'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/dialog_flyout/color_dialog/demo.py'
        )

        self.simpleFlyoutButton = PushButton(self.tr('Show flyout'))
        self.simpleFlyoutButton.clicked.connect(self.showSimpleFlyout)
        self.addExampleCard(
            self.tr('A simple flyout'),
            self.simpleFlyoutButton,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/dialog_flyout/flyout/demo.py'
        )

        self.complexFlyoutButton = PushButton(self.tr('Show flyout'))
        self.complexFlyoutButton.clicked.connect(self.showComplexFlyout)
        self.addExampleCard(
            self.tr('A flyout with image and button'),
            self.complexFlyoutButton,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/dialog_flyout/flyout/demo.py'
        )

        self.teachingButton = PushButton(self.tr('Show teaching tip'))
        self.teachingButton.clicked.connect(self.showBottomTeachingTip)
        self.addExampleCard(
            self.tr('A teaching tip'),
            self.teachingButton,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/dialog_flyout/teaching_tip/demo.py'
        )

        self.teachingRightButton = PushButton(self.tr('Show teaching tip'))
        self.teachingRightButton.clicked.connect(self.showLeftBottomTeachingTip)
        self.addExampleCard(
            self.tr('A teaching tip with image and button'),
            self.teachingRightButton,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/dialog_flyout/teaching_tip/demo.py'
        )

    def showDialog(self):
        title = self.tr('This is a frameless message dialog')
        content = self.tr(
            "If the content of the message box is veeeeeeeeeeeeeeeeeeeeeeeeeery long, it will automatically wrap like this.")
        w = Dialog(title, content, self.window())
        w.setContentCopyable(True)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')

    def showMessageDialog(self):
        title = self.tr('This is a message dialog with mask')
        content = self.tr(
            "If the content of the message box is veeeeeeeeeeeeeeeeeeeeeeeeeery long, it will automatically wrap like this.")
        w = MessageBox(title, content, self.window())
        w.setContentCopyable(True)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')

    def showCustomDialog(self):
        w = CustomMessageBox(self.window())
        if w.exec():
            print(w.urlLineEdit.text())

    def showColorDialog(self):
        w = ColorDialog(Qt.cyan, self.tr('Choose color'), self.window())
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
        pos = TeachingTipTailPosition.LEFT_BOTTOM
        view = TeachingTipView(
            icon=None,
            title='Lesson 5',
            content=self.tr("The shortest shortcut is to take a detour."),
            image=":/gallery/images/Gyro.jpg",
            isClosable=True,
            tailPosition=pos,
        )

        button = PushButton('Action')
        button.setFixedWidth(120)
        view.addWidget(button, align=Qt.AlignRight)

        t = TeachingTip.make(view, self.teachingRightButton, 3000, pos, self)
        view.closed.connect(t.close)

    def showSimpleFlyout(self):
        Flyout.create(
            icon=InfoBarIcon.SUCCESS,
            title='Lesson 3',
            content=self.tr('Believe in the spin, just keep believing!'),
            target=self.simpleFlyoutButton,
            parent=self.window()
        )

    def showComplexFlyout(self):
        view = FlyoutView(
            title=self.tr('Julius·Zeppeli'),
            content=self.tr("Where the tennis ball will land when it touches the net, no one can predict. \nIf that moment comes, I hope the 'goddess' exists. \nIn that case, I would accept it no matter which side the ball falls on."),
            image=':/gallery/images/SBR.jpg',
        )

        # add button to view
        button = PushButton('Action')
        button.setFixedWidth(120)
        view.addWidget(button, align=Qt.AlignRight)

        # adjust layout (optional)
        view.widgetLayout.insertSpacing(1, 5)
        view.widgetLayout.insertSpacing(0, 5)
        view.widgetLayout.addSpacing(5)

        # show view
        Flyout.make(view, self.complexFlyoutButton, self.window(), FlyoutAnimationType.SLIDE_RIGHT)


class CustomMessageBox(MessageBoxBase):
    """ Custom message box """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(self.tr('Open URL'), self)
        self.urlLineEdit = LineEdit(self)

        self.urlLineEdit.setPlaceholderText(self.tr('Enter the URL of a file, stream, or playlist'))
        self.urlLineEdit.setClearButtonEnabled(True)

        # add widget to view layout
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.urlLineEdit)

        # change the text of button
        self.yesButton.setText(self.tr('Open'))
        self.cancelButton.setText(self.tr('Cancel'))

        self.widget.setMinimumWidth(360)
        self.yesButton.setDisabled(True)
        self.urlLineEdit.textChanged.connect(self._validateUrl)

    def _validateUrl(self, text):
        self.yesButton.setEnabled(QUrl(text).isValid())
