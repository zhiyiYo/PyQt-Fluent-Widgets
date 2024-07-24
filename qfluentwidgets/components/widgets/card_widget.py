# coding:utf-8
from typing import List, Union
from PySide2.QtCore import Qt, Signal, QRectF, Property, QPropertyAnimation, QPoint, QSize
from PySide2.QtGui import QPixmap, QPainter, QColor, QPainterPath, QFont, QIcon
from PySide2.QtWidgets import QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel

from ...common.overload import singledispatchmethod
from ...common.style_sheet import isDarkTheme, FluentStyleSheet
from ...common.animation import BackgroundAnimationWidget, DropShadowAnimation
from ...common.font import setFont
from ...common.icon import FluentIconBase
from .label import BodyLabel, CaptionLabel
from .icon_widget import IconWidget


class CardWidget(BackgroundAnimationWidget, QFrame):
    """ Card widget """

    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._isClickEnabled = False
        self._borderRadius = 5

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.clicked.emit()

    def setClickEnabled(self, isEnabled: bool):
        self._isClickEnabled = isEnabled
        self.update()

    def isClickEnabled(self):
        return self._isClickEnabled

    def _normalBackgroundColor(self):
        return QColor(255, 255, 255, 13 if isDarkTheme() else 170)

    def _hoverBackgroundColor(self):
        return QColor(255, 255, 255, 21 if isDarkTheme() else 64)

    def _pressedBackgroundColor(self):
        return QColor(255, 255, 255, 8 if isDarkTheme() else 64)

    def getBorderRadius(self):
        return self._borderRadius

    def setBorderRadius(self, radius: int):
        self._borderRadius = radius
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        w, h = self.width(), self.height()
        r = self.borderRadius
        d = 2 * r

        isDark = isDarkTheme()

        # draw top border
        path = QPainterPath()
        # path.moveTo(1, h - r)
        path.arcMoveTo(1, h - d - 1, d, d, 240)
        path.arcTo(1, h - d - 1, d, d, 225, -60)
        path.lineTo(1, r)
        path.arcTo(1, 1, d, d, -180, -90)
        path.lineTo(w - r, 1)
        path.arcTo(w - d - 1, 1, d, d, 90, -90)
        path.lineTo(w - 1, h - r)
        path.arcTo(w - d - 1, h - d - 1, d, d, 0, -60)

        topBorderColor = QColor(0, 0, 0, 20)
        if isDark:
            if self.isPressed:
                topBorderColor = QColor(255, 255, 255, 18)
            elif self.isHover:
                topBorderColor = QColor(255, 255, 255, 13)
        else:
            topBorderColor = QColor(0, 0, 0, 15)

        painter.strokePath(path, topBorderColor)

        # draw bottom border
        path = QPainterPath()
        path.arcMoveTo(1, h - d - 1, d, d, 240)
        path.arcTo(1, h - d - 1, d, d, 240, 30)
        path.lineTo(w - r - 1, h - 1)
        path.arcTo(w - d - 1, h - d - 1, d, d, 270, 30)

        bottomBorderColor = topBorderColor
        if not isDark and self.isHover and not self.isPressed:
            bottomBorderColor = QColor(0, 0, 0, 27)

        painter.strokePath(path, bottomBorderColor)

        # draw background
        painter.setPen(Qt.NoPen)
        rect = self.rect().adjusted(1, 1, -1, -1)
        painter.setBrush(self.backgroundColor)
        painter.drawRoundedRect(rect, r, r)

    borderRadius = Property(int, getBorderRadius, setBorderRadius)



class SimpleCardWidget(CardWidget):
    """ Simple card widget """

    def __init__(self, parent=None):
        super().__init__(parent)

    def _normalBackgroundColor(self):
        return QColor(255, 255, 255, 13 if isDarkTheme() else 170)

    def _hoverBackgroundColor(self):
        return self._normalBackgroundColor()

    def _pressedBackgroundColor(self):
        return self._normalBackgroundColor()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setBrush(self.backgroundColor)

        if isDarkTheme():
            painter.setPen(QColor(0, 0, 0, 48))
        else:
            painter.setPen(QColor(0, 0, 0, 12))

        r = self.borderRadius
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), r, r)



class ElevatedCardWidget(SimpleCardWidget):
    """ Card widget with shadow effect """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.shadowAni = DropShadowAnimation(self, hoverColor=QColor(0, 0, 0, 20))
        self.shadowAni.setOffset(0, 5)
        self.shadowAni.setBlurRadius(38)

        self.elevatedAni = QPropertyAnimation(self, b'pos', self)
        self.elevatedAni.setDuration(100)

        self._originalPos = self.pos()
        self.setBorderRadius(8)

    def enterEvent(self, e):
        super().enterEvent(e)

        if self.elevatedAni.state() != QPropertyAnimation.Running:
            self._originalPos = self.pos()

        self._startElevateAni(self.pos(), self.pos() - QPoint(0, 3))

    def leaveEvent(self, e):
        super().leaveEvent(e)
        self._startElevateAni(self.pos(), self._originalPos)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self._startElevateAni(self.pos(), self._originalPos)

    def _startElevateAni(self, start, end):
        self.elevatedAni.setStartValue(start)
        self.elevatedAni.setEndValue(end)
        self.elevatedAni.start()

    def _hoverBackgroundColor(self):
        return QColor(255, 255, 255, 16) if isDarkTheme() else QColor(255, 255, 255)

    def _pressedBackgroundColor(self):
        return QColor(255, 255, 255, 6 if isDarkTheme() else 118)



class CardSeparator(QWidget):
    """ Card separator """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(3)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        if isDarkTheme():
            painter.setPen(QColor(255, 255, 255, 46))
        else:
            painter.setPen(QColor(0, 0, 0, 12))

        painter.drawLine(2, 1, self.width() - 2, 1)


class HeaderCardWidget(SimpleCardWidget):
    """ Header card widget """

    @singledispatchmethod
    def __init__(self, parent=None):
        super().__init__(parent)
        self.headerView = QWidget(self)
        self.headerLabel = QLabel(self)
        self.separator = CardSeparator(self)
        self.view = QWidget(self)

        self.vBoxLayout = QVBoxLayout(self)
        self.headerLayout = QHBoxLayout(self.headerView)
        self.viewLayout = QHBoxLayout(self.view)

        self.headerLayout.addWidget(self.headerLabel)
        self.headerLayout.setContentsMargins(24, 0, 16, 0)
        self.headerView.setFixedHeight(48)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.headerView)
        self.vBoxLayout.addWidget(self.separator)
        self.vBoxLayout.addWidget(self.view)

        self.viewLayout.setContentsMargins(24, 24, 24, 24)
        setFont(self.headerLabel, 15, QFont.DemiBold)

        self.view.setObjectName('view')
        self.headerView.setObjectName('headerView')
        self.headerLabel.setObjectName('headerLabel')
        FluentStyleSheet.CARD_WIDGET.apply(self)

        self._postInit()

    @__init__.register
    def _(self, title: str, parent=None):
        self.__init__(parent)
        self.setTitle(title)

    def getTitle(self):
        return self.headerLabel.text()

    def setTitle(self, title: str):
        self.headerLabel.setText(title)

    def _postInit(self):
        pass

    title = Property(str, getTitle, setTitle)



class CardGroupWidget(QWidget):

    def __init__(self, icon: Union[str, FluentIconBase, QIcon], title: str, content: str, parent=None):
        super().__init__(parent=parent)
        self.vBoxLayout = QVBoxLayout(self)
        self.hBoxLayout = QHBoxLayout()

        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title)
        self.contentLabel = CaptionLabel(content)
        self.textLayout = QVBoxLayout()

        self.separator = CardSeparator()

        self.__initWidget()

    def __initWidget(self):
        self.separator.hide()
        self.iconWidget.setFixedSize(20, 20)
        self.contentLabel.setTextColor(QColor(96, 96, 96), QColor(206, 206, 206))

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.addWidget(self.separator)

        self.textLayout.addWidget(self.titleLabel)
        self.textLayout.addWidget(self.contentLabel)
        self.hBoxLayout.addWidget(self.iconWidget)
        self.hBoxLayout.addLayout(self.textLayout)
        self.hBoxLayout.addStretch(1)

        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.setContentsMargins(24, 10, 24, 10)
        self.textLayout.setContentsMargins(0, 0, 0, 0)
        self.textLayout.setSpacing(0)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.textLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def title(self):
        return self.titleLabel.text()

    def setTitle(self, text: str):
        self.titleLabel.setText(text)

    def content(self):
        return self.contentLabel.text()

    def setContent(self, text: str):
        self.contentLabel.setText(text)

    def icon(self):
        return self.iconWidget.icon

    def setIcon(self, icon: Union[str, FluentIconBase, QIcon]):
        self.iconWidget.setIcon(icon)

    def setIconSize(self, size: QSize):
        self.iconWidget.setFixedSize(size)

    def setSeparatorVisible(self, isVisible: bool):
        self.separator.setVisible(isVisible)

    def isSeparatorVisible(self):
        return self.separator.isVisible()

    def addWidget(self, widget: QWidget, stretch=0):
        self.hBoxLayout.addWidget(widget, stretch=stretch)


class GroupHeaderCardWidget(HeaderCardWidget):
    """ Group header card widget """

    def _postInit(self):
        super()._postInit()
        self.groupWidgets = []  # type: List[CardGroupWidget]
        self.groupLayout = QVBoxLayout()

        self.groupLayout.setSpacing(0)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.groupLayout.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.addLayout(self.groupLayout)

    def addGroup(self, icon: Union[str, FluentIconBase, QIcon], title: str, content: str, widget: QWidget, stretch=0) -> CardGroupWidget:
        """ add widget to a new group

        Parameters
        ----------
        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        widget: QWidget
            the widget to be added

        stretch: int
            the layout stretch of widget
        """
        group = CardGroupWidget(icon, title, content, self)
        group.addWidget(widget, stretch=stretch)

        if self.groupWidgets:
            self.groupWidgets[-1].setSeparatorVisible(True)

        self.groupLayout.addWidget(group)
        self.groupWidgets.append(group)
        return group

    def groupCount(self):
        return len(self.groupWidgets)