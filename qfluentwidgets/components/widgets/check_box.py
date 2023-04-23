# coding: utf-8
from PyQt6.QtWidgets import QCheckBox, QWidget

from ...common.style_sheet import FluentStyleSheet
from ...common.overload import singledispatchmethod


class CheckBox(QCheckBox):
    """ Check box """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        FluentStyleSheet.CHECK_BOX.apply(self)

    @__init__.register
    def _(self, text: str, parent: QWidget = None):
        super().__init__(text, parent)
        FluentStyleSheet.CHECK_BOX.apply(self)
