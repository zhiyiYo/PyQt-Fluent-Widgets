# coding:utf-8
from PyQt5.QtCore import Qt, QEasingCurve
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QLabel
from qfluentwidgets import ScrollArea, SmoothScrollArea, ToolTipFilter

from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class ScrollInterface(GalleryInterface):
    """ Scroll interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.scroll,
            subtitle="qfluentwidgets.components.widgets",
            parent=parent
        )

        w = ScrollArea()
        label = QLabel(self)
        label.setPixmap(QPixmap("app/resource/images/chidanta2.jpg").scaled(
            775, 1229, Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))
        label.installEventFilter(ToolTipFilter(label, showDelay=500))
        label.setToolTip(self.tr('Chitanda Eru is too hot 🥵'))
        label.setToolTipDuration(2000)

        w.horizontalScrollBar().setValue(0)
        w.setWidget(label)
        w.setFixedSize(780, 420)
        w.setObjectName('imageViewer')

        self.addExampleCard(
            self.tr('Smooth scroll area'),
            w,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/scroll_area/demo.py',
        )
