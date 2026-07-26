from typing import Optional

from PySide6.QtCore import QTranslator, QLocale


class FluentTranslator(QTranslator):
    """Translator of fluent widgets"""

    def __init__(self, locale: Optional[QLocale] = None, parent=None):
        super().__init__(parent=parent)
        self._load(locale or QLocale())

    def _load(self, locale: QLocale):
        """load translation file"""
        super().load(f':/qfluentwidgets/i18n/qfluentwidgets.{locale.name()}.qm')
