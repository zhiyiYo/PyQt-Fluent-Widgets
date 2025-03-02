# coding: utf-8
import sys
from pathlib import Path

from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout

from qfluentwidgets import setTheme, Theme
from qfluentwidgets.multimedia import SimpleMediaPlayBar, StandardMediaPlayBar, VideoWidget


class Demo1(QWidget):

    def __init__(self):
        super().__init__()
        setTheme(Theme.DARK)
        self.vBoxLayout = QVBoxLayout(self)
        self.resize(500, 300)

        self.simplePlayBar = SimpleMediaPlayBar(self)
        self.standardPlayBar = StandardMediaPlayBar(self)

        self.vBoxLayout.addWidget(self.simplePlayBar)
        self.vBoxLayout.addWidget(self.standardPlayBar)

        # online music
        url = QUrl("https://files.cnblogs.com/files/blogs/677826/beat.zip?t=1693900324")
        self.simplePlayBar.player.setSource(url)

        # local music
        url = QUrl.fromLocalFile(str(Path('resource/aiko - シアワセ.mp3').absolute()))
        self.standardPlayBar.player.setSource(url)

        # self.standardPlayBar.play()


class Demo2(QWidget):

    def __init__(self):
        super().__init__()
        self.vBoxLayout = QVBoxLayout(self)
        self.videoWidget = VideoWidget(self)

        self.videoWidget.setVideo(QUrl('https://media.w3.org/2010/05/sintel/trailer.mp4'))
        self.videoWidget.play()

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.videoWidget)
        self.resize(800, 450)


if __name__ == '__main__':
    app = QApplication([])
    demo1 = Demo1()
    demo1.show()
    demo2 = Demo2()
    demo2.show()
    sys.exit(app.exec())