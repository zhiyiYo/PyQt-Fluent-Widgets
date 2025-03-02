# coding:utf-8
from .acrylic_menu import AcrylicCompleterMenu, AcrylicLineEditMenu
from ..widgets.line_edit import LineEdit, SearchLineEdit


class AcrylicLineEditBase:
    """ Acrylic line edit base """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def setCompleter(self, completer):
        super().setCompleter(completer)
        self.setCompleterMenu(AcrylicCompleterMenu(self))

    def contextMenuEvent(self, e):
        menu = AcrylicLineEditMenu(self)
        menu.exec(e.globalPos())



class AcrylicLineEdit(AcrylicLineEditBase, LineEdit):
    """ Acrylic line edit """


class AcrylicSearchLineEdit(AcrylicLineEditBase, SearchLineEdit):
    """ Acrylic search line edit """
