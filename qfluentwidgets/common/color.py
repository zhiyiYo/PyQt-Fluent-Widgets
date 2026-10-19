# coding: utf-8
from enum import Enum
import re

from PyQt5.QtGui import QColor

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


def blendColor(base: QColor, tint: QColor, strength: float) -> QColor:
    """ blend two colors towards `tint`, the alpha channel of `base` is preserved """
    strength = max(0, min(strength, 1))
    return QColor.fromRgb(
        round(base.red() * (1 - strength) + tint.red() * strength),
        round(base.green() * (1 - strength) + tint.green() * strength),
        round(base.blue() * (1 - strength) + tint.blue() * strength),
        base.alpha(),
    )


class ColorTinter:
    """ Blend the near-neutral surface colors towards a tint color """

    _colorPattern = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\([^()]*\)")
    _rgbPattern = re.compile(r"^rgba?\(([^()]*)\)$")
    _declarationPattern = re.compile(r"([-a-z]+)(\s*:\s*)([^;{}]+)")
    _maxSaturation = 0.18

    def __init__(self, color: QColor, strength: float):
        self.color = QColor(color)
        self.strength = max(0, min(strength, 1))

    def blend(self, color: QColor) -> QColor:
        """ blend the color with the tint color, the alpha channel is preserved """
        return blendColor(QColor(color), self.color, self.strength)

    def blendStyleSheet(self, qss: str) -> str:
        """ blend the near-neutral colors of surface properties in style sheet

        Only the colors of backgrounds and borders are blended, text colors
        and other properties are left untouched.
        """
        def blendDeclaration(m):
            prop, sep, value = m.groups()
            if not self._isSurfaceProperty(prop):
                return m.group(0)

            return prop + sep + self._colorPattern.sub(
                lambda c: self._blendColorText(c.group(0)), value)

        return self._declarationPattern.sub(blendDeclaration, qss)

    def _isSurfaceProperty(self, prop: str) -> bool:
        """ whether the style property declares a surface color """
        if prop.startswith("border"):
            return prop[len("border"):] in (
                "", "-color", "-top", "-right", "-bottom", "-left",
                "-top-color", "-right-color", "-bottom-color", "-left-color")

        return prop in ("background", "background-color", "gridline-color",
                        "alternate-background-color", "selection-background-color")

    def _blendColorText(self, colorText: str) -> str:
        """ blend the near-neutral color text, saturated colors are skipped """
        parsed = self._parseColorText(colorText)
        if parsed is None:
            return colorText

        color, alphaText = parsed
        if color.saturationF() > self._maxSaturation:
            return colorText

        blended = self.blend(color)

        if colorText.startswith("#"):
            if len(colorText) == 9:
                return blended.name(QColor.NameFormat.HexArgb)
            return blended.name(QColor.NameFormat.HexRgb)

        if alphaText is not None:
            return f"rgba({blended.red()}, {blended.green()}, {blended.blue()}, {alphaText})"
        return f"rgb({blended.red()}, {blended.green()}, {blended.blue()})"

    def _parseColorText(self, colorText: str):
        """ parse `#rgb` or `rgb(a)` color text """
        if colorText.startswith("#"):
            color = QColor(colorText)
            return (color, None) if color.isValid() else None

        match = self._rgbPattern.fullmatch(colorText)
        if match is None:
            return None

        parts = [p.strip() for p in match.group(1).split(",")]
        if len(parts) not in (3, 4):
            return None

        try:
            red, green, blue = (int(p) for p in parts[:3])
            rawAlpha = None if len(parts) == 3 else parts[3]
            alpha = 255 if rawAlpha is None else (
                int(rawAlpha) if "." not in rawAlpha else round(float(rawAlpha) * 255))
        except (TypeError, ValueError):
            return None

        if any(v < 0 or v > 255 for v in (red, green, blue, alpha)):
            return None

        return QColor.fromRgb(red, green, blue, alpha), rawAlpha
