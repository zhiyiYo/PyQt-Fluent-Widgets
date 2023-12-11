from PySide2.QtCore import QPoint, QRect
from PySide2.QtGui import QCursor
from PySide2.QtWidgets import QApplication


def getCurrentScreen():
    """ get current screen """
    cursorPos = QCursor.pos()

    for s in QApplication.screens():
        if s.geometry().contains(cursorPos):
            return s

    return None


def getCurrentScreenGeometry(avaliable=True):
    """ get current screen geometry """
    screen = getCurrentScreen() or QApplication.primaryScreen()

    # this should not happen
    if not screen:
        return QRect(0, 0, 1920, 1080)

    return screen.availableGeometry() if avaliable else screen.geometry()