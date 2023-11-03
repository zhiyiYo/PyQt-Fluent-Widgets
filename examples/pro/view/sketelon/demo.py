# coding:utf-8
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout

from qfluentwidgetspro import (Skeleton, CircleSkeletonItem, RoundedRectSkeletonItem, ArticleSkeleton,
                               CirclePersonaSkeleton, SquarePersonaSkeleton)


class CustomSkeleton(Skeleton):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(450, 87)
        # self.setWaveWidth(200)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        circle = CircleSkeletonItem()
        circle.setFixedSize(86, 86)
        self.hBoxLayout.addWidget(circle)

        self.vBoxLayout = QVBoxLayout()

        rect1 = RoundedRectSkeletonItem(8, 8, self)
        rect2 = RoundedRectSkeletonItem(8, 8, self)
        rect1.setFixedSize(340, 27)
        rect2.setFixedSize(340, 27)

        self.vBoxLayout.addWidget(rect1)
        self.vBoxLayout.addWidget(rect2)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(16)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.hBoxLayout.setSpacing(14)
        self.hBoxLayout.addLayout(self.vBoxLayout)


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.vBoxLayout = QVBoxLayout(self)

        self.articleSkeleton = ArticleSkeleton(self)
        self.circlePersonaSkeleton = CirclePersonaSkeleton(self)
        self.squarePersonaSkeleton = SquarePersonaSkeleton(self)
        self.skeleton = CustomSkeleton(self)

        self.vBoxLayout.addWidget(self.articleSkeleton)
        self.vBoxLayout.addWidget(self.circlePersonaSkeleton)
        self.vBoxLayout.addWidget(self.squarePersonaSkeleton)
        self.vBoxLayout.addWidget(self.skeleton)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.vBoxLayout.setSpacing(50)

        self.resize(600, 600)

        self.setStyleSheet('Demo{background: rgb(243,243,243)}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()