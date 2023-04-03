# coding: utf-8
from qtpy.QtCore import QObject, pyqtSignal


class SignalBus(QObject):
    """ Signal bus """

    switchToSampleCard = pyqtSignal(str, int)


signalBus = SignalBus()