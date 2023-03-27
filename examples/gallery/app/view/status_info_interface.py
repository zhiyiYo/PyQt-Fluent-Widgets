# coding:utf-8
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QLabel
from qfluentwidgets import StateToolTip, ToolTipFilter, PushButton, PixmapLabel

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

        self.stateTooltip = None
        button = PushButton(self.tr('Show StateToolTip'))
        button.clicked.connect(self.onStateButtonClicked)
        self.addExampleCard(
            self.tr('State tool tip'),
            button,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/status_tool_tip/demo.py'
        )

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

    def onStateButtonClicked(self):
        if self.stateTooltip:
            self.stateTooltip.setContent(self.tr('The model training is complete!') +' 😆')
            self.sender().setText(self.tr('Show StateToolTip'))
            self.stateTooltip.setState(True)
            self.stateTooltip = None
        else:
            self.stateTooltip = StateToolTip(
                self.tr('Training model'), self.tr('Please wait patiently'), self.window())
            self.sender().setText(self.tr('Hide StateToolTip'))
            self.stateTooltip.move(self.stateTooltip.getSuitablePos())
            self.stateTooltip.show()
