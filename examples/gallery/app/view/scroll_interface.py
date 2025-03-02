# coding:utf-8
from PySide6.QtCore import Qt, QEasingCurve
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget
from qfluentwidgets import (SingleDirectionScrollArea, SmoothScrollArea, ToolTipFilter, PixmapLabel,
                            ScrollArea, ImageLabel, HorizontalPipsPager, PipsScrollButtonDisplayMode, VerticalPipsPager)

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
        self.setObjectName('scrollInterface')

        # scroll area
        w = ScrollArea()
        label = ImageLabel(":/gallery/images/chidanta2.jpg", self)
        label.scaledToWidth(775)
        label.setBorderRadius(8, 8, 8, 8)

        w.horizontalScrollBar().setValue(0)
        w.setWidget(label)
        w.setFixedSize(775, 430)

        card = self.addExampleCard(
            self.tr('Smooth scroll area'),
            w,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/scroll/scroll_area/demo.py',
        )
        card.card.installEventFilter(ToolTipFilter(card.card, showDelay=500))
        card.card.setToolTip(self.tr('Chitanda Eru is too hot 🥵'))
        card.card.setToolTipDuration(2000)

        # smooth scroll area
        w = SmoothScrollArea()
        label = ImageLabel(':/gallery/images/chidanta3.jpg', self)
        label.setBorderRadius(8, 8, 8, 8)

        w.setWidget(label)
        w.setFixedSize(660, 540)

        card = self.addExampleCard(
            self.tr('Smooth scroll area implemented by animation'),
            w,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/scroll/scroll_area/demo.py',
        )
        card.card.installEventFilter(ToolTipFilter(card.card, showDelay=500))
        card.card.setToolTip(self.tr('Chitanda Eru is so hot 🥵🥵'))
        card.card.setToolTipDuration(2000)

        # single direction scroll area
        w = SingleDirectionScrollArea(self, Qt.Horizontal)
        label = ImageLabel(":/gallery/images/chidanta4.jpg", self)
        label.setBorderRadius(8, 8, 8, 8)

        w.setWidget(label)
        w.setFixedSize(660, 498)

        card = self.addExampleCard(
            self.tr('Single direction scroll scroll area'),
            w,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/scroll/scroll_area/demo.py',
        )
        card.card.installEventFilter(ToolTipFilter(card.card, showDelay=500))
        card.card.setToolTip(self.tr('Chitanda Eru is so hot 🥵🥵🥵'))
        card.card.setToolTipDuration(2000)

        # pips pager
        pager = HorizontalPipsPager(self)
        pager.setPageNumber(15)
        pager.setPreviousButtonDisplayMode(PipsScrollButtonDisplayMode.ALWAYS)
        pager.setNextButtonDisplayMode(PipsScrollButtonDisplayMode.ALWAYS)
        card = self.addExampleCard(
            self.tr('Pips pager'),
            pager,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/scroll/pips_pager/demo.py',
        )
        card.topLayout.setContentsMargins(12, 20, 12, 20)
