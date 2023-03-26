# coding: utf-8
from PyQt6.QtCore import QObject


class Translator(QObject):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.basicInput = self.tr('Basic input')
        self.menus = self.tr('Menus')
        self.dialogs = self.tr('Dialogs')
        self.material = self.tr('Material')
        self.statusInfo = self.tr('Status & info')
        self.scroll = self.tr('Scrolling')
        self.layout = self.tr('Layout')