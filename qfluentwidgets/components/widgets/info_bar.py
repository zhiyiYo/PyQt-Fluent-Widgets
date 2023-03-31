# coding:utf-8
from enum import Enum
from typing import Union
import weakref

from PyQt6.QtCore import (Qt, QEvent, QSize, QRectF, QObject, QPropertyAnimation,
                          QEasingCurve, QTimer, pyqtSignal, QParallelAnimationGroup, QPoint)
from PyQt6.QtGui import QPainter, QIcon, QColor
from PyQt6.QtWidgets import (QWidget, QFrame, QLabel, QHBoxLayout, QVBoxLayout,
                             QToolButton, QGraphicsOpacityEffect)

from ...common.auto_wrap import TextWrap
from ...common.style_sheet import setStyleSheet, themeColor
from ...common.icon import FluentIconBase, Theme, isDarkTheme, writeSvg, drawSvgIcon, drawIcon
from ...common.icon import FluentIcon as FIF


class InfoBarCloseButton(QToolButton):
    """ Close button """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(36, 36)
        self.setIconSize(QSize(12, 12))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setObjectName('infoBarCloseButton')
        setStyleSheet(self, 'info_bar')

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing |
                               QPainter.RenderHint.SmoothPixmapTransform)
        FIF.CLOSE.render(painter, QRectF(11, 12, 12, 12))


class InfoBarIcon(FluentIconBase, Enum):
    """ Info bar icon """

    INFORMATION = "Info"
    SUCCESS = "Success"
    WARNING = "Warning"
    ERROR = "Error"

    def path(self, theme=Theme.AUTO):
        if theme == Theme.AUTO:
            color = "dark" if isDarkTheme() else "light"
        else:
            color = theme.value.lower()

        return f':/qfluentwidgets/images/info_bar/{self.value}_{color}.svg'


class InfoBarPosition(Enum):
    """ Info bar position """
    TOP = 0
    BOTTOM = 1
    TOP_LEFT = 2
    TOP_RIGHT = 3
    BOTTOM_LEFT = 4
    BOTTOM_RIGHT = 5
    NONE = 6


class InfoIconWidget(QWidget):
    """ Icon widget """

    def __init__(self, icon: InfoBarIcon, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(15, 15)
        self.icon = icon

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing |
                               QPainter.RenderHint.SmoothPixmapTransform)

        if self.icon != InfoBarIcon.INFORMATION:
            drawIcon(self.icon, painter, self.rect())
        else:
            svg = writeSvg(self.icon.path(), [0], fill=themeColor().name())
            drawSvgIcon(svg.encode(), painter, self.rect())


class InfoBar(QFrame):
    """ Information bar """

    closedSignal = pyqtSignal()

    def __init__(self, icon: Union[InfoBarIcon, FluentIconBase, QIcon, str], title: str, content: str,
                 orient=Qt.Orientation.Horizontal, isClosable=True, duration=1000, position=InfoBarPosition.TOP_RIGHT,
                 parent=None):
        """
        Parameters
        ----------
        icon: InfoBarIcon | FluentIconBase | QIcon | str
            the icon of info bar

        title: str
            the title of info bar

        content: str
            the content of info bar

        orient: Qt.Orientation
            the layout direction of info bar, use `Qt.Horizontal` for short content

        isClosable: bool
            whether to show the close button

        duraction: int
            the time for info bar to display in milliseconds. If duration is less than zero,
            info bar will never disappear.

        parent: QWidget
            parent widget
        """
        super().__init__(parent=parent)
        self.title = title
        self.content = content
        self.orient = orient
        self.icon = icon
        self.duration = duration
        self.isClosable = isClosable
        self.position = position

        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(self)
        self.closeButton = InfoBarCloseButton(self)
        self.iconWidget = InfoIconWidget(icon)

        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout()
        self.contentLayout = QHBoxLayout() if self.orient == Qt.Orientation.Horizontal else QVBoxLayout()

        self.opacityEffect = QGraphicsOpacityEffect(self)
        self.opacityAni = QPropertyAnimation(
            self.opacityEffect, b'opacity', self)

        self.lightBackgroundColor = None
        self.darkBackgroundColor = None

        self.__initWidget()

    def __initWidget(self):
        self.titleLabel.setMinimumHeight(36)
        self.opacityEffect.setOpacity(1)
        self.setGraphicsEffect(self.opacityEffect)
        self.closeButton.setVisible(self.isClosable)

        self.__initLayout()
        self.__setQss()

        self.closeButton.clicked.connect(self.close)

    def __initLayout(self):
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)
        self.contentLayout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetMinimumSize)

        self.vBoxLayout.setSpacing(0)
        self.hBoxLayout.setSpacing(0)

        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.hBoxLayout.addWidget(self.iconWidget)
        self.hBoxLayout.addSpacing(15)
        self.hBoxLayout.addWidget(self.titleLabel)

        # add content label to layout
        if self.orient == Qt.Orientation.Horizontal:
            self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
            self.hBoxLayout.addSpacing(12)
            self.contentLayout.setContentsMargins(0, 0, 20*self.isClosable, 0)
            self.contentLayout.setSpacing(12)
            self.hBoxLayout.addLayout(self.contentLayout)
            self.contentLabel.setText(self.content)
        else:
            self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
            self.contentLayout.setContentsMargins(47, 0, 40, 18)
            self.contentLayout.setSpacing(14)
            self.vBoxLayout.addLayout(self.contentLayout)
            self.contentLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
            self._adjustText()

        self.contentLayout.addWidget(self.contentLabel)

        # add close button to layout
        if self.isClosable:
            self.hBoxLayout.addWidget(self.closeButton)
            mb = 6 if self.orient == Qt.Orientation.Horizontal else 0
            self.hBoxLayout.setContentsMargins(16, 6, 7, mb)
        else:
            self.hBoxLayout.setContentsMargins(16, 6, 16, 6)

    def __setQss(self):
        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        if isinstance(self.icon, Enum):
            self.setProperty('type', self.icon.value)

        setStyleSheet(self, 'info_bar')

    def __fadeOut(self):
        """ fade out """
        self.opacityAni.setDuration(200)
        self.opacityAni.setStartValue(1)
        self.opacityAni.setEndValue(0)
        self.opacityAni.finished.connect(self.close)
        self.opacityAni.start()

    def _adjustText(self):
        w = 900 if not self.parent() else (self.parent().width() - 50)
        chars = max(min(w / 9, 120), 30)
        self.contentLabel.setText(TextWrap.wrap(self.content, chars, False)[0])
        self.adjustSize()

    def addWidget(self, widget: QWidget, stretch=0):
        """ add widget to info bar """
        self.contentLayout.addWidget(widget, stretch, Qt.AlignmentFlag.AlignLeft)

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

    def eventFilter(self, obj, e: QEvent):
        if obj is self.parent():
            if e.type() in [QEvent.Type.Resize, QEvent.Type.WindowStateChange]:
                self._adjustText()

        return super().eventFilter(obj, e)

    def closeEvent(self, e):
        self.closedSignal.emit()
        self.deleteLater()

    def showEvent(self, e):
        self._adjustText()
        super().showEvent(e)

        if self.duration >= 0:
            QTimer.singleShot(self.duration, self.__fadeOut)

        if self.position != InfoBarPosition.NONE:
            manager = InfoBarManager.make(self.position)
            manager.add(self)

        if self.parent():
            self.parent().installEventFilter(self)

    def paintEvent(self, e):
        super().paintEvent(e)
        if self.lightBackgroundColor is None:
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        if isDarkTheme():
            painter.setBrush(self.darkBackgroundColor)
        else:
            painter.setBrush(self.lightBackgroundColor)

        rect = self.rect().adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(rect, 6, 6)

    @classmethod
    def new(cls, icon, title, content, orient=Qt.Orientation.Horizontal, isClosable=True, duration=1000,
            position=InfoBarPosition.TOP_RIGHT, parent=None):
        w = InfoBar(icon, title, content, orient,
                    isClosable, duration, position, parent)
        w.show()
        return w

    @classmethod
    def info(cls, title, content, orient=Qt.Orientation.Horizontal, isClosable=True, duration=1000,
             position=InfoBarPosition.TOP_RIGHT, parent=None):
        return cls.new(InfoBarIcon.INFORMATION, title, content, orient, isClosable, duration, position, parent)

    @classmethod
    def success(cls, title, content, orient=Qt.Orientation.Horizontal, isClosable=True, duration=1000,
                position=InfoBarPosition.TOP_RIGHT, parent=None):
        return cls.new(InfoBarIcon.SUCCESS, title, content, orient, isClosable, duration, position, parent)

    @classmethod
    def warning(cls, title, content, orient=Qt.Orientation.Horizontal, isClosable=True, duration=1000,
                position=InfoBarPosition.TOP_RIGHT, parent=None):
        return cls.new(InfoBarIcon.WARNING, title, content, orient, isClosable, duration, position, parent)

    @classmethod
    def error(cls, title, content, orient=Qt.Orientation.Horizontal, isClosable=True, duration=1000,
              position=InfoBarPosition.TOP_RIGHT, parent=None):
        return cls.new(InfoBarIcon.ERROR, title, content, orient, isClosable, duration, position, parent)


class InfoBarManager(QObject):
    """ Info bar manager """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(InfoBarManager, cls).__new__(
                cls, *args, **kwargs)
            cls._instance.__initialized = False

        return cls._instance

    def __init__(self):
        super().__init__()
        if self.__initialized:
            return

        self.spacing = 16
        self.margin = 24
        self.infoBars = weakref.WeakKeyDictionary()
        self.aniGroups = weakref.WeakKeyDictionary()
        self.slideAnis = []
        self.dropAnis = []
        self.__initialized = True

    def add(self, infoBar: InfoBar):
        """ add info bar """
        p = infoBar.parent()    # type:QWidget
        if not p:
            return

        if p not in self.infoBars:
            p.installEventFilter(self)
            self.infoBars[p] = []
            self.aniGroups[p] = QParallelAnimationGroup(self)

        if infoBar in self.infoBars[p]:
            return

        # add drop animation
        if self.infoBars[p]:
            dropAni = QPropertyAnimation(infoBar, b'pos')
            dropAni.setDuration(200)

            self.aniGroups[p].addAnimation(dropAni)
            self.dropAnis.append(dropAni)

            infoBar.setProperty('dropAni', dropAni)

        # add slide animation
        self.infoBars[p].append(infoBar)
        slideAni = self._createSlideAni(infoBar)
        self.slideAnis.append(slideAni)

        infoBar.setProperty('slideAni', slideAni)
        infoBar.closedSignal.connect(lambda: self.remove(infoBar))

        slideAni.start()

    def remove(self, infoBar: InfoBar):
        """ remove info bar """
        p = infoBar.parent()
        if p not in self.infoBars:
            return

        if infoBar not in self.infoBars[p]:
            return

        self.infoBars[p].remove(infoBar)

        # remove drop animation
        dropAni = infoBar.property('dropAni')   # type: QPropertyAnimation
        if dropAni:
            self.aniGroups[p].removeAnimation(dropAni)
            self.dropAnis.remove(dropAni)

        # remove slider animation
        slideAni = infoBar.property('slideAni')
        if slideAni:
            self.slideAnis.remove(slideAni)

        # adjust the position of the remaining info bars
        self._updateDropAni(p)
        self.aniGroups[p].start()

    def _createSlideAni(self, infoBar: InfoBar):
        slideAni = QPropertyAnimation(infoBar, b'pos')
        slideAni.setEasingCurve(QEasingCurve.Type.OutQuad)
        slideAni.setDuration(200)

        slideAni.setStartValue(self._slideStartPos(infoBar))
        slideAni.setEndValue(self._pos(infoBar))

        return slideAni

    def _updateDropAni(self, parent):
        for bar in self.infoBars[parent]:
            ani = bar.property('dropAni')
            if not ani:
                continue

            ani.setStartValue(bar.pos())
            ani.setEndValue(self._pos(bar))

    def _pos(self, infoBar: InfoBar, parentSize=None) -> QPoint:
        raise NotImplementedError

    def _slideStartPos(self, infoBar: InfoBar) -> QPoint:
        raise NotImplementedError

    def eventFilter(self, obj, e: QEvent):
        if obj not in self.infoBars:
            return False

        if e.type() in [QEvent.Type.Resize, QEvent.Type.WindowStateChange]:
            size = e.size() if e.type() == QEvent.Type.Resize else None
            for bar in self.infoBars[obj]:
                bar.move(self._pos(bar, size))

        return super().eventFilter(obj, e)

    @staticmethod
    def make(position: InfoBarPosition):
        """ mask info bar manager according to the display position """
        managers = {
            InfoBarPosition.TOP: TopInfoBarManager,
            InfoBarPosition.BOTTOM: BottomInfoBarManager,
            InfoBarPosition.TOP_RIGHT: TopRightInfoBarManager,
            InfoBarPosition.BOTTOM_RIGHT: BottomRightInfoBarManager,
            InfoBarPosition.TOP_LEFT: TopLeftInfoBarManager,
            InfoBarPosition.BOTTOM_LEFT: BottomLeftInfoBarManager,
        }

        if position not in managers:
            raise ValueError(f'`{position}` is an invalid info bar position.')

        return managers[position]()


class TopInfoBarManager(InfoBarManager):
    """ Top position info bar manager """

    def _pos(self, infoBar: InfoBar, parentSize=None):
        p = infoBar.parent()
        parentSize = parentSize or p.size()

        x = (infoBar.parent().width() - infoBar.width()) // 2
        y = self.margin
        index = self.infoBars[p].index(infoBar)
        for bar in self.infoBars[p][0:index]:
            y += (bar.height() + self.spacing)

        return QPoint(x, y)

    def _slideStartPos(self, infoBar: InfoBar):
        pos = self._pos(infoBar)
        return QPoint(pos.x(), pos.y() - 16)


class TopRightInfoBarManager(InfoBarManager):
    """ Top right position info bar manager """

    def _pos(self, infoBar: InfoBar, parentSize=None):
        p = infoBar.parent()
        parentSize = parentSize or p.size()

        x = parentSize.width() - infoBar.width() - self.margin
        y = self.margin
        index = self.infoBars[p].index(infoBar)
        for bar in self.infoBars[p][0:index]:
            y += (bar.height() + self.spacing)

        return QPoint(x, y)

    def _slideStartPos(self, infoBar: InfoBar):
        return QPoint(infoBar.parent().width(), self._pos(infoBar).y())


class BottomRightInfoBarManager(InfoBarManager):
    """ Bottom right position info bar manager """

    def _pos(self, infoBar: InfoBar, parentSize=None) -> QPoint:
        p = infoBar.parent()
        parentSize = parentSize or p.size()

        x = parentSize.width() - infoBar.width() - self.margin
        y = parentSize.height() - infoBar.height() - self.margin

        index = self.infoBars[p].index(infoBar)
        for bar in self.infoBars[p][0:index]:
            y -= (bar.height() + self.spacing)

        return QPoint(x, y)

    def _slideStartPos(self, infoBar: InfoBar):
        return QPoint(infoBar.parent().width(), self._pos(infoBar).y())


class TopLeftInfoBarManager(InfoBarManager):
    """ Top left position info bar manager """

    def _pos(self, infoBar: InfoBar, parentSize=None) -> QPoint:
        p = infoBar.parent()
        parentSize = parentSize or p.size()

        y = self.margin
        index = self.infoBars[p].index(infoBar)

        for bar in self.infoBars[p][0:index]:
            y += (bar.height() + self.spacing)

        return QPoint(self.margin, y)

    def _slideStartPos(self, infoBar: InfoBar):
        return QPoint(-infoBar.width(), self._pos(infoBar).y())


class BottomLeftInfoBarManager(InfoBarManager):
    """ Bottom left position info bar manager """

    def _pos(self, infoBar: InfoBar, parentSize: QSize = None) -> QPoint:
        p = infoBar.parent()
        parentSize = parentSize or p.size()

        y = parentSize.height() - infoBar.height() - self.margin
        index = self.infoBars[p].index(infoBar)

        for bar in self.infoBars[p][0:index]:
            y -= (bar.height() + self.spacing)

        return QPoint(self.margin, y)

    def _slideStartPos(self, infoBar: InfoBar):
        return QPoint(-infoBar.width(), self._pos(infoBar).y())


class BottomInfoBarManager(InfoBarManager):
    """ Bottom position info bar manager """

    def _pos(self, infoBar: InfoBar, parentSize: QSize = None) -> QPoint:
        p = infoBar.parent()
        parentSize = parentSize or p.size()

        x = (parentSize.width() - infoBar.width()) // 2
        y = parentSize.height() - infoBar.height() - self.margin
        index = self.infoBars[p].index(infoBar)

        for bar in self.infoBars[p][0:index]:
            y -= (bar.height() + self.spacing)

        return QPoint(x, y)

    def _slideStartPos(self, infoBar: InfoBar):
        pos = self._pos(infoBar)
        return QPoint(pos.x(), pos.y() + 16)
