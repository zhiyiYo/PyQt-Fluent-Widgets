# coding:utf-8
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QColor, QPen, QPainter, QFont

from .progress_bar import ProgressBar
from ...common.style_sheet import themeColor, isDarkTheme


class ProgressRing(ProgressBar):
    """ Progress ring """

    def __init__(self, parent=None, useAni=True):
        super().__init__(parent, useAni=useAni)
        self.lightBackgroundColor = QColor(0, 0, 0, 34)
        self.darkBackgroundColor = QColor(255, 255, 255, 34)

        self.setTextVisible(False)
        self.setFixedSize(100, 100)

        font = QFont()
        font.setFamilies(['Segoe UI', 'Microsoft YaHei'])
        font.setPixelSize(14)
        self.setFont(font)

    def _drawText(self, painter: QPainter, text: str):
        """ draw text """
        painter.setFont(self.font())
        painter.setPen(Qt.GlobalColor.white if isDarkTheme() else Qt.GlobalColor.black)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, text)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        cw = 6    # circle thickness
        w = min(self.height(), self.width()) - cw
        rc = QRectF(cw/2, self.height()/2 - w/2, w, w)

        # draw background
        bc = self.darkBackgroundColor if isDarkTheme() else self.lightBackgroundColor
        pen = QPen(bc, cw, cap=Qt.PenCapStyle.RoundCap, join=Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        painter.drawArc(rc, 0, 360*16)

        if self.maximum() <= self.minimum():
            return

        # draw bar
        pen.setColor(themeColor())
        painter.setPen(pen)
        degree = int(self.val / (self.maximum() - self.minimum()) * 360)
        painter.drawArc(rc, 90*16, -degree*16)

        # draw text
        if self.isTextVisible():
            self._drawText(painter, self.valText())
