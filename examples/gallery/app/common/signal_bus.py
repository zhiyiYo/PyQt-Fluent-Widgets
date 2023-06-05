# coding: utf-8
from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):
    """ Signal bus """

    switchToSampleCard = Signal(str, int)
    supportSignal = Signal()


signalBus = SignalBus()