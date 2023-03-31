# coding:utf-8
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtWidgets import QWidget, QHBoxLayout
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
            160, 160, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
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
            content=self.tr("Essential app message for your users."),
            orient=Qt.Orientation.Horizontal,
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
        content = self.tr("A long essential app message for your users to be informed of, acknowledge, or take action on. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dapibus dolor vitae justo rutrum, ut lobortis nibh mattis. Aenean id elit commodo, semper felis nec.")
        infoBar = InfoBar(
            icon=InfoBarIcon.WARNING,
            title=self.tr('Warning'),
            content=content,
            orient=Qt.Orientation.Vertical,
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
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            duration=-1,
            position=InfoBarPosition.NONE,
            parent=self
        )
        infoBar.addWidget(PushButton('Action'))
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
        content = "A long essential app message for your users to be informed of, acknowledge, or take action on. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin dapibus dolor vitae justo rutrum, ut lobortis nibh mattis. Aenean id elit commodo, semper felis nec."
        w = InfoBar(
            icon=InfoBarIcon.INFORMATION,
            title='Information',
            content=content,
            orient=Qt.Orientation.Vertical,    # vertical layout
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )
        w.show()

    def createSuccessInfoBar(self):
        content = "A short essential success app message."
        # convenient static mothod
        InfoBar.success(
            title='Title',
            content=content,
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )

    def createWarningInfoBar(self):
        InfoBar.warning(
            title='Title',
            content="A short essential app warning message.",
            orient=Qt.Orientation.Horizontal,
            isClosable=False,   # disable close button
            position=InfoBarPosition.TOP_LEFT,
            duration=2000,
            parent=self
        )

    def createErrorInfoBar(self):
        InfoBar.error(
            title=self.tr('No Internet'),
            content="A error message which won't disappear automatically.",
            orient=Qt.Orientation.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,    # won't disappear automatically
            parent=self
        )
