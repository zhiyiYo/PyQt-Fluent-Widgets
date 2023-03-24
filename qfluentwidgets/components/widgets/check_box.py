# coding: utf-8
from PyQt6.QtWidgets import QCheckBox

from ...common.style_sheet import setStyleSheet


class CheckBox(QCheckBox):
    """ Check box """

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        setStyleSheet(self, 'check_box')
