# coding: utf-8
from enum import Enum

from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QCheckBox, QStyle, QStyleOptionButton, QWidget

from ...common.icon import FluentIconBase, Theme, getIconColor
from ...common.style_sheet import FluentStyleSheet, isDarkTheme, ThemeColor, themeColor
from ...common.overload import singledispatchmethod


class CheckBoxIcon(FluentIconBase, Enum):
    """ CheckBoxIcon """

    ACCEPT = "Accept"
    PARTIAL_ACCEPT = "PartialAccept"

    def path(self, theme=Theme.AUTO):
        c = getIconColor(theme, reverse=True)
        return f':/qfluentwidgets/images/check_box/{self.value}_{c}.svg'


class CheckBoxState(Enum):
    """ Check box state """

    NORMAL = 0
    HOVER = 1
    PRESSED = 2
    CHECKED = 3
    CHECKED_HOVER = 4
    CHECKED_PRESSED = 5
    DISABLED = 6
    CHECKED_DISABLED = 7


class CheckBox(QCheckBox):
    """ Check box

    Constructors
    ------------
    * CheckBox(`parent`: QWidget = None)
    * CheckBox(`text`: str, `parent`: QWidget = None)
    """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        FluentStyleSheet.CHECK_BOX.apply(self)
        self.isPressed = False
        self.isHover = False

        self._states = {}

    @__init__.register
    def _(self, text: str, parent: QWidget = None):
        self.__init__(parent)
        self.setText(text)

    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)

    def enterEvent(self, e):
        self.isHover = True
        self.update()

    def leaveEvent(self, e):
        self.isHover = False
        self.update()

    def _borderColor(self):
        if isDarkTheme():
            map = {
                CheckBoxState.NORMAL: QColor(255, 255, 255, 141),
                CheckBoxState.HOVER: QColor(255, 255, 255, 141),
                CheckBoxState.PRESSED: QColor(255, 255, 255, 40),
                CheckBoxState.CHECKED : themeColor(),
                CheckBoxState.CHECKED_HOVER : ThemeColor.DARK_1.color(),
                CheckBoxState.CHECKED_PRESSED : ThemeColor.DARK_2.color(),
                CheckBoxState.DISABLED : QColor(255, 255, 255, 41),
                CheckBoxState.CHECKED_DISABLED : QColor(0, 0, 0, 0)
            }
        else:
            map = {
                CheckBoxState.NORMAL: QColor(0, 0, 0, 122),
                CheckBoxState.HOVER: QColor(0, 0, 0, 143),
                CheckBoxState.PRESSED: QColor(0, 0, 0, 69),
                CheckBoxState.CHECKED : themeColor(),
                CheckBoxState.CHECKED_HOVER : ThemeColor.LIGHT_1.color(),
                CheckBoxState.CHECKED_PRESSED : ThemeColor.LIGHT_2.color(),
                CheckBoxState.DISABLED : QColor(0, 0, 0, 56),
                CheckBoxState.CHECKED_DISABLED : QColor(0, 0, 0, 0)
            }

        return map[self._state()]

    def _backgroundColor(self):
        if isDarkTheme():
            map = {
                CheckBoxState.NORMAL: QColor(0, 0, 0, 26),
                CheckBoxState.HOVER: QColor(255, 255, 255, 11),
                CheckBoxState.PRESSED: QColor(255, 255, 255, 18),
                CheckBoxState.CHECKED: themeColor(),
                CheckBoxState.CHECKED_HOVER: ThemeColor.DARK_1.color(),
                CheckBoxState.CHECKED_PRESSED: ThemeColor.DARK_2.color(),
                CheckBoxState.DISABLED: QColor(0, 0, 0, 0),
                CheckBoxState.CHECKED_DISABLED: QColor(255, 255, 255, 41)
            }
        else:
            map = {
                CheckBoxState.NORMAL: QColor(0, 0, 0, 6),
                CheckBoxState.HOVER: QColor(0, 0, 0, 13),
                CheckBoxState.PRESSED: QColor(0, 0, 0, 31),
                CheckBoxState.CHECKED: themeColor(),
                CheckBoxState.CHECKED_HOVER: ThemeColor.LIGHT_1.color(),
                CheckBoxState.CHECKED_PRESSED: ThemeColor.LIGHT_2.color(),
                CheckBoxState.DISABLED: QColor(0, 0, 0, 0),
                CheckBoxState.CHECKED_DISABLED: QColor(0, 0, 0, 56)
            }

        return map[self._state()]

    def _state(self):
        if not self.isEnabled():
            return CheckBoxState.CHECKED_DISABLED if self.isChecked() else CheckBoxState.DISABLED

        if self.isChecked():
            if self.isPressed:
                return CheckBoxState.CHECKED_PRESSED
            if self.isHover:
                return CheckBoxState.CHECKED_HOVER

            return CheckBoxState.CHECKED
        else:
            if self.isPressed:
                return CheckBoxState.PRESSED
            if self.isHover:
                return CheckBoxState.HOVER

            return CheckBoxState.NORMAL

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        # get the rect of indicator
        opt = QStyleOptionButton()
        opt.initFrom(self)
        rect = self.style().subElementRect(QStyle.SE_CheckBoxIndicator, opt, self)

        # draw shape
        painter.setPen(self._borderColor())
        painter.setBrush(self._backgroundColor())
        painter.drawRoundedRect(rect, 4.5, 4.5)

        if not self.isEnabled():
            painter.setOpacity(0.8)

        # draw icon
        if self.checkState() == Qt.Checked:
            CheckBoxIcon.ACCEPT.render(painter, rect)
        elif self.checkState() == Qt.PartiallyChecked:
            CheckBoxIcon.PARTIAL_ACCEPT.render(painter, rect)
