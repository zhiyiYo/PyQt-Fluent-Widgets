# coding:utf-8
import sys
from pathlib import Path

from PyQt5.QtCore import QModelIndex, Qt, QRect, QSize
from PyQt5.QtGui import QIcon, QPainter, QFont, QColor
from PyQt5.QtWidgets import QApplication, QStyleOptionViewItem, QWidget, QHBoxLayout, QVBoxLayout

from qfluentwidgets import (FlipImageDelegate, setTheme, Theme, HorizontalPipsPager, HorizontalFlipView,
                            VerticalFlipView, getFont)


class CustomFlipItemDelegate(FlipImageDelegate):
    """ Custom flip item delegate """

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        super().paint(painter, option, index)
        painter.save()

        # draw mask
        painter.setBrush(QColor(255, 255, 255, 200))
        painter.setPen(Qt.NoPen)
        rect = option.rect
        rect = QRect(rect.x(), rect.y(), 200, rect.height())
        painter.drawRect(rect)

        # draw text
        painter.setPen(Qt.black)
        painter.setFont(getFont(16, QFont.Bold))
        painter.drawText(rect, Qt.AlignCenter, '🥰\n硝子酱一级棒卡哇伊')

        painter.restore()



class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)
        # self.setStyleSheet('Demo{background:rgb(32,32,32)}')

        self.flipView = HorizontalFlipView(self)
        self.pager = HorizontalPipsPager(self)

        # change aspect ratio mode
        self.flipView.setAspectRatioMode(Qt.AspectRatioMode.KeepAspectRatio)

        # adjust view size
        # self.flipView.setItemSize(QSize(320, 180))
        # self.flipView.setFixedSize(QSize(320, 180))

        # NOTE: use custom delegate
        # self.flipView.setItemDelegate(CustomFlipItemDelegate(self.flipView))

        # add images
        self.flipView.addImages([str(i) for i in Path('./resource').glob('*')])
        self.pager.setPageNumber(self.flipView.count())

        # adjust border radius
        # self.flipView.setBorderRadius(15)
        # self.flipView.setFixedSize(QSize(710, 270))
        # self.flipView.setSpacing(15)

        self.pager.currentIndexChanged.connect(self.flipView.setCurrentIndex)
        self.flipView.currentIndexChanged.connect(self.pager.setCurrentIndex)

        # self.flipView.setCurrentIndex(2)

        self.setLayout(QVBoxLayout(self))
        self.layout().addWidget(self.flipView, 0, Qt.AlignCenter)
        self.layout().addWidget(self.pager, 0, Qt.AlignCenter)
        self.layout().setAlignment(Qt.AlignCenter)
        self.layout().setSpacing(20)
        self.resize(600, 600)




if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()