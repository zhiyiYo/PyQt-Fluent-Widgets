# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal, QObject, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QWidget


class MediaPlayerBase(QObject):
    """ Media player base class """

    mediaStatusChanged = pyqtSignal(QMediaPlayer.MediaStatus)
    playbackRateChanged = pyqtSignal(float)
    positionChanged = pyqtSignal(int)
    durationChanged = pyqtSignal(int)
    sourceChanged = pyqtSignal(QUrl)
    volumeChanged = pyqtSignal(int)
    mutedChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def isPlaying(self):
        """ Whether the media is playing """
        raise NotImplementedError

    def mediaStatus(self) -> QMediaPlayer.MediaStatus:
        """ Return the status of the current media stream """
        raise NotImplementedError

    def playbackState(self) -> QMediaPlayer.State:
        """ Return the playback status of the current media stream """
        raise NotImplementedError

    def duration(self):
        """ Returns the duration of the current media in ms """
        raise NotImplementedError

    def position(self):
        """ Returns the current position inside the media being played back in ms """
        raise NotImplementedError

    def volume(self):
        """ Return the volume of player """
        raise NotImplementedError

    def source(self) -> QUrl:
        """ Return the active media source being used """
        raise NotImplementedError

    def pause(self):
        """ Pause playing the current source """
        raise NotImplementedError

    def play(self):
        """ Start or resume playing the current source """
        raise NotImplementedError

    def stop(self):
        """ Stop playing, and reset the play position to the beginning """
        raise NotImplementedError

    def playbackRate(self) -> float:
        """ Return the playback rate of the current media """
        raise NotImplementedError

    def setPosition(self, position: int):
        """ Sets the position of media in ms """
        raise NotImplementedError

    def setSource(self, media: QUrl):
        """ Sets the current source """
        raise NotImplementedError

    def setPlaybackRate(self, rate: float):
        """ Sets the playback rate of player """
        raise NotImplementedError

    def setVolume(self, volume: int):
        """ Sets the volume of player """
        raise NotImplementedError

    def setMuted(self, isMuted: bool):
        raise NotImplementedError

    def videoOutput(self) -> QObject:
        """ Return the video output to be used by the media player """
        raise NotImplementedError

    def setVideoOutput(self, output: QObject) -> None:
        """ Sets the video output to be used by the media player """
        raise NotImplementedError


class MediaPlayer(QMediaPlayer):
    """ Media player """

    sourceChanged = pyqtSignal(QUrl)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mediaChanged.connect(lambda i: i.canonicalUrl())
        self.setNotifyInterval(1000)

    def isPlaying(self):
        return self.state() == QMediaPlayer.PlayingState

    def source(self) -> QUrl:
        """ Return the active media source being used """
        return self.currentMedia().canonicalUrl()

    def setSource(self, media: QUrl):
        """ Sets the current source """
        self.setMedia(QMediaContent(media))
