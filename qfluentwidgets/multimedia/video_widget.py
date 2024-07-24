# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal, QUrl, QSizeF, QTimer
from PyQt5.QtGui import QPainter
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt5.QtWidgets import QWidget, QGraphicsView, QVBoxLayout, QGraphicsScene

from ..common.style_sheet import FluentStyleSheet
from .media_play_bar import StandardMediaPlayBar


class GraphicsVideoItem(QGraphicsVideoItem):
    """ Graphics video item """

    def paint(self, painter: QPainter, option, widget):
        painter.setCompositionMode(QPainter.CompositionMode_Difference)
        super().paint(painter, option, widget)


class VideoWidget(QGraphicsView):
    """ Video widget """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.isHover = False
        self.timer = QTimer(self)

        self.vBoxLayout = QVBoxLayout(self)
        self.videoItem = QGraphicsVideoItem()
        self.graphicsScene = QGraphicsScene(self)
        self.playBar = StandardMediaPlayBar(self)

        self.setMouseTracking(True)
        self.setScene(self.graphicsScene)
        self.graphicsScene.addItem(self.videoItem)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)

        self.player.setVideoOutput(self.videoItem)
        FluentStyleSheet.MEDIA_PLAYER.apply(self)

        self.timer.timeout.connect(self._onHideTimeOut)

    def setVideo(self, url: QUrl):
        """ set the video to play """
        self.player.setSource(url)
        self.fitInView(self.videoItem, Qt.KeepAspectRatio)

    def hideEvent(self, e):
        self.pause()
        e.accept()

    def wheelEvent(self, e):
        return

    def enterEvent(self, e):
        self.isHover = True
        self.playBar.fadeIn()

    def leaveEvent(self, e):
        self.isHover = False
        self.timer.start(3000)

    def _onHideTimeOut(self):
        if not self.isHover:
            self.playBar.fadeOut()

    def play(self):
        self.playBar.play()

    def pause(self):
        self.playBar.pause()

    def stop(self):
        self.playBar.stop()

    def togglePlayState(self):
        """ toggle play state """
        if self.player.isPlaying():
            self.pause()
        else:
            self.play()

    def resizeEvent(self, e):
        super().resizeEvent(e)
        self.videoItem.setSize(QSizeF(self.size()))
        self.fitInView(self.videoItem, Qt.KeepAspectRatio)
        self.playBar.move(11, self.height() - self.playBar.height() - 11)
        self.playBar.setFixedSize(self.width() - 22, self.playBar.height())

    @property
    def player(self):
        return self.playBar.player