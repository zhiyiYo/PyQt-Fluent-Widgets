# coding:utf-8
import warnings
from  typing import Union

from PyQt6.QtCore import Qt, QThread, pyqtSignal, QRect
from PyQt6.QtGui import QBrush, QColor, QImage, QPainter, QPixmap, QPainterPath
from PyQt6.QtWidgets import QLabel, QApplication, QWidget

from ...common.screen import getCurrentScreen

try:
    from ...common.image_utils import gaussianBlur

    isAcrylicAvailable = True
except ImportError as e:
    isAcrylicAvailable = False

    def gaussianBlur(imagePath, blurRadius=18, brightFactor=1, blurPicSize=None):
        return QPixmap(imagePath)


def checkAcrylicAvailability():
    if not isAcrylicAvailable:
        warnings.warn(
            'Acrylic is not supported in current qfluentwidgets, use `pip install PyQt6-Fluent-Widgets[full]` to enable it.')

    return isAcrylicAvailable


class BlurCoverThread(QThread):
    """ Blur album cover thread """

    blurFinished = pyqtSignal(QPixmap)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.imagePath = ""
        self.blurRadius = 7
        self.maxSize = None

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
        checkAcrylicAvailability()

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
        self.imagePath = imagePath
        self.blurThread.blur(imagePath, self.blurRadius, self.maxBlurSize)

    def setTintColor(self, color: QColor):
        self.acrylicTextureLabel.setTintColor(color)

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.acrylicTextureLabel.resize(self.size())

        if not self.blurPixmap.isNull() and self.blurPixmap.size() != self.size():
            self.setPixmap(self.blurPixmap.scaled(
                self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))


class AcrylicBrush:
    """ Acrylic brush """

    def __init__(self, device: QWidget, blurRadius: int, tintColor=QColor(242, 242, 242, 150),
                 luminosityColor=QColor(255, 255, 255, 10), noiseOpacity=0.03):
        self.device = device
        self.blurRadius = blurRadius
        self.tintColor = QColor(tintColor)
        self.luminosityColor = QColor(luminosityColor)
        self.noiseOpacity = noiseOpacity
        self.noiseImage = QImage(':/qfluentwidgets/images/acrylic/noise.png')
        self.originalImage = QPixmap()
        self.image = QPixmap()

        self.clipPath = QPainterPath()

    def setBlurRadius(self, radius: int):
        if radius == self.blurRadius:
            return

        self.blurRadius = radius
        self.setImage(self.originalImage)

    def setTintColor(self, color: QColor):
        self.tintColor = QColor(color)
        self.device.update()

    def setLuminosityColor(self, color: QColor):
        self.luminosityColor = QColor(color)
        self.device.update()

    def isAvailable(self):
        return isAcrylicAvailable

    def grabImage(self, rect: QRect):
        """ grab image from screen

        Parameters
        ----------
        rect: QRect
            grabbed region
        """
        screen = getCurrentScreen()
        if not screen:
            screen = QApplication.screens()[0]

        x, y, w, h = rect.x(), rect.y(), rect.width(), rect.height()
        x -= screen.geometry().x()
        y -= screen.geometry().y()
        self.setImage(screen.grabWindow(0, x, y, w, h))

    def setImage(self, image: Union[str, QImage, QPixmap]):
        """ set blurred image """
        if isinstance(image, str):
            image = QPixmap(image)
        elif isinstance(image, QImage):
            image = QPixmap.fromImage(image)

        self.originalImage = image
        if not image.isNull():
            checkAcrylicAvailability()

            self.image = gaussianBlur(image, self.blurRadius)

        self.device.update()

    def setClipPath(self, path: QPainterPath):
        self.clipPath = path
        self.device.update()

    def textureImage(self):
        texture = QImage(64, 64, QImage.Format.Format_ARGB32_Premultiplied)
        texture.fill(self.luminosityColor)

        # paint tint color
        painter = QPainter(texture)
        painter.fillRect(texture.rect(), self.tintColor)

        # paint noise
        painter.setOpacity(self.noiseOpacity)
        painter.drawImage(texture.rect(), self.noiseImage)

        return texture

    def paint(self):
        device = self.device

        painter = QPainter(device)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        if not self.clipPath.isEmpty():
            painter.setClipPath(self.clipPath)

        # paint image
        image = self.image.scaled(
            device.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        painter.drawPixmap(0, 0, image)

        # paint acrylic texture
        painter.fillRect(device.rect(), QBrush(self.textureImage()))
