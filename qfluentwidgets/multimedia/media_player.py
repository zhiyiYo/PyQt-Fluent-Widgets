# coding:utf-8
from PySide6.QtCore import Qt, Signal, QObject, QUrl
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput


class MediaPlayerBase(QObject):
    """ Media player base class """

    mediaStatusChanged = Signal(QMediaPlayer.MediaStatus)
    playbackRateChanged = Signal(float)
    positionChanged = Signal(int)
    durationChanged = Signal(int)
    sourceChanged = Signal(QUrl)
    volumeChanged = Signal(int)
    mutedChanged = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def isPlaying(self):
        """ Whether the media is playing """
        raise NotImplementedError

    def mediaStatus(self) -> QMediaPlayer.MediaStatus:
        """ Return the status of the current media stream """
        raise NotImplementedError

    def playbackState(self) -> QMediaPlayer.PlaybackState:
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

    sourceChanged = Signal(QUrl)
    mutedChanged = Signal(bool)
    volumeChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._audioOutput = QAudioOutput(parent)
        self.setAudioOutput(self._audioOutput)

    def isPlaying(self):
        return self.playbackState() == QMediaPlayer.PlayingState

    def volume(self):
        """ Return the volume of player """
        return int(self.audioOutput().volume() * 100)

    def setVolume(self, volume: int):
        """ Sets the volume of player """
        if volume == self.volume():
            return

        self.audioOutput().setVolume(volume / 100)
        self.volumeChanged.emit(volume)

    def setMuted(self, isMuted: bool):
        if isMuted == self.audioOutput().isMuted():
            return

        self.audioOutput().setMuted(isMuted)
        self.mutedChanged.emit(isMuted)