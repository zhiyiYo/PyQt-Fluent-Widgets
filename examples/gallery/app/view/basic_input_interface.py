# coding:utf-8
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QAction, QWidget, QVBoxLayout, QButtonGroup
from qfluentwidgets import (Action, DropDownPushButton, DropDownToolButton, PushButton, ToolButton, PrimaryPushButton,
                            HyperlinkButton, ComboBox, RadioButton, CheckBox, Slider, SwitchButton, EditableComboBox,
                            ToggleButton, RoundMenu, FluentIcon, SplitPushButton, SplitToolButton, PrimarySplitToolButton,
                            PrimarySplitPushButton, PrimaryDropDownPushButton, PrimaryToolButton, PrimaryDropDownToolButton,
                            ToggleToolButton, TransparentDropDownPushButton, TransparentPushButton, TransparentToggleToolButton,
                            TransparentTogglePushButton, TransparentDropDownToolButton, TransparentToolButton,
                            PillPushButton, PillToolButton)

from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class BasicInputInterface(GalleryInterface):
    """ Basic input interface """

    def __init__(self, parent=None):
        translator = Translator()
        super().__init__(
            title=translator.basicInput,
            subtitle='qfluentwidgets.components.widgets',
            parent=parent
        )
        self.setObjectName('basicInputInterface')

        # simple push button
        self.addExampleCard(
            self.tr('A simple button with text content'),
            PushButton(self.tr('Standard push button')),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # tool button
        button = ToolButton(':/gallery/images/kunkun.png')
        button.setIconSize(QSize(40, 40))
        button.resize(70, 70)
        self.addExampleCard(
            self.tr('A button with graphical content'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # primary color push button
        self.addExampleCard(
            self.tr('Accent style applied to push button'),
            PrimaryPushButton(self.tr('Accent style button')),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # primary color tool button
        self.addExampleCard(
            self.tr('Accent style applied to tool button'),
            PrimaryToolButton(FluentIcon.BASKETBALL),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # pill push button
        self.addExampleCard(
            self.tr('Pill push button'),
            PillPushButton(self.tr('Tag'), self, FluentIcon.TAG),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # pill tool button
        self.addExampleCard(
            self.tr('Pill tool button'),
            PillToolButton(FluentIcon.BASKETBALL),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # transparent push button
        self.addExampleCard(
            self.tr('A transparent push button'),
            TransparentPushButton(self.tr('Transparent push button'), self, FluentIcon.BOOK_SHELF),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # transparent tool button
        self.addExampleCard(
            self.tr('A transparent tool button'),
            TransparentToolButton(FluentIcon.BOOK_SHELF, self),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # 2-state check box
        self.addExampleCard(
            self.tr('A 2-state CheckBox'),
            CheckBox(self.tr('Two-state CheckBox')),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/check_box/demo.py'
        )

        # 3-state check box
        checkBox = CheckBox(self.tr('Three-state CheckBox'))
        checkBox.setTristate(True)
        self.addExampleCard(
            self.tr('A 3-state CheckBox'),
            checkBox,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/check_box/demo.py'
        )

        # combo box
        comboBox = ComboBox()
        comboBox.addItems(['shoko 🥰', '西宫硝子 😊', '一级棒卡哇伊的硝子酱 😘'])
        comboBox.setCurrentIndex(0)
        comboBox.setMinimumWidth(210)
        self.addExampleCard(
            self.tr('A ComboBox with items'),
            comboBox,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/combo_box/demo.py'
        )

        # editable combo box
        comboBox = EditableComboBox()
        comboBox.addItems([
            self.tr('Star Platinum'),
            self.tr('Crazy Diamond'),
            self.tr("Gold Experience"),
            self.tr('Sticky Fingers'),
        ])
        comboBox.setPlaceholderText(self.tr('Choose your stand'))
        comboBox.setMinimumWidth(210)
        self.addExampleCard(
            self.tr('An editable ComboBox'),
            comboBox,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/combo_box/demo.py'
        )

        # drop down button
        menu = RoundMenu(parent=self)
        menu.addAction(Action(FluentIcon.SEND, self.tr('Send')))
        menu.addAction(Action(FluentIcon.SAVE, self.tr('Save')))
        button = DropDownPushButton(self.tr('Email'), self, FluentIcon.MAIL)
        button.setMenu(menu)
        self.addExampleCard(
            self.tr('A push button with drop down menu'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        button = DropDownToolButton(FluentIcon.MAIL, self)
        button.setMenu(menu)
        self.addExampleCard(
            self.tr('A tool button with drop down menu'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # primary color drop down button
        button = PrimaryDropDownPushButton(self.tr('Email'), self, FluentIcon.MAIL)
        button.setMenu(menu)
        self.addExampleCard(
            self.tr('A primary color push button with drop down menu'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        button = PrimaryDropDownToolButton(FluentIcon.MAIL, self)
        button.setMenu(menu)
        self.addExampleCard(
            self.tr('A primary color tool button with drop down menu'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # transparent drop down button
        button = TransparentDropDownPushButton(self.tr('Email'), self, FluentIcon.MAIL)
        button.setMenu(menu)
        self.addExampleCard(
            self.tr('A transparent push button with drop down menu'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # transparent drop down tool button
        button = TransparentDropDownToolButton(FluentIcon.MAIL, self)
        button.setMenu(menu)
        self.addExampleCard(
            self.tr('A transparent tool button with drop down menu'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # hyperlink button
        self.addExampleCard(
            self.tr('A hyperlink button that navigates to a URI'),
            HyperlinkButton(
                'https://qfluentwidgets.com', 'GitHub', self, FluentIcon.LINK),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # radio button
        radioWidget = QWidget()
        radioLayout = QVBoxLayout(radioWidget)
        radioLayout.setContentsMargins(2, 0, 0, 0)
        radioLayout.setSpacing(15)
        radioButton1 = RadioButton(self.tr('Star Platinum'), radioWidget)
        radioButton2 = RadioButton(self.tr('Crazy Diamond'), radioWidget)
        radioButton3 = RadioButton(self.tr('Soft and Wet'), radioWidget)
        buttonGroup = QButtonGroup(radioWidget)
        buttonGroup.addButton(radioButton1)
        buttonGroup.addButton(radioButton2)
        buttonGroup.addButton(radioButton3)
        radioLayout.addWidget(radioButton1)
        radioLayout.addWidget(radioButton2)
        radioLayout.addWidget(radioButton3)
        radioButton1.click()
        self.addExampleCard(
            self.tr('A group of RadioButton controls in a button group'),
            radioWidget,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/radio_button/demo.py'
        )

        # horizontal slider
        slider = Slider(Qt.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(30)
        slider.setMinimumWidth(200)
        self.addExampleCard(
            self.tr('A simple horizontal slider'),
            slider,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/slider/demo.py'
        )

        # split button
        button = SplitPushButton(self.tr('Choose your stand'), self, FluentIcon.BASKETBALL)
        button.setFlyout(self.createStandMenu(button))
        self.addExampleCard(
            self.tr('A split push button with drop down menu'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        ikunMenu = RoundMenu(parent=self)
        ikunMenu.addActions([
            Action(self.tr('Sing')),
            Action(self.tr('Jump')),
            Action(self.tr("Rap")),
            Action(self.tr('Music')),
        ])
        button = SplitToolButton(":/gallery/images/kunkun.png", self)
        button.setIconSize(QSize(30, 30))
        button.setFlyout(ikunMenu)
        self.addExampleCard(
            self.tr('A split tool button with drop down menu'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # primary color split button
        button = PrimarySplitPushButton(self.tr('Choose your stand'), self, FluentIcon.BASKETBALL)
        button.setFlyout(self.createStandMenu(button))
        self.addExampleCard(
            self.tr('A primary color split push button with drop down menu'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        button = PrimarySplitToolButton(FluentIcon.BASKETBALL, self)
        button.setFlyout(ikunMenu)
        self.addExampleCard(
            self.tr('A primary color split tool button with drop down menu'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # switch button
        self.switchButton = SwitchButton(self.tr('Off'))
        self.switchButton.checkedChanged.connect(self.onSwitchCheckedChanged)
        self.addExampleCard(
            self.tr('A simple switch button'),
            self.switchButton,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/switch_button/demo.py'
        )

        # toggle button
        self.addExampleCard(
            self.tr('A simple toggle push button'),
            ToggleButton(self.tr('Start practicing'), self, FluentIcon.BASKETBALL),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # toggle tool button
        self.addExampleCard(
            self.tr('A simple toggle tool button'),
            ToggleToolButton(FluentIcon.BASKETBALL, self),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # transparent toggle button
        self.addExampleCard(
            self.tr('A transparent toggle push button'),
            TransparentTogglePushButton(self.tr('Start practicing'), self, FluentIcon.BASKETBALL),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )

        # transparent toggle tool button
        self.addExampleCard(
            self.tr('A transparent toggle tool button'),
            TransparentToggleToolButton(FluentIcon.BASKETBALL, self),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/basic_input/button/demo.py'
        )


    def onSwitchCheckedChanged(self, isChecked):
        if isChecked:
            self.switchButton.setText(self.tr('On'))
        else:
            self.switchButton.setText(self.tr('Off'))

    def createStandMenu(self, button):
        menu = RoundMenu(parent=self)
        menu.addActions([
            Action(self.tr('Star Platinum'), triggered=lambda c, b=button: b.setText(self.tr('Star Platinum'))),
            Action(self.tr('Crazy Diamond'), triggered=lambda c, b=button: b.setText(self.tr('Crazy Diamond'))),
            Action(self.tr("Gold Experience"), triggered=lambda c, b=button: b.setText(self.tr("Gold Experience"))),
            Action(self.tr('Sticky Fingers'), triggered=lambda c, b=button: b.setText(self.tr('Sticky Fingers'))),
        ])
        return menu