# coding: utf-8
from enum import Enum

from PySide6.QtGui import QColor

from .style_sheet import themeColor, Theme, isDarkTheme
from .config import isDarkThemeMode


class FluentThemeColor(Enum):
    """ Fluent theme color

    Refer to: https://www.figma.com/file/iM7EPX8Jn37zjeSezb43cF
    """
    YELLOW_GOLD = "#FFB900"
    GOLD = "#FF8C00"
    ORANGE_BRIGHT = "#F7630C"
    ORANGE_DARK = "#CA5010"
    RUST = "#DA3B01"
    PALE_RUST = "#EF6950"
    BRICK_RED = "#D13438"
    MOD_RED = "#FF4343"
    PALE_RED = "#E74856"
    RED = "#E81123"
    ROSE_BRIGHT = "#EA005E"
    ROSE = "#C30052"
    PLUM_LIGHT = "#E3008C"
    PLUM = "#BF0077"
    ORCHID_LIGHT = "#BF0077"
    ORCHID = "#9A0089"
    DEFAULT_BLUE = "#0078D7"
    NAVY_BLUE = "#0063B1"
    PURPLE_SHADOW = "#8E8CD8"
    PURPLE_SHADOW_DARK = "#6B69D6"
    IRIS_PASTEL = "#8764B8"
    IRIS_SPRING = "#744DA9"
    VIOLET_RED_LIGHT = "#B146C2"
    VIOLET_RED = "#881798"
    COOL_BLUE_BRIGHT = "#0099BC"
    COOL_BLUR = "#2D7D9A"
    SEAFOAM = "#00B7C3"
    SEAFOAM_TEAL = "#038387"
    MINT_LIGHT = "#00B294"
    MINT_DARK = "#018574"
    TURF_GREEN = "#00CC6A"
    SPORT_GREEN = "#10893E"
    GRAY = "#7A7574"
    GRAY_BROWN = "#5D5A58"
    STEAL_BLUE = "#68768A"
    METAL_BLUE = "#515C6B"
    PALE_MOSS = "#567C73"
    MOSS = "#486860"
    MEADOW_GREEN = "#498205"
    GREEN = "#107C10"
    OVERCAST = "#767676"
    STORM = "#4C4A48"
    BLUE_GRAY = "#69797E"
    GRAY_DARK = "#4A5459"
    LIDDY_GREEN = "#647C64"
    SAGE = "#525E54"
    CAMOUFLAGE_DESERT = "#847545"
    CAMOUFLAGE = "#7E735F"

    def color(self):
        return QColor(self.value)



class FluentSystemColor(Enum):

    SUCCESS_FOREGROUND = ("#0f7b0f", "#6ccb5f")
    CAUTION_FOREGROUND = ("#9d5d00", "#fce100")
    CRITICAL_FOREGROUND = ("#c42b1c", "#ff99a4")

    SUCCESS_BACKGROUND = ("#dff6dd", "#393d1b")
    CAUTION_BACKGROUND = ("#fff4ce", "#433519")
    CRITICAL_BACKGROUND = ("#fde7e9", "#442726")

    def color(self, theme=Theme.AUTO) -> QColor:
        color = self.value[1] if isDarkThemeMode(theme) else self.value[0]
        return QColor(color)



def validColor(color: QColor, default: QColor) -> QColor:
    return color if color.isValid() else default


def fallbackThemeColor(color: QColor):
    return color if color.isValid() else themeColor()


def autoFallbackThemeColor(light: QColor, dark: QColor):
    color = dark if isDarkTheme() else light
    return fallbackThemeColor(color)
