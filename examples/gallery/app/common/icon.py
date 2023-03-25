# coding: utf-8
from enum import Enum

from qfluentwidgets import FluentIconBase, getIconColor, Theme


class Icon(FluentIconBase, Enum):

    HOME = "Home"
    CHAT = "Chat"
    MENU = "Menu"
    LAYOUT = "Layout"
    GITHUB = "Github"
    MESSAGE = "Message"
    CHECKBOX = "CheckBox"
    DOCUMENT = "Document"
    CONSTRACT = "Constract"

    def path(self, theme=Theme.AUTO):
        if theme == Theme.AUTO:
            c = getIconColor()
        else:
            c = "white" if theme == Theme.DARK else "black"

        return f"app/resource/images/icons/{self.value}_{c}.svg"
