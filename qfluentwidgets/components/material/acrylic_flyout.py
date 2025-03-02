# coding:utf-8
from typing import Union
from PyQt5.QtCore import QPoint, Qt, QRect, QRectF
from PyQt5.QtGui import QPixmap, QPainter, QColor, QPainterPath, QIcon, QImage
from PyQt5.QtWidgets import QWidget

from ...common.style_sheet import isDarkTheme
from ...common.icon import FluentIconBase
from ..widgets.flyout import FlyoutAnimationType, FlyoutViewBase, FlyoutView, Flyout, FlyoutAnimationManager
from .acrylic_widget import AcrylicWidget


class AcrylicFlyoutViewBase(AcrylicWidget, FlyoutViewBase):
    """ Acrylic flyout view base """

    def acrylicClipPath(self):
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect().adjusted(1, 1, -1, -1)), 8, 8)
        return path

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        self._drawAcrylic(painter)

        # draw border
        painter.setBrush(Qt.NoBrush)
        painter.setPen(self.borderColor())
        rect = QRectF(self.rect()).adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(rect, 8, 8)


class AcrylicFlyoutView(AcrylicWidget, FlyoutView):
    """ Acrylic flyout view """

    def acrylicClipPath(self):
        path = QPainterPath()
        path.addRoundedRect(QRectF(self.rect().adjusted(1, 1, -1, -1)), 8, 8)
        return path

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        self._drawAcrylic(painter)

        # draw border
        painter.setBrush(Qt.NoBrush)
        painter.setPen(self.borderColor())
        rect = self.rect().adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(rect, 8, 8)


class AcrylicFlyout(Flyout):
    """ Acrylic flyout """

    @classmethod
    def create(cls, title: str, content: str, icon: Union[FluentIconBase, QIcon, str] = None,
               image: Union[str, QPixmap, QImage] = None, isClosable=False, target: Union[QWidget, QPoint] = None,
               parent=None, aniType=FlyoutAnimationType.PULL_UP, isDeleteOnClose=True):
        """ create and show a flyout using the default view

        Parameters
        ----------
        title: str
            the title of teaching tip

        content: str
            the content of teaching tip

        icon: InfoBarIcon | FluentIconBase | QIcon | str
            the icon of teaching tip

        image: str | QPixmap | QImage
            the image of teaching tip

        isClosable: bool
            whether to show the close button

        target: QWidget | QPoint
            the target widget or position to show flyout

        parent: QWidget
            parent window

        aniType: FlyoutAnimationType
            flyout animation type

        isDeleteOnClose: bool
            whether delete flyout automatically when flyout is closed
        """
        view = AcrylicFlyoutView(title, content, icon, image, isClosable)
        w = cls.make(view, target, parent, aniType, isDeleteOnClose)
        view.closed.connect(w.close)
        return w

    def exec(self, pos: QPoint, aniType=FlyoutAnimationType.PULL_UP):
        """ show calendar view """
        self.aniManager = FlyoutAnimationManager.make(aniType, self)

        if isinstance(self.view, AcrylicWidget):
            pos = self.aniManager._adjustPosition(pos)
            self.view.acrylicBrush.grabImage(QRect(pos, self.layout().sizeHint()))

        self.show()
        self.aniManager.exec(pos)