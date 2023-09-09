# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout
from qfluentwidgets import (StateToolTip, InfoBadge, ToolTipFilter, PushButton, PixmapLabel,
                            InfoBar, InfoBarIcon, FluentIcon, InfoBarPosition, ProgressBar,
                            IndeterminateProgressBar, SpinBox, ProgressRing, IndeterminateProgressRing)

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
        self.setObjectName('statusInfoInterface')

        # state tool tip
        self.stateTooltip = None
        button = PushButton(self.tr('Show StateToolTip'))
        button.clicked.connect(self.onStateButtonClicked)
        self.addExampleCard(
            self.tr('State tool tip'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/status_info/state_tool_tip/demo.py'
        )

        # tool tip
        button = PushButton(self.tr('Button with a simple ToolTip'))
        button.installEventFilter(ToolTipFilter(button))
        button.setToolTip(self.tr('Simple ToolTip'))
        self.addExampleCard(
            self.tr('A button with a simple ToolTip'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/status_info/tool_tip/demo.py'
        )

        label = PixmapLabel()
        label.setPixmap(QPixmap(':/gallery/images/kunkun.png').scaled(
            160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label.installEventFilter(ToolTipFilter(label, showDelay=500))
        label.setToolTip(self.tr('Label with a ToolTip'))
        label.setToolTipDuration(2000)
        label.setFixedSize(160, 160)
        self.addExampleCard(
            self.tr('A label with a ToolTip'),
            label,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/status_info/tool_tip/demo.py'
        )

        # info badge
        w = QWidget()
        w.setLayout(QHBoxLayout())
        w.layout().addWidget(InfoBadge.info(1))
        w.layout().addWidget(InfoBadge.success(10))
        w.layout().addWidget(InfoBadge.attension(100))
        w.layout().addWidget(InfoBadge.warning(1000))
        w.layout().addWidget(InfoBadge.error(10000))
        w.layout().addWidget(InfoBadge.custom('1w+', '#005fb8', '#60cdff'))
        w.layout().setSpacing(20)
        w.layout().setContentsMargins(0, 10, 0, 10)
        self.addExampleCard(
            self.tr('InfoBadge in different styles'),
            w,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/status_info/info_bar/demo.py'
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
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/status_info/info_bar/demo.py'
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
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/status_info/info_bar/demo.py',
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
        infoBar.setCustomBackgroundColor("white", "#2a2a2a")
        self.addExampleCard(
            self.tr('An InfoBar with custom icon, background color and widget.'),
            infoBar,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/status_info/info_bar/demo.py',
        )

        # different type info bar
        w = QWidget(self)
        hBoxLayout = QHBoxLayout(w)
        button1 = PushButton(self.tr('Top right'), w)
        button2 = PushButton(self.tr('Top'), w)
        button3 = PushButton(self.tr('Top left'), w)
        button4 = PushButton(self.tr('Bottom right'), w)
        button5 = PushButton(self.tr('Bottom'), w)
        button6 = PushButton(self.tr('Bottom left'), w)

        button1.clicked.connect(self.createTopRightInfoBar)
        button2.clicked.connect(self.createTopInfoBar)
        button3.clicked.connect(self.createTopLeftInfoBar)
        button4.clicked.connect(self.createBottomRightInfoBar)
        button5.clicked.connect(self.createBottomInfoBar)
        button6.clicked.connect(self.createBottomLeftInfoBar)

        hBoxLayout.addWidget(button1)
        hBoxLayout.addWidget(button2)
        hBoxLayout.addWidget(button3)
        hBoxLayout.addWidget(button4)
        hBoxLayout.addWidget(button5)
        hBoxLayout.addWidget(button6)
        hBoxLayout.setContentsMargins(0, 0, 0, 0)
        hBoxLayout.setSpacing(15)
        self.addExampleCard(
            self.tr('InfoBar with different pop-up locations'),
            w,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/status_info/info_bar/demo.py',
        )

        # indeterminate progress bar
        bar = IndeterminateProgressBar(self)
        bar.setFixedWidth(200)
        card = self.addExampleCard(
            self.tr('An indeterminate progress bar'),
            bar,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/status_info/progress_bar/demo.py',
        )
        card.topLayout.setContentsMargins(12, 24, 12, 24)

        # progress bar
        bar = ProgressBar(self)
        bar.setFixedWidth(200)
        self.addExampleCard(
            self.tr('An determinate progress bar'),
            ProgressWidget(bar, self),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/status_info/progress_bar/demo.py',
        )

        # Indeterminate progress ring
        ring = IndeterminateProgressRing(self)
        ring.setFixedSize(70, 70)
        self.addExampleCard(
            self.tr('An indeterminate progress ring'),
            ring,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/status_info/progress_ring/demo.py',
        )

        # progress ring
        ring = ProgressRing(self)
        ring.setFixedSize(80, 80)
        ring.setTextVisible(True)
        self.addExampleCard(
            self.tr('An determinate progress ring'),
            ProgressWidget(ring, self),
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/status_info/progress_ring/demo.py',
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

    def createTopRightInfoBar(self):
        InfoBar.info(
            title=self.tr('Lesson 3'),
            content=self.tr("Believe in the spin, just keep believing!"),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

    def createTopInfoBar(self):
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

    def createTopLeftInfoBar(self):
        InfoBar.warning(
            title=self.tr('Lesson 5'),
            content=self.tr("The shortest shortcut is to take a detour."),
            orient=Qt.Horizontal,
            isClosable=False,   # disable close button
            position=InfoBarPosition.TOP_LEFT,
            duration=2000,
            parent=self
        )

    def createBottomRightInfoBar(self):
        InfoBar.error(
            title=self.tr('No Internet'),
            content=self.tr("An error message which won't disappear automatically."),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_RIGHT,
            duration=-1,    # won't disappear automatically
            parent=self
        )

    def createBottomInfoBar(self):
        InfoBar.success(
            title=self.tr('Lesson 1'),
            content=self.tr("Don't have any strange expectations of me."),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM,
            duration=2000,    # won't disappear automatically
            parent=self
        )

    def createBottomLeftInfoBar(self):
        InfoBar.warning(
            title=self.tr('Lesson 2'),
            content=self.tr("Don't let your muscles notice."),
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.BOTTOM_LEFT,
            duration=1500,    # won't disappear automatically
            parent=self
        )


class ProgressWidget(QWidget):

    def __init__(self, widget, parent=None):
        super().__init__(parent=parent)
        hBoxLayout = QHBoxLayout(self)

        self.spinBox = SpinBox(self)
        self.spinBox.valueChanged.connect(widget.setValue)
        self.spinBox.setRange(0, 100)

        hBoxLayout.addWidget(widget)
        hBoxLayout.addSpacing(50)
        hBoxLayout.addWidget(QLabel(self.tr('Progress')))
        hBoxLayout.addSpacing(5)
        hBoxLayout.addWidget(self.spinBox)
        hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.spinBox.setValue(0)
