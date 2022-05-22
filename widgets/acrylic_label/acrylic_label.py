# coding:utf-8
import numpy as np
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QImage, QPainter, QPixmap
from PyQt5.QtWidgets import QLabel
from scipy.ndimage.filters import gaussian_filter


def gaussianBlur(imagePath: str, blurRadius=18, brightFactor=1, blurPicSize: tuple = None) -> np.ndarray:
    if not imagePath.startswith(':'):
        image = Image.open(imagePath)
    else:
        image = Image.fromqpixmap(QPixmap(imagePath))

    if blurPicSize:
        # adjust image size to reduce computation
        w, h = image.size
        ratio = min(blurPicSize[0] / w, blurPicSize[1] / h)
        w_, h_ = w * ratio, h * ratio

        if w_ < w:
            image = image.resize((int(w_), int(h_)), Image.ANTIALIAS)

    image = np.array(image)

    # handle gray image
    if len(image.shape) == 2:
        image = np.stack([image, image, image], axis=-1)

    # blur each channel
    for i in range(3):
        image[:, :, i] = gaussian_filter(
            image[:, :, i], blurRadius) * brightFactor

    return image


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
        self.noiseImage = QImage('resource/noise.png')
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

    def setImage(self, imagePath: str):
        """ set the image to be blurred """
        if imagePath == self.imagePath:
            return

        self.imagePath = imagePath
        image = Image.fromarray(gaussianBlur(
            imagePath, self.blurRadius, 0.85, self.maxBlurSize))
        self.blurPixmap = image.toqpixmap()  # type:QPixmap
        self.setPixmap(self.blurPixmap)
        self.adjustSize()

    def setTintColor(self, color: QColor):
        self.acrylicTextureLabel.setTintColor(color)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.acrylicTextureLabel.resize(self.size())
        self.setPixmap(self.blurPixmap.scaled(
            self.size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
