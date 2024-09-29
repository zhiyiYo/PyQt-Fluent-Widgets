# coding:utf-8
from PyQt5.QtCore import QThread, pyqtSignal

from .config import Theme, qconfig
import darkdetect


class SystemThemeListener(QThread):
    """ System theme listener """

    systemThemeChanged = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def run(self):
        darkdetect.listener(self._onThemeChanged)

    def _onThemeChanged(self, theme: str):
        theme = Theme.DARK if theme.lower() == "dark" else Theme.LIGHT

        if qconfig.themeMode.value != Theme.AUTO or theme == qconfig.theme:
            return

        qconfig.theme = Theme.AUTO
        qconfig._cfg.themeChanged.emit(Theme.AUTO)
        self.systemThemeChanged.emit()