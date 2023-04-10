# coding: utf-8
from qtpy.QtWidgets import QCheckBox

from ...common.style_sheet import FluentStyleSheet


class CheckBox(QCheckBox):
    """ Check box """

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        FluentStyleSheet.CHECK_BOX.apply(self)
