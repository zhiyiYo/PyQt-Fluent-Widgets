from typing import Optional

from PySide6.QtCore import QRect
from PySide6.QtGui import QCursor, QScreen
from PySide6.QtWidgets import QApplication


def getCurrentScreen() -> Optional[QScreen]:
    """get current screen"""
    cursorPos = QCursor.pos()

    for s in QApplication.screens():
        if s.geometry().contains(cursorPos):
            return s

    return None


def getCurrentScreenGeometry(available: bool = True) -> QRect:
    """get current screen geometry"""
    screen = getCurrentScreen() or QApplication.primaryScreen()

    # this should not happen
    if not screen:
        return QRect(0, 0, 1920, 1080)

    return screen.availableGeometry() if available else screen.geometry()
