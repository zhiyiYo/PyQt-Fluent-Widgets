# coding:utf-8
import warnings

from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QBrush, QColor, QImage, QPainter, QPixmap
from PyQt6.QtWidgets import QLabel

try:
    from ...common.image_utils import gaussianBlur
except ImportError as e:
    warnings.warn('`AcrylicLabel` is not supported in current qfluentwidgets, use `pip install PyQt-Fluent-Widgets[full]` to enable it.')


class BlurCoverThread(QThread):
    """ Blur album cover thread """

    blurFinished = pyqtSignal(QPixmap)

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

    def blur(self, imagePath, blurRadius=6, maxSize=(450, 450)):
        self.imagePath = imagePath
        self.blurRadius = blurRadius
        self.maxSize = maxSize or self.maxSize
        self.start()


class AcrylicTextureLabel(QLabel):
    """ Acrylic texture label """

    def __init__(self, tintColor, luminosityColor, noiseOpacity=0.03, parent=None):
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
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def setTintColor(self, color: QColor):
        self.tintColor = color
        self.update()

    def paintEvent(self, e):
        acrylicTexture = QImage(64, 64, QImage.Format.Format_ARGB32_Premultiplied)

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

    def __init__(self, blurRadius, tintColor, luminosityColor=QColor(255, 255, 255, 0),
                 maxBlurSize=None, parent=None):
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

    def __onBlurFinished(self, blurPixmap):
        """ blur finished slot """
        self.blurPixmap = blurPixmap
        self.setPixmap(self.blurPixmap)
        self.adjustSize()

    def setImage(self, imagePath):
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
            self.setPixmap(
                self.blurPixmap.scaled(
                    self.size(),
                    Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
