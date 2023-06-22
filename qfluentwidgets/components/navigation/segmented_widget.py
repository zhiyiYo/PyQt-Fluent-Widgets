# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

from ...common.font import setFont
from ...common.style_sheet import themeColor
from ..widgets.button import PushButton
from .pivot import Pivot, PivotItem


class SegmentedItem(PivotItem):
    """ Segmented item """

    def _postInit(self):
        super()._postInit()
        setFont(self, 14)

    def paintEvent(self, e):
        PushButton.paintEvent(self, e)

        # draw indicator
        if not self.isSelected:
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(themeColor())

        w = 16 if not self.isPressed else 10
        x = int(self.width() / 2 - w / 2)
        painter.drawRoundedRect(x, self.height() - 4, w, 3, 1.5, 1.5)


class SegmentedWidget(Pivot):
    """ Segmented widget """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground)

    def insertItem(self, index: int, routeKey: str, text: str, onClick=None, icon=None):
        if routeKey in self.items:
            return

        item = SegmentedItem(text, self)
        if icon:
            item.setIcon(icon)

        self.insertWidget(index, routeKey, item, onClick)
        return item

