# coding: utf-8
from qtpy.QtCore import QObject, Signal


class SignalBus(QObject):
    """ Signal bus """

    switchToSampleCard = Signal(str, int)


signalBus = SignalBus()