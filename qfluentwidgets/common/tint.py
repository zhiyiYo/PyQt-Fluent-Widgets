# coding: utf-8
import re

from PyQt5.QtGui import QColor


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
    _surfaceProperties = frozenset({
        # backgrounds
        "background", "background-color", "gridline-color",
        "alternate-background-color", "selection-background-color",
        # borders
        "border", "border-color",
        "border-top", "border-right", "border-bottom", "border-left",
        "border-top-color", "border-right-color", "border-bottom-color",
        "border-left-color",
    })

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
        if self.strength <= 0:
            return qss

        def blendDeclaration(m):
            prop, sep, value = m.groups()
            if not self._isSurfaceProperty(prop):
                return m.group(0)

            return prop + sep + self._colorPattern.sub(
                lambda c: self._blendColorText(c.group(0)), value)

        return self._declarationPattern.sub(blendDeclaration, qss)

    def _isSurfaceProperty(self, prop: str) -> bool:
        """ whether the style property declares a surface color """
        return prop in self._surfaceProperties

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
