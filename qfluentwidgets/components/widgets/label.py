# coding:utf-8
from typing import List, Union

from PyQt5.QtCore import Qt, QRectF, QPoint
from PyQt5.QtGui import (QPixmap, QPainter, QPalette, QColor, QFont, QImage, QPainterPath,
                         QImageReader, QBrush, QMovie)
from PyQt5.QtWidgets import QLabel, QWidget

from ...common.overload import singledispatchmethod
from ...common.font import setFont, getFont
from ...common.config import qconfig, isDarkTheme


class PixmapLabel(QLabel):
    """ Label for high dpi pixmap """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__pixmap = QPixmap()

    def setPixmap(self, pixmap: QPixmap):
        self.__pixmap = pixmap
        self.setFixedSize(pixmap.size())
        self.update()

    def pixmap(self):
        return self.__pixmap

    def paintEvent(self, e):
        if self.__pixmap.isNull():
            return super().paintEvent(e)

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)
        painter.drawPixmap(self.rect(), self.__pixmap)


class FluentLabelBase(QLabel):
    """ Fluent label base class """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._init()

    @__init__.register
    def _(self, text: str, parent: QWidget = None):
        self.__init__(parent)
        self.setText(text)

    def _init(self):
        self.setFont(self.getFont())
        self.setTextColor()
        qconfig.themeChanged.connect(
            lambda: self.setTextColor(self.lightColor, self.darkColor))
        return self

    def getFont(self):
        raise NotImplementedError

    def setTextColor(self, light=QColor(0, 0, 0), dark=QColor(255, 255, 255)):
        """ set the text color of label

        Parameters
        ----------
        light, dark: QColor | Qt.GlobalColor | str
            text color in light/dark mode
        """
        self.lightColor = QColor(light)
        self.darkColor = QColor(dark)

        palette = self.palette()
        color = self.darkColor if isDarkTheme() else self.lightColor
        palette.setColor(QPalette.WindowText, color)
        self.setPalette(palette)


class CaptionLabel(FluentLabelBase):
    """ Caption text label """

    def getFont(self):
        return getFont(12)


class BodyLabel(FluentLabelBase):
    """ Body text label """

    def getFont(self):
        return getFont(14)


class StrongBodyLabel(FluentLabelBase):
    """ Strong body text label """

    def getFont(self):
        return getFont(14, QFont.DemiBold)


class SubtitleLabel(FluentLabelBase):
    """ Sub title text label """

    def getFont(self):
        return getFont(20, QFont.DemiBold)


class TitleLabel(FluentLabelBase):
    """ Sub title text label """

    def getFont(self):
        return getFont(28, QFont.DemiBold)


class LargeTitleLabel(FluentLabelBase):
    """ Large title text label """

    def getFont(self):
        return getFont(40, QFont.DemiBold)


class DisplayLabel(FluentLabelBase):
    """ Display text label """

    def getFont(self):
        return getFont(68, QFont.DemiBold)


class ImageLabel(QLabel):
    """ Image label """

    def __init__(self, image: Union[str, QPixmap, QImage] = None, parent=None):
        super().__init__(parent=parent)
        self.setImage(image)
        self.setBorderRadius(0, 0, 0, 0)

    def _onFrameChanged(self, index: int):
        self.image = self.movie().currentImage()
        self.update()

    def setBorderRadius(self, topLeft: int, topRight: int, bottomLeft: int, bottomRight: int):
        """ set the border radius of image """
        self.topLeftRadius = topLeft
        self.topRightRadius = topRight
        self.bottomLeftRadius = bottomLeft
        self.bottomRightRadius = bottomRight
        self.update()

    def setImage(self, image: Union[str, QPixmap, QImage] = None):
        """ set the image of label """
        self.image = QImage()

        if isinstance(image, str):
            reader = QImageReader(image)
            if reader.supportsAnimation():
                self.setMovie(QMovie(image))
                self.movie().start()
                self.image = self.movie().currentImage()
                self.movie().frameChanged.connect(self._onFrameChanged)
            else:
                self.image = reader.read()
        elif isinstance(image, QPixmap):
            self.image = image.toImage()

    def scaledToWidth(self, width: int):
        if self.isNull():
            return

        self.image = self.image.scaledToWidth(width, Qt.SmoothTransformation)
        self.setFixedSize(self.image.size())

        if self.movie():
            self.movie().setScaledSize(self.image.size())

    def scaledToHeight(self, height: int):
        if self.isNull():
            return

        self.image = self.image.scaledToHeight(height, Qt.SmoothTransformation)
        self.setFixedSize(self.image.size())

        if self.movie():
            self.movie().setScaledSize(self.image.size())

    def isNull(self):
        return self.image.isNull()

    def paintEvent(self, e):
        if self.isNull():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)

        path = QPainterPath()
        w, h = self.image.width(), self.image.height()

        # top line
        path.moveTo(self.topLeftRadius, 0)
        path.lineTo(w - self.topRightRadius, 0)

        # top right arc
        d = self.topRightRadius * 2
        path.arcTo(w - d, 0, d, d, 90, -90)

        # right line
        path.lineTo(w, h - self.bottomRightRadius)

        # bottom right arc
        d = self.bottomRightRadius * 2
        path.arcTo(w - d, h - d, d, d, 0, -90)

        # bottom line
        path.lineTo(self.bottomLeftRadius, h)

        # bottom left arc
        d = self.bottomLeftRadius * 2
        path.arcTo(0, h - d, d, d, -90, -90)

        # left line
        path.lineTo(0, self.topLeftRadius)

        # top left arc
        d = self.topLeftRadius * 2
        path.arcTo(0, 0, d, d, -180, -90)

        # draw image
        painter.setPen(Qt.NoPen)
        painter.fillPath(path, QBrush(self.image))
