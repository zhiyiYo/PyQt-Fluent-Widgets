# coding:utf-8
from typing import Union

from PyQt6.QtCore import QUrl, Qt, QRectF, QSize
from PyQt6.QtGui import QDesktopServices, QIcon, QPainter
from PyQt6.QtWidgets import QPushButton, QRadioButton, QToolButton

from ...common.icon import FluentIconBase, drawIcon, isDarkTheme, Theme
from ...common.style_sheet import setStyleSheet


class PushButton(QPushButton):
    """ push button """

    def __init__(self, text: str, parent=None, icon: Union[QIcon, str, FluentIconBase] = None):
        super().__init__(text=text, parent=parent)
        setStyleSheet(self, 'button')
        self._icon = icon
        self.isPressed = False
        self.setProperty('hasIcon', icon is not None)
        self.setIconSize(QSize(16, 16))

    def setIcon(self, icon: Union[QIcon, str, FluentIconBase]):
        self._icon = icon
        self.update()

    def icon(self):
        if isinstance(self._icon, str):
            return QIcon(self._icon)
        if isinstance(self._icon, FluentIconBase):
            return self._icon.icon()

        return self._icon

    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)

    def _drawIcon(self, icon, painter, rect):
        """ draw icon """
        drawIcon(icon, painter, rect)

    def paintEvent(self, e):
        super().paintEvent(e)
        if self._icon is None:
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing |
                               QPainter.RenderHint.SmoothPixmapTransform)

        if not self.isEnabled():
            painter.setOpacity(0.43)
        elif self.isPressed:
            painter.setOpacity(0.63)

        w, h = self.iconSize().width(), self.iconSize().height()
        y = (self.height() - h) / 2
        self._drawIcon(self._icon, painter, QRectF(12, y, w, h))


class PrimaryPushButton(PushButton):
    """ Primary color push button """

    def _drawIcon(self, icon, painter, rect):
        if isinstance(icon, FluentIconBase) and self.isEnabled():
            # reverse icon color
            theme = Theme.DARK if not isDarkTheme() else Theme.LIGHT
            icon = icon.icon(theme)
        elif not self.isEnabled():
            painter.setOpacity(0.63 if isDarkTheme() else 0.9)
            icon = icon.icon(Theme.DARK)

        super()._drawIcon(icon, painter, rect)


class HyperlinkButton(QPushButton):
    """ Hyperlink button """

    def __init__(self, url: str, text: str, parent=None):
        super().__init__(text, parent)
        self.url = QUrl(url)
        self.clicked.connect(lambda i: QDesktopServices.openUrl(self.url))
        setStyleSheet(self, 'button')
        self.setCursor(Qt.CursorShape.PointingHandCursor)


class RadioButton(QRadioButton):
    """ Radio button """

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)
        setStyleSheet(self, 'button')


class ToolButton(QToolButton):
    """ Tool button """

    def __init__(self, icon: Union[QIcon, str, FluentIconBase], parent=None):
        super().__init__(parent)
        self._icon = icon
        self.isPressed = False
        setStyleSheet(self, 'button')

    def setIcon(self, icon: Union[QIcon, str, FluentIconBase]):
        self._icon = icon
        self.update()

    def icon(self):
        if isinstance(self._icon, str):
            return QIcon(self._icon)
        if isinstance(self._icon, FluentIconBase):
            return self._icon.icon()

        return self._icon

    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)

    def _drawIcon(self, icon, painter, rect):
        """ draw icon """
        drawIcon(icon, painter, rect)

    def paintEvent(self, e):
        super().paintEvent(e)
        if self._icon is None:
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing |
                               QPainter.RenderHint.SmoothPixmapTransform)

        if not self.isEnabled():
            painter.setOpacity(0.43)
        elif self.isPressed:
            painter.setOpacity(0.63)

        w, h = self.iconSize().width(), self.iconSize().height()
        y = (self.height() - h) / 2
        x  = (self.width() - w) / 2
        self._drawIcon(self._icon, painter, QRectF(x, y, w, h))
