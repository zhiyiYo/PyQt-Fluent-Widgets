# coding:utf-8
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QBrush, QColor, QImage, QPainter, QPixmap
from PySide6.QtWidgets import QLabel

from ...common.image_utils import gaussianBlur


class BlurCoverThread(QThread):
    """ Blur album cover thread """

    blurFinished = Signal(QPixmap)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.imagePath = ""
        self.blurRadius = 7
        self.maxSize = (450, 450)

    def run(self):
        if not self.imagePath:
            return

        pixmap = gaussianBlur(
            self.imagePath, self.blurRadius, 0.85, self.maxSize)
        self.blurFinished.emit(pixmap)

    def blur(self, imagePath: str, blurRadius=6, maxSize: tuple = (450, 450)):
        self.imagePath = imagePath
        self.blurRadius = blurRadius
        self.maxSize = maxSize or self.maxSize
        self.start()


class AcrylicTextureLabel(QLabel):
    """ Acrylic texture label """

    def __init__(self, tintColor: QColor, luminosityColor: QColor, noiseOpacity=0.03, parent=None):
        """
        Parameters
        ----------
        tintColor: QColor
            RGB tint color

        luminosityColor: QColor
            luminosity layer color

        noiseOpacity: float
            noise layer opacity

        parent:
            parent window
        """
        super().__init__(parent=parent)
        self.tintColor = QColor(tintColor)
        self.luminosityColor = QColor(luminosityColor)
        self.noiseOpacity = noiseOpacity
        self.noiseImage = QImage(':/qfluentwidgets/images/acrylic/noise.png')
        self.setAttribute(Qt.WA_TranslucentBackground)

    def setTintColor(self, color: QColor):
        self.tintColor = color
        self.update()

    def paintEvent(self, e):
        acrylicTexture = QImage(64, 64, QImage.Format_ARGB32_Premultiplied)

        # paint luminosity layer
        acrylicTexture.fill(self.luminosityColor)

        # paint tint color
        painter = QPainter(acrylicTexture)
        painter.fillRect(acrylicTexture.rect(), self.tintColor)

        # paint noise
        painter.setOpacity(self.noiseOpacity)
        painter.drawImage(acrylicTexture.rect(), self.noiseImage)

        acrylicBrush = QBrush(acrylicTexture)
        painter = QPainter(self)
        painter.fillRect(self.rect(), acrylicBrush)


class AcrylicLabel(QLabel):
    """ Acrylic label """

    def __init__(self, blurRadius: int, tintColor: QColor, luminosityColor=QColor(255, 255, 255, 0),
                 maxBlurSize: tuple = None, parent=None):
        """
        Parameters
        ----------
        blurRadius: int
            blur radius

        tintColor: QColor
            tint color

        luminosityColor: QColor
            luminosity layer color

        maxBlurSize: tuple
            maximum image size

        parent:
            parent window
        """
        super().__init__(parent=parent)
        self.imagePath = ''
        self.blurPixmap = QPixmap()
        self.blurRadius = blurRadius
        self.maxBlurSize = maxBlurSize
        self.acrylicTextureLabel = AcrylicTextureLabel(
            tintColor, luminosityColor, parent=self)
        self.blurThread = BlurCoverThread(self)
        self.blurThread.blurFinished.connect(self.__onBlurFinished)

    def __onBlurFinished(self, blurPixmap: QPixmap):
        """ blur finished slot """
        self.blurPixmap = blurPixmap
        self.setPixmap(self.blurPixmap)
        self.adjustSize()

    def setImage(self, imagePath: str):
        """ set the image to be blurred """
        if imagePath == self.imagePath:
            return

        self.imagePath = imagePath
        self.blurThread.blur(imagePath, self.blurRadius, self.maxBlurSize)

    def setTintColor(self, color: QColor):
        self.acrylicTextureLabel.setTintColor(color)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.acrylicTextureLabel.resize(self.size())

        if not self.blurPixmap.isNull():
            self.setPixmap(self.blurPixmap.scaled(
                self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))


class PixmapLabel(QLabel):
    """ Label for high dpi screen """

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
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)
        painter.drawPixmap(self.rect(), self.__pixmap)