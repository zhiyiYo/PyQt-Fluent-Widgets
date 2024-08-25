# coding:utf-8
from enum import Enum
from typing import Union

from PySide2.QtCore import Qt, QSize, QRectF, QObject, QEvent, QPoint
from PySide2.QtGui import QPixmap, QPainter, QColor, QIcon
from PySide2.QtWidgets import QLabel, QWidget, QSizePolicy

from ...common.font import setFont
from ...common.icon import drawIcon, FluentIconBase, toQIcon
from ...common.overload import singledispatchmethod
from ...common.style_sheet import themeColor, FluentStyleSheet, isDarkTheme, Theme


class InfoLevel(Enum):
    """ Info level """
    INFOAMTION = 'Info'
    SUCCESS = 'Success'
    ATTENTION = 'Attension'
    WARNING = "Warning"
    ERROR = "Error"


class InfoBadgePosition(Enum):
    """ Info badge position """
    TOP_RIGHT = 0
    BOTTOM_RIGHT = 1
    RIGHT = 2
    TOP_LEFT = 3
    BOTTOM_LEFT = 4
    LEFT = 5
    NAVIGATION_ITEM = 6


class InfoBadge(QLabel):
    """ Information badge

    Constructors
    ------------
    * InfoBadge(`parent`: QWidget = None, `level`=InfoLevel.ATTENTION)
    * InfoBadge(`text`: str, `parent`: QWidget = None, `level`=InfoLevel.ATTENTION)
    * InfoBadge(`num`: int, `parent`: QWidget = None, `level`=InfoLevel.ATTENTION)
    * InfoBadge(`num`: float, `parent`: QWidget = None, `level`=InfoLevel.ATTENTION)
    """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None, level=InfoLevel.ATTENTION):
        super().__init__(parent=parent)
        self.level = InfoLevel.INFOAMTION
        self.lightBackgroundColor = None
        self.darkBackgroundColor = None
        self.manager = None  # type: InfoBadgeManager
        self.setLevel(level)

        setFont(self, 11)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        FluentStyleSheet.INFO_BADGE.apply(self)

    @__init__.register
    def _(self, text: str, parent: QWidget = None, level=InfoLevel.ATTENTION):
        self.__init__(parent, level)
        self.setText(text)

    @__init__.register
    def _(self, num: int, parent: QWidget = None, level=InfoLevel.ATTENTION):
        self.__init__(parent, level)
        self.setNum(num)

    @__init__.register
    def _(self, num: float, parent: QWidget = None, level=InfoLevel.ATTENTION):
        self.__init__(parent, level)
        self.setNum(num)

    def setLevel(self, level: InfoLevel):
        """ set infomation level """
        if level == self.level:
            return

        self.level = level
        self.setProperty('level', level.value)
        self.update()

    def setProperty(self, name: str, value):
        super().setProperty(name, value)
        if name != "level":
            return

        values = [i.value for i in InfoLevel._member_map_.values()]
        if value in values:
            self.level = InfoLevel(value)

    def setCustomBackgroundColor(self, light, dark):
        """ set the custom background color

        Parameters
        ----------
        light, dark: str | Qt.GlobalColor | QColor
            background color in light/dark theme mode
        """
        self.lightBackgroundColor = QColor(light)
        self.darkBackgroundColor = QColor(dark)
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._backgroundColor())

        r = self.height() / 2
        painter.drawRoundedRect(self.rect(), r, r)

        super().paintEvent(e)

    def _backgroundColor(self):
        isDark = isDarkTheme()

        if self.lightBackgroundColor:
            color = self.darkBackgroundColor if isDark else self.lightBackgroundColor
        elif self.level == InfoLevel.INFOAMTION:
            color = QColor(157, 157, 157) if isDark else QColor(138, 138, 138)
        elif self.level == InfoLevel.SUCCESS:
            color = QColor(108, 203, 95) if isDark else QColor(15, 123, 15)
        elif self.level == InfoLevel.ATTENTION:
            color = themeColor()
        elif self.level == InfoLevel.WARNING:
            color = QColor(255, 244, 206) if isDark else QColor(157, 93, 0)
        else:
            color = QColor(255, 153, 164) if isDark else QColor(196, 43, 28)

        return color

    @classmethod
    def make(cls, text: Union[str, float], parent=None, level=InfoLevel.INFOAMTION, target: QWidget = None,
             position=InfoBadgePosition.TOP_RIGHT):
        w = InfoBadge(text, parent, level)
        w.adjustSize()

        if target:
            w.manager = InfoBadgeManager.make(position, target, w)
            w.move(w.manager.position())

        return w

    @classmethod
    def info(cls, text: Union[str, float], parent=None, target: QWidget = None, position=InfoBadgePosition.TOP_RIGHT):
        return cls.make(text, parent, InfoLevel.INFOAMTION, target, position)

    @classmethod
    def success(cls, text: Union[str, float], parent=None, target: QWidget = None, position=InfoBadgePosition.TOP_RIGHT):
        return cls.make(text, parent, InfoLevel.SUCCESS, target, position)

    @classmethod
    def attension(cls, text: Union[str, float], parent=None, target: QWidget = None, position=InfoBadgePosition.TOP_RIGHT):
        return cls.make(text, parent, InfoLevel.ATTENTION, target, position)

    @classmethod
    def warning(cls, text: Union[str, float], parent=None, target: QWidget = None, position=InfoBadgePosition.TOP_RIGHT):
        return cls.make(text, parent, InfoLevel.WARNING, target, position)

    @classmethod
    def error(cls, text: Union[str, float], parent=None, target: QWidget = None, position=InfoBadgePosition.TOP_RIGHT):
        return cls.make(text, parent, InfoLevel.ERROR, target, position)

    @classmethod
    def custom(cls, text: Union[str, float], light: QColor, dark: QColor, parent=None, target: QWidget = None,
               position=InfoBadgePosition.TOP_RIGHT):
        """ create a badge with custom background color

        Parameters
        ----------
        text: str | float
            the text of badge

        light, dark: str | Qt.GlobalColor | QColor
            background color in light/dark theme mode

        parent: QWidget
            parent widget

        target: QWidget
            target widget to show the badge

        pos: InfoBadgePosition
            the position relative to target
        """
        w = cls.make(text, parent, target=target, position=position)
        w.setCustomBackgroundColor(light, dark)
        return w


class DotInfoBadge(InfoBadge):
    """ Dot info badge """

    def __init__(self, parent=None, level=InfoLevel.ATTENTION):
        super().__init__(parent, level)
        self.setFixedSize(4, 4)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._backgroundColor())
        painter.drawEllipse(self.rect())

    @classmethod
    def make(cls, parent=None, level=InfoLevel.INFOAMTION, target: QWidget = None,
             position=InfoBadgePosition.TOP_RIGHT):
        w = DotInfoBadge(parent, level)

        if target:
            w.manager = InfoBadgeManager.make(position, target, w)
            w.move(w.manager.position())

        return w

    @classmethod
    def info(cls, parent=None, target: QWidget = None, position=InfoBadgePosition.TOP_RIGHT):
        return cls.make(parent, InfoLevel.INFOAMTION, target, position)

    @classmethod
    def success(cls, parent=None, target: QWidget = None, position=InfoBadgePosition.TOP_RIGHT):
        return cls.make(parent, InfoLevel.SUCCESS, target, position)

    @classmethod
    def attension(cls, parent=None, target: QWidget = None, position=InfoBadgePosition.TOP_RIGHT):
        return cls.make(parent, InfoLevel.ATTENTION, target, position)

    @classmethod
    def warning(cls, parent=None, target: QWidget = None, position=InfoBadgePosition.TOP_RIGHT):
        return cls.make(parent, InfoLevel.WARNING, target, position)

    @classmethod
    def error(cls, parent=None, target: QWidget = None, position=InfoBadgePosition.TOP_RIGHT):
        return cls.make(parent, InfoLevel.ERROR, target, position)

    @classmethod
    def custom(cls, light: QColor, dark: QColor, parent=None, target: QWidget = None,
               position=InfoBadgePosition.TOP_RIGHT):
        """ create a badge with custom background color

        Parameters
        ----------
        light, dark: str | Qt.GlobalColor | QColor
            background color in light/dark theme mode

        parent: QWidget
            parent widget
        """
        w = cls.make(parent, target=target, position=position)
        w.setCustomBackgroundColor(light, dark)
        return w


class IconInfoBadge(InfoBadge):
    """ Icon icon badge

    Constructors
    ------------
    * IconInfoBadge(`parent`: QWidget = None, `level`=InfoLevel.ATTENTION)
    * IconInfoBadge(`icon`: QIcon | str | FluentIconBase, `parent`: QWidget = None, `level`=InfoLevel.ATTENTION)
    """

    @singledispatchmethod
    def __init__(self, parent: QWidget = None, level=InfoLevel.ATTENTION):
        super().__init__(parent=parent, level=level)
        self._icon = QIcon()
        self._iconSize = QSize(8, 8)
        self.setFixedSize(16, 16)

    @__init__.register
    def _(self, icon: FluentIconBase, parent: QWidget = None, level=InfoLevel.ATTENTION):
        self.__init__(parent, level)
        self.setIcon(icon)

    @__init__.register
    def _(self, icon: QIcon, parent: QWidget = None, level=InfoLevel.ATTENTION):
        self.__init__(parent, level)
        self.setIcon(icon)

    def setIcon(self, icon: Union[QIcon, FluentIconBase, str]):
        """ set the icon of info badge """
        self._icon = icon
        self.update()

    def icon(self):
        return toQIcon(self._icon)

    def iconSize(self):
        return self._iconSize

    def setIconSize(self, size: QSize):
        self._iconSize = size
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._backgroundColor())
        painter.drawEllipse(self.rect())

        iw, ih = self.iconSize().width(), self.iconSize().height()
        x, y = (self.width() - iw) / 2, (self.width() - ih) / 2
        rect = QRectF(x, y, iw, ih)

        if isinstance(self._icon, FluentIconBase):
            theme = Theme.DARK if not isDarkTheme() else Theme.LIGHT
            self._icon.render(painter, rect, theme)
        else:
            drawIcon(self._icon, painter, rect)

    @classmethod
    def make(cls, icon: Union[QIcon, FluentIconBase], parent=None, level=InfoLevel.INFOAMTION, target: QWidget = None,
             position=InfoBadgePosition.TOP_RIGHT):
        w = IconInfoBadge(icon, parent, level)

        if target:
            w.manager = InfoBadgeManager.make(position, target, w)
            w.move(w.manager.position())

        return w

    @classmethod
    def info(cls, icon: Union[QIcon, FluentIconBase], parent=None, target: QWidget = None,
             position=InfoBadgePosition.TOP_RIGHT):
        return cls.make(icon, parent, InfoLevel.INFOAMTION, target, position)

    @classmethod
    def success(cls, icon: Union[QIcon, FluentIconBase], parent=None, target: QWidget = None,
                position=InfoBadgePosition.TOP_RIGHT):
        return cls.make(icon, parent, InfoLevel.SUCCESS, target, position)

    @classmethod
    def attension(cls, icon: Union[QIcon, FluentIconBase], parent=None, target: QWidget = None,
                  position=InfoBadgePosition.TOP_RIGHT):
        return cls.make(icon, parent, InfoLevel.ATTENTION, target, position)

    @classmethod
    def warning(cls, icon: Union[QIcon, FluentIconBase], parent=None, target: QWidget = None,
                position=InfoBadgePosition.TOP_RIGHT):
        return cls.make(icon, parent, InfoLevel.WARNING, target, position)

    @classmethod
    def error(cls, icon: Union[QIcon, FluentIconBase], parent=None, target: QWidget = None,
              position=InfoBadgePosition.TOP_RIGHT):
        return cls.make(icon, parent, InfoLevel.ERROR, target, position)

    @classmethod
    def custom(cls, icon: Union[QIcon, FluentIconBase], light: QColor, dark: QColor, parent=None,
               target: QWidget = None, position=InfoBadgePosition.TOP_RIGHT):
        """ create a badge with custom background color

        Parameters
        ----------
        icon: QIcon | FluentIconBase
            the icon of badge

        light, dark: str | Qt.GlobalColor | QColor
            background color in light/dark theme mode

        parent: QWidget
            parent widget
        """
        w = cls.make(icon, parent, target=target, position=position)
        w.setCustomBackgroundColor(light, dark)
        return w


class InfoBadgeManager(QObject):
    """ Info badge manager """

    managers = {}

    def __init__(self, target: QWidget, badge: InfoBadge):
        super().__init__()
        self.target = target
        self.badge = badge

        self.target.installEventFilter(self)

    def eventFilter(self, obj, e: QEvent):
        if obj is self.target:
            if e.type() in [QEvent.Resize, QEvent.Move]:
                self.badge.move(self.position())

        return super().eventFilter(obj, e)

    @classmethod
    def register(cls, name):
        """ register menu animation manager

        Parameters
        ----------
        name: Any
            the name of manager, it should be unique
        """
        def wrapper(Manager):
            if name not in cls.managers:
                cls.managers[name] = Manager

            return Manager

        return wrapper

    @classmethod
    def make(cls, position: InfoBadgePosition, target: QWidget, badge: InfoBadge):
        """ mask info badge manager """
        if position not in cls.managers:
            raise ValueError(f'`{position}` is an invalid animation type.')

        return cls.managers[position](target, badge)

    def position(self):
        """ return the position of info badge """
        return QPoint()


@InfoBadgeManager.register(InfoBadgePosition.TOP_RIGHT)
class TopRightInfoBadgeManager(InfoBadgeManager):
    """ Top right info badge manager """

    def position(self):
        pos = self.target.geometry().topRight()
        x = pos.x() - self.badge.width() // 2
        y = pos.y() - self.badge.height() // 2
        return QPoint(x, y)


@InfoBadgeManager.register(InfoBadgePosition.RIGHT)
class RightInfoBadgeManager(InfoBadgeManager):
    """ Right info badge manager """

    def position(self):
        x = self.target.geometry().right() - self.badge.width() // 2
        y = self.target.geometry().center().y() - self.badge.height() // 2
        return QPoint(x, y)


@InfoBadgeManager.register(InfoBadgePosition.BOTTOM_RIGHT)
class BottomRightInfoBadgeManager(InfoBadgeManager):
    """ Bottom right info badge manager """

    def position(self):
        pos = self.target.geometry().bottomRight()
        x = pos.x() - self.badge.width() // 2
        y = pos.y() - self.badge.height() // 2
        return QPoint(x, y)


@InfoBadgeManager.register(InfoBadgePosition.TOP_LEFT)
class TopLeftInfoBadgeManager(InfoBadgeManager):
    """ Top left info badge manager """

    def position(self):
        x = self.target.x() - self.badge.width() // 2
        y = self.target.y() - self.badge.height() // 2
        return QPoint(x, y)


@InfoBadgeManager.register(InfoBadgePosition.LEFT)
class LeftInfoBadgeManager(InfoBadgeManager):
    """ Top left info badge manager """

    def position(self):
        x = self.target.x() - self.badge.width() // 2
        y = self.target.geometry().center().y() - self.badge.height() // 2
        return QPoint(x, y)


@InfoBadgeManager.register(InfoBadgePosition.BOTTOM_LEFT)
class BottomLeftInfoBadgeManager(InfoBadgeManager):
    """ Bottom left info badge manager """

    def position(self):
        pos = self.target.geometry().bottomLeft()
        x = pos.x() - self.badge.width() // 2
        y = pos.y() - self.badge.height() // 2
        return QPoint(x, y)


