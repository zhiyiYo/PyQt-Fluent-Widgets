# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel
from qfluentwidgets import StateToolTip, ToolTipFilter, PushButton

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

        label = QLabel()
        label.setPixmap(QPixmap('app/resource/images/kunkun.png').scaled(
            200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        label.installEventFilter(ToolTipFilter(label, showDelay=500))
        label.setToolTip(self.tr('Label with a ToolTip'))
        label.setToolTipDuration(2000)
        label.setFixedSize(200, 200)
        self.addExampleCard(
            self.tr('A label with a ToolTip'),
            label,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/tool_tip/demo.py'
        )

    def onStateButtonClicked(self):
        if self.stateTooltip:
            self.stateTooltip.setContent(self.tr('The model training is complete!') +' 😆')
            self.stateTooltip.setState(True)
            self.stateTooltip = None
        else:
            self.stateTooltip = StateToolTip(
                self.tr('Training model'), self.tr('Please wait patiently'), self.window())
            self.sender().setText(self.tr('Hide state tool tip'))
            self.stateTooltip.move(self.stateTooltip.getSuitablePos())
            self.stateTooltip.show()
