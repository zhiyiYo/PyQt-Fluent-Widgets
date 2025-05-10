# coding:utf-8
from typing import Union

from PySide2.QtCore import Signal, QUrl, Qt, QRectF, QSize, QPoint, Property, QRect
from PySide2.QtGui import QDesktopServices, QIcon, QPainter, QColor, QPainterPath
from PySide2.QtWidgets import QHBoxLayout, QPushButton, QRadioButton, QToolButton, QApplication, QWidget, QSizePolicy

from ...common.animation import TranslateYAnimation
from ...common.icon import FluentIconBase, drawIcon, isDarkTheme, Theme, toQIcon, Icon
from ...common.icon import FluentIcon as FIF
from ...common.font import setFont, getFont
from ...common.style_sheet import FluentStyleSheet, themeColor, ThemeColor
from ...common.color import autoFallbackThemeColor
from ...common.overload import singledispatchmethod
from .menu import RoundMenu, MenuAnimationType


class PushButton(QPushButton):
    """ Push button

    Constructors
    ------------
    * PushButton(`parent`: QWidget = None)
    * PushButton(`text`: str, `parent`: QWidget = None, `icon`: QIcon | str | FluentIconBase = None)
    * PushButton(`icon`: QIcon | FluentIcon, `text`: str, `parent`: QWidget = None)
    """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        FluentStyleSheet.BUTTON.apply(self)
        self.isPressed = False
        self.isHover = False
        self.setIconSize(QSize(16, 16))
        self.setIcon(None)
        setFont(self)
        self._postInit()

    @__init__.register
    def _(self, text: str, parent: QWidget = None, icon: Union[QIcon, str, FluentIconBase] = None):
        self.__init__(parent=parent)
        self.setText(text)
        self.setIcon(icon)

    @__init__.register
    def _(self, icon: QIcon, text: str, parent: QWidget = None):
        self.__init__(text, parent, icon)

    @__init__.register
    def _(self, icon: FluentIconBase, text: str, parent: QWidget = None):
        self.__init__(text, parent, icon)

    def _postInit(self):
        pass

    def setIcon(self, icon: Union[QIcon, str, FluentIconBase]):
        self.setProperty('hasIcon', icon is not None)
        self.setStyle(QApplication.style())
        self._icon = icon or QIcon()
        self.update()

    def icon(self):
        return toQIcon(self._icon)

    def setProperty(self, name: str, value) -> bool:
        if name != 'icon':
            return super().setProperty(name, value)

        self.setIcon(value)
        return True

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

    def _drawIcon(self, icon, painter, rect, state=QIcon.Off):
        """ draw icon """
        drawIcon(icon, painter, rect, state)

    def paintEvent(self, e):
        super().paintEvent(e)
        if self.icon().isNull():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)

        if not self.isEnabled():
            painter.setOpacity(0.3628)
        elif self.isPressed:
            painter.setOpacity(0.786)

        w, h = self.iconSize().width(), self.iconSize().height()
        y = (self.height() - h) / 2
        mw = self.minimumSizeHint().width()
        if mw > 0:
            x = 12 + (self.width() - mw) // 2
        else:
            x = 12

        if self.isRightToLeft():
            x = self.width() - w - x

        self._drawIcon(self._icon, painter, QRectF(x, y, w, h))


class PrimaryPushButton(PushButton):
    """ Primary color push button

    Constructors
    ------------
    * PrimaryPushButton(`parent`: QWidget = None)
    * PrimaryPushButton(`text`: str, `parent`: QWidget = None, `icon`: QIcon | str | FluentIconBase = None)
    * PrimaryPushButton(`icon`: QIcon | FluentIcon, `text`: str, `parent`: QWidget = None)
    """

    def _drawIcon(self, icon, painter, rect, state=QIcon.Off):
        if isinstance(icon, FluentIconBase) and self.isEnabled():
            # reverse icon color
            theme = Theme.DARK if not isDarkTheme() else Theme.LIGHT
            icon = icon.icon(theme)
        elif not self.isEnabled():
            painter.setOpacity(0.786 if isDarkTheme() else 0.9)
            if isinstance(icon, FluentIconBase):
                icon = icon.icon(Theme.DARK)

        PushButton._drawIcon(self, icon, painter, rect, state)


class TransparentPushButton(PushButton):
    """ Transparent push button

    Constructors
    ------------
    * TransparentPushButton(`parent`: QWidget = None)
    * TransparentPushButton(`text`: str, `parent`: QWidget = None, `icon`: QIcon | str | FluentIconBase = None)
    * TransparentPushButton(`icon`: QIcon | FluentIcon, `text`: str, `parent`: QWidget = None)
    """


class ToggleButton(PushButton):
    """ Toggle push button

    Constructors
    ------------
    * ToggleButton(`parent`: QWidget = None)
    * ToggleButton(`text`: str, `parent`: QWidget = None, `icon`: QIcon | str | FluentIconBase = None)
    * ToggleButton(`icon`: QIcon | FluentIcon, `text`: str, `parent`: QWidget = None)
    """

    def _postInit(self):
        self.setCheckable(True)
        self.setChecked(False)

    def _drawIcon(self, icon, painter, rect):
        if not self.isChecked():
            return PushButton._drawIcon(self, icon, painter, rect)

        PrimaryPushButton._drawIcon(self, icon, painter, rect, QIcon.On)


TogglePushButton = ToggleButton


class TransparentTogglePushButton(TogglePushButton):
    """ Transparent toggle push button

    Constructors
    ------------
    * TransparentTogglePushButton(`parent`: QWidget = None)
    * TransparentTogglePushButton(`text`: str, `parent`: QWidget = None,
                                  `icon`: QIcon | str | FluentIconBase = None)
    * TransparentTogglePushButton(`icon`: QIcon | FluentIconBase, `text`: str, `parent`: QWidget = None)
    """


class HyperlinkButton(PushButton):
    """ Hyperlink button

    Constructors
    ------------
    * HyperlinkButton(`parent`: QWidget = None)
    * HyperlinkButton(`url`: str, `text`: str, `parent`: QWidget = None, `icon`: QIcon | str | FluentIconBase = None)
    * HyperlinkButton(`icon`: QIcon | FluentIconBase, `url`: str, `text`: str, `parent`: QWidget = None)
    """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._url = QUrl()
        FluentStyleSheet.BUTTON.apply(self)
        self.setCursor(Qt.PointingHandCursor)
        setFont(self)
        self.clicked.connect(self._onClicked)

    @__init__.register
    def _(self, url: str, text: str, parent: QWidget = None, icon: Union[QIcon, FluentIconBase, str] = None):
        self.__init__(parent)
        self.setText(text)
        self.url.setUrl(url)
        self.setIcon(icon)

    @__init__.register
    def _(self, icon: QIcon, url: str, text: str, parent: QWidget = None):
        self.__init__(url, text, parent, icon)

    @__init__.register
    def _(self, icon: FluentIconBase, url: str, text: str, parent: QWidget = None):
        self.__init__(url, text, parent, icon)

    def getUrl(self):
        return self._url

    def setUrl(self, url: Union[str, QUrl]):
        self._url = QUrl(url)

    def _onClicked(self):
        if self.getUrl().isValid():
            QDesktopServices.openUrl(self.getUrl())

    def _drawIcon(self, icon, painter, rect, state=QIcon.Off):
        if isinstance(icon, FluentIconBase) and self.isEnabled():
            icon = icon.icon(color=themeColor())
        elif not self.isEnabled():
            painter.setOpacity(0.3628 if isDarkTheme() else 0.36)

        drawIcon(icon, painter, rect, state)

    url = Property(QUrl, getUrl, setUrl)


class RadioButton(QRadioButton):
    """ Radio button

    Constructors
    ------------
    * RadioButton(`parent`: QWidget = None)
    * RadioButton(`url`: text, `text`: str, `parent`: QWidget = None,
                  `icon`: QIcon | str | FluentIconBase = None)
    """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        self._lightTextColor = QColor(0, 0, 0)
        self._darkTextColor = QColor(255, 255, 255)
        self.lightIndicatorColor = QColor()
        self.darkIndicatorColor = QColor()
        self.indicatorPos = QPoint(11, 12)
        self.isHover = False

        FluentStyleSheet.BUTTON.apply(self)
        self.setAttribute(Qt.WA_MacShowFocusRect, False)
        self._postInit()

    @__init__.register
    def _(self, text: str, parent: QWidget = None):
        self.__init__(parent)
        self.setText(text)

    def _postInit(self):
        pass

    def enterEvent(self, e):
        self.isHover = True
        self.update()

    def leaveEvent(self, e):
        self.isHover = False
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        self._drawIndicator(painter)
        self._drawText(painter)

    def _drawText(self, painter: QPainter):
        if not self.isEnabled():
            painter.setOpacity(0.36)

        painter.setFont(self.font())
        painter.setPen(self.textColor())
        painter.drawText(QRect(29, 0, self.width(), self.height()), Qt.AlignVCenter, self.text())

    def _drawIndicator(self, painter: QPainter):
        if self.isChecked():
            if self.isEnabled():
                borderColor = autoFallbackThemeColor(self.lightIndicatorColor, self.darkIndicatorColor)
            else:
                borderColor = QColor(255, 255, 255, 40) if isDarkTheme() else QColor(0, 0, 0, 55)

            filledColor = Qt.black if isDarkTheme() else Qt.white

            if self.isHover and not self.isDown():
                self._drawCircle(painter, self.indicatorPos, 10, 4, borderColor, filledColor)
            else:
                self._drawCircle(painter, self.indicatorPos, 10, 5, borderColor, filledColor)

        else:
            if self.isEnabled():
                if not self.isDown():
                    borderColor = QColor(255, 255, 255, 153) if isDarkTheme() else QColor(0, 0, 0, 153)
                else:
                    borderColor = QColor(255, 255, 255, 40) if isDarkTheme() else QColor(0, 0, 0, 55)

                if self.isDown():
                    filledColor = Qt.black if isDarkTheme() else Qt.white
                elif self.isHover:
                    filledColor = QColor(255, 255, 255, 11) if isDarkTheme() else QColor(0, 0, 0, 15)
                else:
                    filledColor = QColor(0, 0, 0, 26) if isDarkTheme() else QColor(0, 0, 0, 6)
            else:
                filledColor = Qt.transparent
                borderColor = QColor(255, 255, 255, 40) if isDarkTheme() else QColor(0, 0, 0, 55)

            self._drawCircle(painter, self.indicatorPos, 10, 1, borderColor, filledColor)

            if self.isEnabled() and self.isDown():
                borderColor = QColor(255, 255, 255, 40) if isDarkTheme() else QColor(0, 0, 0, 24)
                self._drawCircle(painter, self.indicatorPos, 9, 4, borderColor, Qt.transparent)

    def _drawCircle(self, painter: QPainter, center: QPoint, radius, thickness, borderColor, filledColor):
        path = QPainterPath()
        path.setFillRule(Qt.FillRule.WindingFill)

        # outer circle (border)
        outerRect = QRectF(center.x() - radius, center.y() - radius, 2 * radius, 2 * radius)
        path.addEllipse(outerRect)

        # inner center (filled)
        ir = radius - thickness
        innerRect = QRectF(center.x() - ir, center.y() - ir, 2 * ir, 2 * ir)
        innerPath = QPainterPath()
        innerPath.addEllipse(innerRect)

        path = path.subtracted(innerPath)

        # draw outer ring
        painter.setPen(Qt.NoPen)
        painter.fillPath(path, borderColor)

        # fill inner circle
        painter.fillPath(innerPath, filledColor)

    def textColor(self):
        return self.darkTextColor if isDarkTheme() else self.lightTextColor

    def getLightTextColor(self) -> QColor:
        return self._lightTextColor

    def getDarkTextColor(self) -> QColor:
        return self._darkTextColor

    def setLightTextColor(self, color: QColor):
        self._lightTextColor = QColor(color)
        self.update()

    def setDarkTextColor(self, color: QColor):
        self._darkTextColor = QColor(color)
        self.update()

    def setIndicatorColor(self, light, dark):
        self.lightIndicatorColor = QColor(light)
        self.darkIndicatorColor = QColor(dark)
        self.update()

    def setTextColor(self, light, dark):
        self.setLightTextColor(light)
        self.setDarkTextColor(dark)

    lightTextColor = Property(QColor, getLightTextColor, setLightTextColor)
    darkTextColor = Property(QColor, getDarkTextColor, setDarkTextColor)


class ToolButton(QToolButton):
    """ Tool button

    Constructors
    ------------
    * ToolButton(`parent`: QWidget = None)
    * ToolButton(`icon`: QIcon | str | FluentIconBase, `parent`: QWidget = None)
    """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent)
        FluentStyleSheet.BUTTON.apply(self)
        self.isPressed = False
        self.isHover = False
        self.setIconSize(QSize(16, 16))
        self.setIcon(QIcon())
        setFont(self)
        self._postInit()

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

    def _postInit(self):
        pass

    def setIcon(self, icon: Union[QIcon, str, FluentIconBase]):
        self._icon = icon
        self.update()

    def icon(self):
        return toQIcon(self._icon)

    def setProperty(self, name: str, value) -> bool:
        if name != 'icon':
            return super().setProperty(name, value)

        self.setIcon(value)
        return True

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

    def _drawIcon(self, icon, painter: QPainter, rect: QRectF, state=QIcon.Off):
        """ draw icon """
        drawIcon(icon, painter, rect, state)

    def paintEvent(self, e):
        super().paintEvent(e)
        if self._icon is None:
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)

        if not self.isEnabled():
            painter.setOpacity(0.43)
        elif self.isPressed:
            painter.setOpacity(0.63)

        w, h = self.iconSize().width(), self.iconSize().height()
        y = (self.height() - h) / 2
        x = (self.width() - w) / 2
        self._drawIcon(self._icon, painter, QRectF(x, y, w, h))


class TransparentToolButton(ToolButton):
    """ Transparent background tool button

    Constructors
    ------------
    * TransparentToolButton(`parent`: QWidget = None)
    * TransparentToolButton(`icon`: QIcon | str | FluentIconBase, `parent`: QWidget = None)
    """


class PrimaryToolButton(ToolButton):
    """ Primary color tool button

    Constructors
    ------------
    * PrimaryToolButton(`parent`: QWidget = None)
    * PrimaryToolButton(`icon`: QIcon | str | FluentIconBase, `parent`: QWidget = None)
    """

    def _drawIcon(self, icon, painter: QPainter, rect: QRectF, state=QIcon.Off):
        if isinstance(icon, FluentIconBase) and self.isEnabled():
            # reverse icon color
            theme = Theme.DARK if not isDarkTheme() else Theme.LIGHT
            icon = icon.icon(theme)
        elif isinstance(icon, Icon) and self.isEnabled():
            theme = Theme.DARK if not isDarkTheme() else Theme.LIGHT
            icon = icon.fluentIcon.icon(theme)
        elif not self.isEnabled():
            painter.setOpacity(0.786 if isDarkTheme() else 0.9)
            if isinstance(icon, FluentIconBase):
                icon = icon.icon(Theme.DARK)

        return drawIcon(icon, painter, rect, state)


class ToggleToolButton(ToolButton):
    """ Toggle tool button

    Constructors
    ------------
    * ToggleToolButton(`parent`: QWidget = None)
    * ToggleToolButton(`icon`: QIcon | str | FluentIconBase, `parent`: QWidget = None)
    """

    def _postInit(self):
        self.setCheckable(True)
        self.setChecked(False)

    def _drawIcon(self, icon, painter, rect):
        if not self.isChecked():
            return ToolButton._drawIcon(self, icon, painter, rect)

        PrimaryToolButton._drawIcon(self, icon, painter, rect, QIcon.On)


class TransparentToggleToolButton(ToggleToolButton):
    """ Transparent toggle tool button

    Constructors
    ------------
    * TransparentToggleToolButton(`parent`: QWidget = None)
    * TransparentToggleToolButton(`icon`: QIcon | str | FluentIconBase, `parent`: QWidget = None)
    """


class DropDownButtonBase:
    """ Drop down button base class """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._menu = None
        self.arrowAni = TranslateYAnimation(self)

    def setMenu(self, menu: RoundMenu):
        self._menu = menu

    def menu(self) -> RoundMenu:
        return self._menu

    def _showMenu(self):
        if not self.menu():
            return

        menu = self.menu()
        menu.view.setMinimumWidth(self.width())
        menu.view.adjustSize()
        menu.adjustSize()

        # determine the animation type by choosing the maximum height of view
        x = -menu.width()//2 + menu.layout().contentsMargins().left() + self.width()//2
        pd = self.mapToGlobal(QPoint(x, self.height()))
        hd = menu.view.heightForAnimation(pd, MenuAnimationType.DROP_DOWN)

        pu = self.mapToGlobal(QPoint(x, 0))
        hu = menu.view.heightForAnimation(pu, MenuAnimationType.PULL_UP)

        if hd >= hu:
            menu.view.adjustSize(pd, MenuAnimationType.DROP_DOWN)
            menu.exec(pd, aniType=MenuAnimationType.DROP_DOWN)
        else:
            menu.view.adjustSize(pu, MenuAnimationType.PULL_UP)
            menu.exec(pu, aniType=MenuAnimationType.PULL_UP)

    def _hideMenu(self):
        if self.menu():
            self.menu().hide()

    def _drawDropDownIcon(self, painter, rect):
        if isDarkTheme():
            FIF.ARROW_DOWN.render(painter, rect)
        else:
            FIF.ARROW_DOWN.render(painter, rect, fill="#646464")

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        if self.isHover:
            painter.setOpacity(0.8)
        elif self.isPressed:
            painter.setOpacity(0.7)

        rect = QRectF(self.width()-22, self.height() /
                      2-5+self.arrowAni.y, 10, 10)
        self._drawDropDownIcon(painter, rect)


class DropDownPushButton(DropDownButtonBase, PushButton):
    """ Drop down push button

    Constructors
    ------------
    * DropDownPushButton(`parent`: QWidget = None)
    * DropDownPushButton(`text`: str, `parent`: QWidget = None,
                         `icon`: QIcon | str | FluentIconBase = None)
    * DropDownPushButton(`icon`: QIcon | FluentIcon, `text`: str, `parent`: QWidget = None)
    """

    def mouseReleaseEvent(self, e):
        PushButton.mouseReleaseEvent(self, e)
        self._showMenu()

    def paintEvent(self, e):
        PushButton.paintEvent(self, e)
        DropDownButtonBase.paintEvent(self, e)


class TransparentDropDownPushButton(DropDownPushButton):
    """ Transparent drop down push button

    Constructors
    ------------
    * TransparentDropDownPushButton(`parent`: QWidget = None)
    * TransparentDropDownPushButton(`text`: str, `parent`: QWidget = None,
                                    `icon`: QIcon | str | FluentIconBase = None)
    * TransparentDropDownPushButton(`icon`: QIcon | FluentIcon, `text`: str, `parent`: QWidget = None)
    """


class DropDownToolButton(DropDownButtonBase, ToolButton):
    """ Drop down tool button

    Constructors
    ------------
    * DropDownToolButton(`parent`: QWidget = None)
    * DropDownToolButton(`icon`: QIcon | str | FluentIconBase, `parent`: QWidget = None)
    """

    def mouseReleaseEvent(self, e):
        ToolButton.mouseReleaseEvent(self, e)
        self._showMenu()

    def _drawIcon(self, icon, painter, rect: QRectF):
        rect.moveLeft(12)
        return super()._drawIcon(icon, painter, rect)

    def paintEvent(self, e):
        ToolButton.paintEvent(self, e)
        DropDownButtonBase.paintEvent(self, e)


class TransparentDropDownToolButton(DropDownToolButton):
    """ Transparent drop down tool button

    Constructors
    ------------
    * TransparentDropDownToolButton(`parent`: QWidget = None)
    * TransparentDropDownToolButton(`icon`: QIcon | str | FluentIconBase, `parent`: QWidget = None)
    """


class PrimaryDropDownButtonBase(DropDownButtonBase):
    """ Primary color drop down button base class """

    def _drawDropDownIcon(self, painter, rect):
        theme = Theme.DARK if not isDarkTheme() else Theme.LIGHT
        FIF.ARROW_DOWN.render(painter, rect, theme)


class PrimaryDropDownPushButton(PrimaryDropDownButtonBase, PrimaryPushButton):
    """ Primary color drop down push button

    Constructors
    ------------
    * PrimaryDropDownPushButton(`parent`: QWidget = None)
    * PrimaryDropDownPushButton(`text`: str, `parent`: QWidget = None,
                                `icon`: QIcon | str | FluentIconBase = None)
    * PrimaryDropDownPushButton(`icon`: QIcon | FluentIcon, `text`: str, `parent`: QWidget = None)
    """

    def mouseReleaseEvent(self, e):
        PrimaryPushButton.mouseReleaseEvent(self, e)
        self._showMenu()

    def paintEvent(self, e):
        PrimaryPushButton.paintEvent(self, e)
        PrimaryDropDownButtonBase.paintEvent(self, e)


class PrimaryDropDownToolButton(PrimaryDropDownButtonBase, PrimaryToolButton):
    """ Primary drop down tool button

    Constructors
    ------------
    * PrimaryDropDownToolButton(`parent`: QWidget = None)
    * PrimaryDropDownToolButton(`icon`: QIcon | str | FluentIconBase, `parent`: QWidget = None)
    """

    def mouseReleaseEvent(self, e):
        PrimaryToolButton.mouseReleaseEvent(self, e)
        self._showMenu()

    def _drawIcon(self, icon, painter, rect: QRectF):
        rect.moveLeft(12)
        return super()._drawIcon(icon, painter, rect)

    def paintEvent(self, e):
        PrimaryToolButton.paintEvent(self, e)
        PrimaryDropDownButtonBase.paintEvent(self, e)


class SplitDropButton(ToolButton):

    def _postInit(self):
        self.arrowAni = TranslateYAnimation(self)
        self.setIcon(FIF.ARROW_DOWN)
        self.setIconSize(QSize(10, 10))
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

    def _drawIcon(self, icon, painter, rect):
        rect.translate(0, self.arrowAni.y)

        if self.isPressed:
            painter.setOpacity(0.5)
        elif self.isHover:
            painter.setOpacity(1)
        else:
            painter.setOpacity(0.63)

        super()._drawIcon(icon, painter, rect)


class PrimarySplitDropButton(PrimaryToolButton):

    def _postInit(self):
        self.arrowAni = TranslateYAnimation(self)
        self.setIcon(FIF.ARROW_DOWN)
        self.setIconSize(QSize(10, 10))
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)

    def _drawIcon(self, icon, painter, rect):
        rect.translate(0, self.arrowAni.y)

        if self.isPressed:
            painter.setOpacity(0.7)
        elif self.isHover:
            painter.setOpacity(0.9)
        else:
            painter.setOpacity(1)

        if isinstance(icon, FluentIconBase):
            icon = icon.icon(Theme.DARK if not isDarkTheme() else Theme.LIGHT)

        super()._drawIcon(icon, painter, rect)


class SplitWidgetBase(QWidget):
    """ Split widget base class """

    dropDownClicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.flyout = None  # type: QWidget
        self.dropButton = SplitDropButton(self)

        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.dropButton)

        self.dropButton.clicked.connect(self.dropDownClicked)
        self.dropButton.clicked.connect(self.showFlyout)

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def setWidget(self, widget: QWidget):
        """ set the widget on left side """
        self.hBoxLayout.insertWidget(0, widget, 1, Qt.AlignLeft)

    def setDropButton(self, button):
        """ set drop dow button """
        self.hBoxLayout.removeWidget(self.dropButton)
        self.dropButton.deleteLater()

        self.dropButton = button
        self.dropButton.clicked.connect(self.dropDownClicked)
        self.dropButton.clicked.connect(self.showFlyout)
        self.hBoxLayout.addWidget(button)

    def setDropIcon(self, icon: Union[str, QIcon, FluentIconBase]):
        """ set the icon of drop down button """
        self.dropButton.setIcon(icon)
        self.dropButton.removeEventFilter(self.dropButton.arrowAni)

    def setDropIconSize(self, size: QSize):
        """ set the icon size of drop down button """
        self.dropButton.setIconSize(size)

    def setFlyout(self, flyout):
        """ set the widget pops up when drop down button is clicked

        Parameters
        ----------
        flyout: QWidget
            the widget pops up when drop down button is clicked.
            It should contain `exec(pos: QPoint)` method
        """
        self.flyout = flyout

    def showFlyout(self):
        """ show flyout """
        if not self.flyout:
            return

        w = self.flyout

        if isinstance(w, RoundMenu):
            w.view.setMinimumWidth(self.width())
            w.view.adjustSize()
            w.adjustSize()

        dx = w.layout().contentsMargins().left() if isinstance(w, RoundMenu) else 0
        x = -w.width()//2 + dx + self.width()//2
        y = self.height()
        w.exec(self.mapToGlobal(QPoint(x, y)))


class SplitPushButton(SplitWidgetBase):
    """ Split push button

    Constructors
    ------------
    * SplitPushButton(`parent`: QWidget = None)
    * SplitPushButton(`text`: str, `parent`: QWidget = None, `icon`: QIcon | str | FluentIconBase = None)
    """

    clicked = Signal()

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)
        self.button = PushButton(self)
        self.button.setObjectName('splitPushButton')
        self.button.clicked.connect(self.clicked)
        self.setWidget(self.button)
        self._postInit()

    @__init__.register
    def _(self, text: str, parent: QWidget = None, icon: Union[QIcon, str, FluentIconBase] = None):
        self.__init__(parent)
        self.setText(text)
        self.setIcon(icon)

    @__init__.register
    def _(self, icon: QIcon, text: str, parent: QWidget = None):
        self.__init__(text, parent, icon)

    @__init__.register
    def _(self, icon: FluentIconBase, text: str, parent: QWidget = None):
        self.__init__(text, parent, icon)

    def _postInit(self):
        pass

    def text(self):
        return self.button.text()

    def setText(self, text: str):
        self.button.setText(text)
        self.adjustSize()

    def icon(self):
        return self.button.icon()

    def setIcon(self, icon: Union[QIcon, FluentIconBase, str]):
        self.button.setIcon(icon)

    def setIconSize(self, size: QSize):
        self.button.setIconSize(size)

    text_ = Property(str, text, setText)
    icon_ = Property(QIcon, icon, setIcon)


class PrimarySplitPushButton(SplitPushButton):
    """ Primary split push button

    Constructors
    ------------
    * PrimarySplitPushButton(`parent`: QWidget = None)
    * PrimarySplitPushButton(`text`: str, `parent`: QWidget = None,
                             `icon`: QIcon | str | FluentIconBase = None)
    * PrimarySplitPushButton(`icon`: QIcon | FluentIcon, `text`: str, `parent`: QWidget = None)
    """

    def _postInit(self):
        self.setDropButton(PrimarySplitDropButton(self))

        self.hBoxLayout.removeWidget(self.button)
        self.button.deleteLater()

        self.button = PrimaryPushButton(self)
        self.button.setObjectName('primarySplitPushButton')
        self.button.clicked.connect(self.clicked)
        self.setWidget(self.button)


class SplitToolButton(SplitWidgetBase):
    """ Split tool button

    Constructors
    ------------
    * SplitToolButton(`parent`: QWidget = None)
    * SplitToolButton(`icon`: QIcon | str | FluentIconBase, `parent`: QWidget = None)
    """

    clicked = Signal()

    @singledispatchmethod
    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)
        self.button = ToolButton(self)
        self.button.setObjectName('splitToolButton')
        self.button.clicked.connect(self.clicked)
        self.setWidget(self.button)
        self._postInit()

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

    def _postInit(self):
        pass

    def icon(self):
        return self.button.icon()

    def setIcon(self, icon: Union[QIcon, FluentIconBase, str]):
        self.button.setIcon(icon)

    def setIconSize(self, size: QSize):
        self.button.setIconSize(size)

    icon_ = Property(QIcon, icon, setIcon)


class PrimarySplitToolButton(SplitToolButton):
    """ Primary split push button

    Constructors
    ------------
    * PrimarySplitToolButton(`parent`: QWidget = None)
    * PrimarySplitToolButton(`icon`: QIcon | str | FluentIconBase, `parent`: QWidget = None)
    """

    def _postInit(self):
        self.setDropButton(PrimarySplitDropButton(self))

        self.hBoxLayout.removeWidget(self.button)
        self.button.deleteLater()

        self.button = PrimaryToolButton(self)
        self.button.setObjectName('primarySplitToolButton')
        self.button.clicked.connect(self.clicked)
        self.setWidget(self.button)


class PillButtonBase:
    """ Pill button base class """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        isDark = isDarkTheme()

        if not self.isChecked():
            rect = self.rect().adjusted(1, 1, -1, -1)
            borderColor = QColor(255, 255, 255, 18) if isDark else QColor(0, 0, 0, 15)

            if not self.isEnabled():
                bgColor = QColor(255, 255, 255, 11) if isDark else QColor(249, 249, 249, 75)
            elif self.isPressed or self.isHover:
                bgColor = QColor(255, 255, 255, 21) if isDark else QColor(249, 249, 249, 128)
            else:
                bgColor = QColor(255, 255, 255, 15) if isDark else QColor(243, 243, 243, 194)

        else:
            if not self.isEnabled():
                bgColor = QColor(255, 255, 255, 40) if isDark else QColor(0, 0, 0, 55)
            elif self.isPressed:
                bgColor = ThemeColor.DARK_2.color() if isDark else ThemeColor.LIGHT_3.color()
            elif self.isHover:
                bgColor = ThemeColor.DARK_1.color() if isDark else ThemeColor.LIGHT_1.color()
            else:
                bgColor = themeColor()

            borderColor = Qt.transparent
            rect = self.rect()

        painter.setPen(borderColor)
        painter.setBrush(bgColor)

        r = rect.height() / 2
        painter.drawRoundedRect(rect, r, r)


class PillPushButton(TogglePushButton, PillButtonBase):
    """ Pill push button

    Constructors
    ------------
    * PillPushButton(`parent`: QWidget = None)
    * PillPushButton(`text`: str, `parent`: QWidget = None,
                     `icon`: QIcon | str | FluentIconBase = None)
    * PillPushButton(`icon`: QIcon | FluentIcon, `text`: str, `parent`: QWidget = None)
    """

    def paintEvent(self, e):
        PillButtonBase.paintEvent(self, e)
        TogglePushButton.paintEvent(self, e)


class PillToolButton(ToggleToolButton, PillButtonBase):
    """ Pill push button

    Constructors
    ------------
    * PillToolButton(`parent`: QWidget = None)
    * PillToolButton(`icon`: QIcon | str | FluentIconBase, `parent`: QWidget = None)
    """

    def paintEvent(self, e):
        PillButtonBase.paintEvent(self, e)
        ToggleToolButton.paintEvent(self, e)