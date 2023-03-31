# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtWidgets import QWidget, QHBoxLayout
from qfluentwidgets import (StateToolTip, ToolTipFilter, PushButton, PixmapLabel,
                            InfoBar, InfoBarIcon, FluentIcon, InfoBarPosition)

from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class StatusInfoInterface(GalleryInterface):
    """ Status info interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.statusInfo,
            subtitle="qfluentwidgets.components.widgets",
            parent=parent
        )

        # state tool tip
        self.stateTooltip = None
        button = PushButton(self.tr('Show StateToolTip'))
        button.clicked.connect(self.onStateButtonClicked)
        self.addExampleCard(
            self.tr('State tool tip'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/status_tool_tip/demo.py'
        )

        # tool tip
        button = PushButton(self.tr('Button with a simple ToolTip'))
        button.installEventFilter(ToolTipFilter(button))
        button.setToolTip(self.tr('Simple ToolTip'))
        self.addExampleCard(
            self.tr('State tool tip'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/tool_tip/demo.py'
        )

        label = PixmapLabel()
        label.setPixmap(QPixmap('app/resource/images/kunkun.png').scaled(
            160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label.installEventFilter(ToolTipFilter(label, showDelay=500))
        label.setToolTip(self.tr('Label with a ToolTip'))
        label.setToolTipDuration(2000)
        label.setFixedSize(160, 160)
        self.addExampleCard(
            self.tr('A label with a ToolTip'),
            label,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/tool_tip/demo.py'
        )

        # short info bar
        infoBar = InfoBar(
            icon=InfoBarIcon.SUCCESS,
            title=self.tr('Success'),
            content=self.tr("The Anthem of man is the Anthem of courage."),
            orient=Qt.Horizontal,
            isClosable=True,
            duration=-1,
            position=InfoBarPosition.NONE,
            parent=self
        )
        self.addExampleCard(
            self.tr('A closable InfoBar'),
            infoBar,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/info_bar/demo.py'
        )

        # long info bar
        content = self.tr("My name is kira yoshikake, 33 years old. Living in the villa area northeast of duwangting, unmarried. I work in Guiyou chain store. Every day I have to work overtime until 8 p.m. to go home. I don't smoke. The wine is only for a taste. Sleep at 11 p.m. for 8 hours a day. Before I go to bed, I must drink a cup of warm milk, then do 20 minutes of soft exercise, get on the bed, and immediately fall asleep. Never leave fatigue and stress until the next day. Doctors say I'm normal.")
        infoBar = InfoBar(
            icon=InfoBarIcon.WARNING,
            title=self.tr('Warning'),
            content=content,
            orient=Qt.Vertical,
            isClosable=True,
            duration=-1,
            position=InfoBarPosition.NONE,
            parent=self
        )
        self.addExampleCard(
            self.tr('A closable InfoBar with long message'),
            infoBar,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/info_bar/demo.py',
        )

        # add custom widget to info bar
        infoBar = InfoBar(
            icon=FluentIcon.GITHUB,
            title=self.tr('GitHub'),
            content=self.tr("When you look long into an abyss, the abyss looks into you."),
            orient=Qt.Horizontal,
            isClosable=True,
            duration=-1,
            position=InfoBarPosition.NONE,
            parent=self
        )
        infoBar.addWidget(PushButton(self.tr('Action')))
        infoBar.setCustomBackgroundColor("white", "#202020")
        self.addExampleCard(
            self.tr('An InfoBar with custom icon, background color and widget.'),
            infoBar,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/info_bar/demo.py',
        )

        # different type info bar
        w = QWidget(self)
        hBoxLayout = QHBoxLayout(w)
        button1 = PushButton(self.tr('Information'), w)
        button2 = PushButton(self.tr('Success'), w)
        button3 = PushButton(self.tr('Warning'), w)
        button4 = PushButton(self.tr('Error'), w)

        button1.clicked.connect(self.createInfoInfoBar)
        button2.clicked.connect(self.createSuccessInfoBar)
        button3.clicked.connect(self.createWarningInfoBar)
        button4.clicked.connect(self.createErrorInfoBar)

        hBoxLayout.addWidget(button1)
        hBoxLayout.addWidget(button2)
        hBoxLayout.addWidget(button3)
        hBoxLayout.addWidget(button4)
        hBoxLayout.setContentsMargins(0, 0, 0, 0)
        hBoxLayout.setSpacing(15)
        self.addExampleCard(
            self.tr('InfoBar with different pop-up locations'),
            w,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/info_bar/demo.py',
        )

    def onStateButtonClicked(self):
        if self.stateTooltip:
            self.stateTooltip.setContent(
                self.tr('The model training is complete!') + ' 😆')
            self.sender().setText(self.tr('Show StateToolTip'))
            self.stateTooltip.setState(True)
            self.stateTooltip = None
        else:
            self.stateTooltip = StateToolTip(
                self.tr('Training model'), self.tr('Please wait patiently'), self.window())
            self.sender().setText(self.tr('Hide StateToolTip'))
            self.stateTooltip.move(self.stateTooltip.getSuitablePos())
            self.stateTooltip.show()

    def createInfoInfoBar(self):
        InfoBar.info(
            title=self.tr('Lesson 3'),
            content=self.tr("Believe in the spin, just keep believing!"),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

    def createSuccessInfoBar(self):
        # convenient static mothod
        InfoBar.success(
            title=self.tr('Lesson 4'),
            content=self.tr("With respect, let's advance towards a new stage of the spin."),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )

    def createWarningInfoBar(self):
        InfoBar.warning(
            title=self.tr('Lesson 5'),
            content=self.tr("迂回路を行けば最短ルート。"),
            orient=Qt.Horizontal,
            isClosable=False,   # disable close button
            position=InfoBarPosition.TOP_LEFT,
            duration=2000,
            parent=self
        )

    def createErrorInfoBar(self):
        InfoBar.error(
            title=self.tr('No Internet'),
            content=self.tr("An error message which won't disappear automatically."),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,    # won't disappear automatically
            parent=self
        )
