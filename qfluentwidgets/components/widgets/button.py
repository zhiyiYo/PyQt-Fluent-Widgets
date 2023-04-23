# coding:utf-8
from typing import Union

from PyQt6.QtCore import QUrl, Qt, QRectF, QSize
from PyQt6.QtGui import QDesktopServices, QIcon, QPainter
from PyQt6.QtWidgets import QPushButton, QRadioButton, QToolButton, QApplication, QWidget

from ...common.icon import FluentIconBase, drawIcon, isDarkTheme, Theme
from ...common.style_sheet import FluentStyleSheet
from ...common.overload import singledispatchmethod


class PushButton(QPushButton):
    """ push button """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        FluentStyleSheet.BUTTON.apply(self)
        self.isPressed = False
        self.setIconSize(QSize(16, 16))
        self.setIcon(None)

    @__init__.register
    def _(self, text: str, parent: QWidget = None, icon: Union[QIcon, str, FluentIconBase] = None):
        self.__init__(parent=parent)
        self.setText(text)
        self.setIcon(icon)

    def setIcon(self, icon: Union[QIcon, str, FluentIconBase]):
        self.setProperty('hasIcon', icon is not None)
        self.setStyle(QApplication.style())
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
            painter.setOpacity(0.3628)
        elif self.isPressed:
            painter.setOpacity(0.786)

        w, h = self.iconSize().width(), self.iconSize().height()
        y = (self.height() - h) / 2
        mw = self.minimumSizeHint().width()
        if mw > 0:
            self._drawIcon(self._icon, painter, QRectF(12+(self.width()-mw)//2, y, w, h))
        else:
            self._drawIcon(self._icon, painter, QRectF(12, y, w, h))


class PrimaryPushButton(PushButton):
    """ Primary color push button """

    def _drawIcon(self, icon, painter, rect):
        if isinstance(icon, FluentIconBase) and self.isEnabled():
            # reverse icon color
            theme = Theme.DARK if not isDarkTheme() else Theme.LIGHT
            icon = icon.icon(theme)
        elif not self.isEnabled():
            painter.setOpacity(0.786 if isDarkTheme() else 0.9)
            icon = icon.icon(Theme.DARK)

        super()._drawIcon(icon, painter, rect)


class HyperlinkButton(QPushButton):
    """ Hyperlink button """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self.url = QUrl()
        FluentStyleSheet.BUTTON.apply(self)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.clicked.connect(lambda i: QDesktopServices.openUrl(self.url))

    @__init__.register
    def _(self, url: str, text: str, parent: QWidget = None):
        self.__init__(parent)
        self.setText(text)
        self.url.setUrl(url)


class RadioButton(QRadioButton):
    """ Radio button """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        FluentStyleSheet.BUTTON.apply(self)

    @__init__.register
    def _(self, text: str, parent: QWidget = None):
        self.__init__(parent)
        self.setText(text)


class ToolButton(QToolButton):
    """ Tool button """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        FluentStyleSheet.BUTTON.apply(self)
        self.isPressed = False
        self.setIcon(QIcon())

    @__init__.register
    def _(self, icon: FluentIconBase, parent: QWidget = None):
        self.__init__(parent)
        self.setIcon(icon)

    @__init__.register
    def _(self, icon: QIcon, parent: QWidget = None):
        self.__init__(parent)
        self.setIcon(icon)

    @__init__.register
    def _(self, icon: str, parent: QWidget = None):
        self.__init__(parent)
        self.setIcon(icon)

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
        x = (self.width() - w) / 2
        self._drawIcon(self._icon, painter, QRectF(x, y, w, h))


class TransparentToolButton(ToolButton):
    """ Transparent background tool button """
