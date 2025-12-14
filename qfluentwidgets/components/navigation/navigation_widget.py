# coding:utf-8
from typing import Union, List

from PyQt6.QtCore import (Qt, pyqtSignal, QRect, QRectF, QPropertyAnimation, pyqtProperty, QMargins,
                          QEasingCurve, QPoint, QEvent, QPointF, QSize, QParallelAnimationGroup)
from PyQt6.QtGui import QColor, QPainter, QPen, QIcon, QCursor, QFont, QBrush, QPixmap, QImage
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from collections import deque

from ...common.config import isDarkTheme
from ...common.style_sheet import themeColor
from ...common.icon import drawIcon, toQIcon
from ...common.icon import FluentIcon as FIF
from ...common.color import autoFallbackThemeColor
from ...common.font import setFont, getFont
from ...common.animation import ScaleSlideAnimation
from ..widgets.scroll_area import ScrollArea
from ..widgets.label import AvatarWidget
from ..widgets.info_badge import InfoBadgeManager, InfoBadgePosition


class NavigationWidget(QWidget):
    """ Navigation widget """

    clicked = pyqtSignal(bool)  # whether triggered by the user
    selectedChanged = pyqtSignal(bool)
    EXPAND_WIDTH = 312

    def __init__(self, isSelectable: bool, parent=None):
        super().__init__(parent)
        self.isCompacted = True
        self.isSelected = False
        self.isPressed = False
        self.isEnter = False
        self.isAboutSelected = False
        self.isSelectable = isSelectable
        self.treeParent = None
        self.nodeDepth = 0

        # text color
        self.lightTextColor = QColor(0, 0, 0)
        self.darkTextColor = QColor(255, 255, 255)

        # indicator color
        self.lightIndicatorColor = QColor()
        self.darkIndicatorColor = QColor()

        self.setFixedSize(40, 36)

    def enterEvent(self, e):
        self.isEnter = True
        self.update()

    def leaveEvent(self, e):
        self.isEnter = False
        self.isPressed = False
        self.update()

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.isPressed = True
        self.update()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.isPressed = False
        self.update()
        self.clicked.emit(True)

    def click(self):
        self.clicked.emit(True)

    def setCompacted(self, isCompacted: bool):
        """ set whether the widget is compacted """
        if isCompacted == self.isCompacted:
            return

        self.isCompacted = isCompacted
        if isCompacted:
            self.setFixedSize(40, 36)
        else:
            self.setFixedSize(self.EXPAND_WIDTH, 36)

        self.update()

    def setSelected(self, isSelected: bool):
        """ set whether the button is selected

        Parameters
        ----------
        isSelected: bool
            whether the button is selected
        """
        if not self.isSelectable:
            return

        self.isSelected = isSelected
        self.isAboutSelected = False
        self.update()
        self.selectedChanged.emit(isSelected)

    def textColor(self):
        return self.darkTextColor if isDarkTheme() else self.lightTextColor

    def setLightTextColor(self, color):
        """ set the text color in light theme mode """
        self.lightTextColor = QColor(color)
        self.update()

    def setDarkTextColor(self, color):
        """ set the text color in dark theme mode """
        self.darkTextColor = QColor(color)
        self.update()

    def setTextColor(self, light, dark):
        """ set the text color in light/dark theme mode """
        self.setLightTextColor(light)
        self.setDarkTextColor(dark)

    def setAboutSelected(self, selected: bool):
        self.isAboutSelected = selected
        self.update()

    def _margins(self):
        return QMargins(0, 0, 0, 0)

    def indicatorRect(self):
        """ get the indicator geometry """
        m = self._margins()
        return QRectF(m.left(), 10, 3, 16)

    def setIndicatorColor(self, light, dark):
        self.lightIndicatorColor = QColor(light)
        self.darkIndicatorColor = QColor(dark)
        self.update()



class NavigationPushButton(NavigationWidget):
    """ Navigation push button """

    def __init__(self, icon: Union[str, QIcon, FIF], text: str, isSelectable: bool, parent=None):
        """
        Parameters
        ----------
        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        text: str
            the text of button
        """
        super().__init__(isSelectable=isSelectable, parent=parent)

        self._icon = icon
        self._text = text

        setFont(self)

    def text(self):
        return self._text

    def setText(self, text: str):
        self._text = text
        self.update()

    def icon(self):
        return toQIcon(self._icon)

    def setIcon(self, icon: Union[str, QIcon, FIF]):
        self._icon = icon
        self.update()

    def _canDrawIndicator(self):
        return self.isSelected

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing |
                               QPainter.RenderHint.TextAntialiasing | QPainter.RenderHint.SmoothPixmapTransform)
        painter.setPen(Qt.PenStyle.NoPen)

        if self.isPressed:
            painter.setOpacity(0.7)
        if not self.isEnabled():
            painter.setOpacity(0.4)

        # draw background
        c = 255 if isDarkTheme() else 0
        m = self._margins()
        pl, pr = m.left(), m.right()
        globalRect = QRect(self.mapToGlobal(QPoint()), self.size())

        if self._canDrawIndicator():
            painter.setBrush(QColor(c, c, c, 6 if self.isEnter else 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

            # draw indicator
            painter.setBrush(autoFallbackThemeColor(self.lightIndicatorColor, self.darkIndicatorColor))
            painter.drawRoundedRect(self.indicatorRect(), 1.5, 1.5)
        elif ((self.isEnter and globalRect.contains(QCursor.pos())) or self.isAboutSelected) and self.isEnabled():
            painter.setBrush(QColor(c, c, c, 6 if self.isAboutSelected else 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

        drawIcon(self._icon, painter, QRectF(11.5+pl, 10, 16, 16))

        # draw text
        if self.isCompacted:
            return

        painter.setFont(self.font())
        painter.setPen(self.textColor())

        left = 44 + pl if not self.icon().isNull() else pl + 16
        painter.drawText(QRectF(left, 0, self.width()-13-left-pr, self.height()), Qt.AlignmentFlag.AlignVCenter, self.text())


class NavigationToolButton(NavigationPushButton):
    """ Navigation tool button """

    def __init__(self, icon: Union[str, QIcon, FIF], parent=None):
        super().__init__(icon, '', False, parent)

    def setCompacted(self, isCompacted: bool):
        self.setFixedSize(40, 36)


class NavigationSeparator(NavigationWidget):
    """ Navigation Separator """

    def __init__(self, parent=None):
        super().__init__(False, parent=parent)
        self.setCompacted(True)

    def setCompacted(self, isCompacted: bool):
        if isCompacted:
            self.setFixedSize(48, 3)
        else:
            self.setFixedSize(self.EXPAND_WIDTH + 10, 3)

        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        c = 255 if isDarkTheme() else 0
        pen = QPen(QColor(c, c, c, 15))
        pen.setCosmetic(True)
        painter.setPen(pen)
        painter.drawLine(0, 1, self.width(), 1)


class NavigationItemHeader(NavigationWidget):
    """ Navigation item header for grouping items """

    def __init__(self, text: str, parent=None):
        super().__init__(False, parent=parent)
        self._text = text
        self._targetHeight = 30
        setFont(self, 12)  # smaller font size for header

        # Override text colors for header style
        self.lightTextColor = QColor(96, 96, 96)  # gray in light mode
        self.darkTextColor = QColor(160, 160, 160)  # light gray in dark mode

        # Animation for smooth height transition
        self.heightAni = QPropertyAnimation(self, b'maximumHeight', self)
        self.heightAni.setDuration(150)
        self.heightAni.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.heightAni.valueChanged.connect(self._onHeightChanged)

        self.setCursor(Qt.CursorShape.ArrowCursor)  # normal cursor, not hand cursor

        # Initialize to hidden state
        self.setFixedHeight(0)

    def text(self):
        return self._text

    def setText(self, text: str):
        self._text = text
        self.update()

    def setCompacted(self, isCompacted: bool):
        """ set whether the widget is compacted """
        self.isCompacted = isCompacted

        # Stop any running animation
        self.heightAni.stop()

        if isCompacted:
            # in compact mode, animate to height 0
            self.setFixedWidth(40)
            self.heightAni.setStartValue(self.height())
            self.heightAni.setEndValue(0)
        else:
            # in expand mode, animate to full height
            self.setFixedWidth(self.EXPAND_WIDTH)
            self.setVisible(True)  # ensure visible before expanding
            self.heightAni.setStartValue(self.height())
            self.heightAni.setEndValue(self._targetHeight)

        self.heightAni.start()
        self.update()

    def _onCollapseFinished(self):
        """ called when collapse animation finishes """
        if not self.isCompacted:
            self.setVisible(False)

    def _onHeightChanged(self, value):
        """ called when height animation value changes """
        self.setFixedHeight(value)

    def mousePressEvent(self, e):
        # do not handle mouse press - header is not clickable
        e.ignore()

    def mouseReleaseEvent(self, e):
        # do not handle mouse release - header is not clickable
        e.ignore()

    def enterEvent(self, e):
        # do not show hover effect
        pass

    def leaveEvent(self, e):
        # do not show hover effect
        pass

    def paintEvent(self, e):
        if self.height() == 0 or not self.isVisible():
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)

        # Calculate opacity based on height for fade effect
        opacity = min(1.0, self.height() / max(1, self._targetHeight))
        painter.setOpacity(opacity)

        if not self.isCompacted:
            # draw header text in expand mode
            painter.setFont(self.font())
            painter.setPen(self.textColor())
            painter.drawText(QRectF(16, 0, self.width() - 16, self.height()),
                             Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, self.text())


class NavigationTreeItem(NavigationPushButton):
    """ Navigation tree item widget """

    itemClicked = pyqtSignal(bool, bool)    # triggerByUser, clickArrow

    def __init__(self, icon: Union[str, QIcon, FIF], text: str, isSelectable: bool, parent=None):
        super().__init__(icon, text, isSelectable, parent)
        self._arrowAngle = 0
        self.rotateAni = QPropertyAnimation(self, b'arrowAngle', self)

    def setExpanded(self, isExpanded: bool):
        self.rotateAni.stop()
        self.rotateAni.setEndValue(180 if isExpanded else 0)
        self.rotateAni.setDuration(150)
        self.rotateAni.start()

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        clickArrow = QRectF(self.width()-30, 8, 20, 20).contains(QPointF(e.pos()))
        self.itemClicked.emit(True, clickArrow and not self.treeWidget().isLeaf())
        self.update()

    def _canDrawIndicator(self):
        p = self.treeWidget()   # type: NavigationTreeWidget
        if p.isLeaf() or p.isSelected:
            return p.isSelected

        for child in p.treeChildren:
            if child.itemWidget._canDrawIndicator() and not child.isVisible():
                return True

        return False

    def _margins(self):
        p = self.treeWidget()   # type: NavigationTreeWidget
        return QMargins(p.nodeDepth*28, 0, 20*bool(p.treeChildren), 0)

    def paintEvent(self, e):
        super().paintEvent(e)
        self._drawDropDownArrow()

    def _drawDropDownArrow(self):
        # only draw arrow on inner item
        if self.isCompacted or self.treeWidget().isLeaf():
            return

        # draw drop down arrow
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        if self.isPressed:
            painter.setOpacity(0.7)
        if not self.isEnabled():
            painter.setOpacity(0.4)

        painter.translate(self.width() - 20, 18)
        painter.rotate(self.arrowAngle)
        FIF.ARROW_DOWN.render(painter, QRectF(-5, -5, 9.6, 9.6))

    def treeWidget(self) -> 'NavigationTreeWidget':
        return self.parent()

    def getArrowAngle(self):
        return self._arrowAngle

    def setArrowAngle(self, angle):
        self._arrowAngle = angle
        self.update()

    arrowAngle = pyqtProperty(float, getArrowAngle, setArrowAngle)


class NavigationTreeWidgetBase(NavigationWidget):
    """ Navigation tree widget base class """

    def addChild(self, child):
        """ add child

        Parameters
        ----------
        child: NavigationTreeWidgetBase
            child item
        """
        raise NotImplementedError

    def insertChild(self, index: int, child: NavigationWidget):
        """ insert child

        Parameters
        ----------
        child: NavigationTreeWidgetBase
            child item
        """
        raise NotImplementedError

    def removeChild(self, child: NavigationWidget):
        """ remove child

        Parameters
        ----------
        child: NavigationTreeWidgetBase
            child item
        """
        raise NotImplementedError

    def isRoot(self):
        """ is root node """
        return True

    def isLeaf(self):
        """ is leaf node """
        return True

    def setExpanded(self, isExpanded: bool):
        """ set the expanded status

        Parameters
        ----------
        isExpanded: bool
            whether to expand node
        """
        raise NotImplementedError

    def childItems(self) -> list:
        """ return child items """
        raise NotImplementedError

    def setRememberExpandState(self, remember: bool):
        """ set whether to remember expand state """
        raise NotImplementedError

    def saveExpandState(self):
        """ save current expand state """
        raise NotImplementedError

    def restoreExpandState(self, ani=True):
        """ restore saved expand state """
        raise NotImplementedError


class NavigationTreeWidget(NavigationTreeWidgetBase):
    """ Navigation tree widget """

    expanded = pyqtSignal()

    def __init__(self, icon: Union[str, QIcon, FIF], text: str, isSelectable: bool, parent=None):
        super().__init__(isSelectable, parent)

        self.treeChildren = []  # type: List[NavigationTreeWidget]
        self.isExpanded = False
        self._icon = icon
        self._rememberExpandState = False
        self._wasExpanded = False

        self.itemWidget = NavigationTreeItem(icon, text, isSelectable, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.expandAni = QPropertyAnimation(self, b'geometry', self)

        self.__initWidget()

    def __initWidget(self):
        self.vBoxLayout.setSpacing(4)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.itemWidget, 0, Qt.AlignmentFlag.AlignTop)

        self.itemWidget.itemClicked.connect(self._onClicked)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.expandAni.valueChanged.connect(lambda g: self.setFixedSize(g.size()))
        self.expandAni.valueChanged.connect(self.expanded)
        self.expandAni.finished.connect(self.parentWidget().layout().invalidate)

    def _margins(self):
        return self.itemWidget._margins()

    def addChild(self, child):
        self.insertChild(-1, child)

    def text(self):
        return self.itemWidget.text()

    def icon(self):
        return self.itemWidget.icon()

    def setText(self, text):
        self.itemWidget.setText(text)

    def setIcon(self, icon: Union[str, QIcon, FIF]):
        self.itemWidget.setIcon(icon)

    def textColor(self):
        return self.itemWidget.textColor()

    def setLightTextColor(self, color):
        """ set the text color in light theme mode """
        self.itemWidget.setLightTextColor(color)

    def setDarkTextColor(self, color):
        """ set the text color in dark theme mode """
        self.itemWidget.setDarkTextColor(color)

    def setTextColor(self, light, dark):
        """ set the text color in light/dark theme mode """
        self.lightTextColor = QColor(light)
        self.darkTextColor = QColor(dark)
        self.itemWidget.setTextColor(light, dark)

    def setIndicatorColor(self, light, dark):
        """ set the indicator color in light/dark theme mode """
        self.lightIndicatorColor = QColor(light)
        self.darkIndicatorColor = QColor(dark)
        self.itemWidget.setIndicatorColor(light, dark)

    def setFont(self, font: QFont):
        super().setFont(font)
        self.itemWidget.setFont(font)

    def clone(self):
        root = NavigationTreeWidget(self._icon, self.text(), self.isSelectable, self.parent())
        root.setSelected(self.isSelected)
        root.setFixedSize(self.size())
        root.setTextColor(self.lightTextColor, self.darkTextColor)
        root.setIndicatorColor(self.itemWidget.lightIndicatorColor, self.itemWidget.darkIndicatorColor)
        root.nodeDepth = self.nodeDepth

        root.clicked.connect(self.clicked)
        self.selectedChanged.connect(root.setSelected)

        for child in self.treeChildren:
            root.addChild(child.clone())

        return root

    def suitableWidth(self):
        m = self.itemWidget._margins()
        left = 57 + m.left() if not self.icon().isNull() else m.left() + 29
        tw = self.itemWidget.fontMetrics().boundingRect(self.text()).width()
        return left + tw + m.right()

    def insertChild(self, index, child):
        if child in self.treeChildren:
            return

        child.treeParent = self
        child.nodeDepth = self.nodeDepth + 1
        child.setVisible(self.isExpanded)
        child.expandAni.valueChanged.connect(lambda: self.setFixedSize(self.sizeHint()))
        child.expandAni.valueChanged.connect(self.expanded)

        # connect height changed signal to parent recursively
        p = self.treeParent
        while p:
            child.expandAni.valueChanged.connect(lambda v, p=p: p.setFixedSize(p.sizeHint()))
            p = p.treeParent

        if index < 0:
            index = len(self.treeChildren)

        index += 1  # item widget should always be the first
        self.treeChildren.insert(index, child)
        self.vBoxLayout.insertWidget(index, child, 0, Qt.AlignmentFlag.AlignTop)

        # adjust height
        if self.isExpanded:
            self.setFixedHeight(self.height() + child.height() + self.vBoxLayout.spacing())

            p = self.treeParent
            while p:
                p.setFixedSize(p.sizeHint())
                p = p.treeParent

        self.update()

    def removeChild(self, child):
        self.treeChildren.remove(child)
        self.vBoxLayout.removeWidget(child)

    def childItems(self) -> list:
        return self.treeChildren

    def setExpanded(self, isExpanded: bool, ani=False):
        """ set the expanded status """
        if isExpanded == self.isExpanded:
            return

        self.isExpanded = isExpanded
        self.itemWidget.setExpanded(isExpanded)

        for child in self.treeChildren:
            child.setVisible(isExpanded)
            child.setFixedSize(child.sizeHint())

        if ani:
            self.expandAni.stop()
            self.expandAni.setStartValue(self.geometry())
            self.expandAni.setEndValue(QRect(self.pos(), self.sizeHint()))
            self.expandAni.setDuration(120)
            self.expandAni.setEasingCurve(QEasingCurve.Type.OutQuad)
            self.expandAni.start()
        else:
            self.setFixedSize(self.sizeHint())

    def isRoot(self):
        return self.treeParent is None

    def isLeaf(self):
        return len(self.treeChildren) == 0

    def setSelected(self, isSelected: bool):
        super().setSelected(isSelected)
        self.itemWidget.setSelected(isSelected)

    def mouseReleaseEvent(self, e):
        pass

    def setCompacted(self, isCompacted: bool):
        super().setCompacted(isCompacted)
        self.itemWidget.setCompacted(isCompacted)

    def setAboutSelected(self, selected: bool):
        self.isAboutSelected = selected
        self.itemWidget.setAboutSelected(selected)

    def _onClicked(self, triggerByUser, clickArrow):
        if not self.isCompacted:
            if self.isSelectable and not self.isSelected and not clickArrow:
                self.setExpanded(True, ani=True)
            else:
                self.setExpanded(not self.isExpanded, ani=True)

        if not clickArrow or self.isCompacted:
            self.clicked.emit(triggerByUser)

    def setRememberExpandState(self, remember: bool):
        self._rememberExpandState = remember

    def saveExpandState(self):
        self._wasExpanded = self.isExpanded if self._rememberExpandState else False

    def restoreExpandState(self, ani=True):
        if self._wasExpanded:
            self.setExpanded(True, ani)


class NavigationAvatarWidget(NavigationWidget):
    """ Avatar widget """

    def __init__(self, name: str, avatar: Union[str, QPixmap, QImage] = None, parent=None):
        super().__init__(isSelectable=False, parent=parent)
        self.name = name
        self.avatar = AvatarWidget(self)

        self.avatar.setRadius(12)
        self.avatar.setText(name)
        self.avatar.move(8, 6)
        setFont(self)

        if avatar:
            self.setAvatar(avatar)

    def setName(self, name: str):
        self.name = name
        self.avatar.setText(name)
        self.update()

    def setAvatar(self, avatar: Union[str, QPixmap, QImage]):
        self.avatar.setImage(avatar)
        self.avatar.setRadius(12)
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.SmoothPixmapTransform | QPainter.RenderHint.Antialiasing)

        if self.isPressed:
            painter.setOpacity(0.7)

        self._drawBackground(painter)
        self._drawText(painter)

    def _drawText(self, painter: QPainter):
        if self.isCompacted:
            return

        painter.setPen(self.textColor())
        painter.setFont(self.font())
        painter.drawText(QRect(44, 0, 255, 36), Qt.AlignmentFlag.AlignVCenter, self.name)

    def _drawBackground(self, painter):
        if not self.isEnter:
            return

        c = 255 if isDarkTheme() else 0
        painter.setBrush(QColor(c, c, c, 10))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 5, 5)


@InfoBadgeManager.register(InfoBadgePosition.NAVIGATION_ITEM)
class NavigationItemInfoBadgeManager(InfoBadgeManager):
    """ Navigation item info badge manager """

    def eventFilter(self, obj, e: QEvent):
        if obj is self.target:
            if e.type() == QEvent.Type.Show:
                self.badge.show()

        return super().eventFilter(obj, e)

    def position(self):
        target = self.target
        self.badge.setVisible(target.isVisible())

        if target.isCompacted:
            return target.geometry().topRight() - QPoint(self.badge.width() + 2, -2)

        if isinstance(target, NavigationTreeWidget):
            dx = 10 if target.isLeaf() else 35
            x = target.geometry().right() - self.badge.width() - dx
            y = target.y() + 18 - self.badge.height() // 2
        else:
            x = target.geometry().right() - self.badge.width() - 10
            y = target.geometry().center().y() - self.badge.height() // 2

        return QPoint(x, y)


class NavigationFlyoutMenu(ScrollArea):
    """ Navigation flyout menu """

    expanded = pyqtSignal()

    def __init__(self, tree: NavigationTreeWidget, parent=None):
        super().__init__(parent)
        self.view = QWidget(self)

        self.treeWidget = tree
        self.treeChildren = []

        self.vBoxLayout = QVBoxLayout(self.view)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.enableTransparentBackground()

        self.vBoxLayout.setSpacing(5)
        self.vBoxLayout.setContentsMargins(5, 8, 5, 8)

        # add nodes to menu
        for child in tree.treeChildren:
            node = child.clone()
            node.expanded.connect(self._adjustViewSize)

            self.treeChildren.append(node)
            self.vBoxLayout.addWidget(node)

        self._initNode(self)
        self._adjustViewSize(False)

    def _initNode(self, root: NavigationTreeWidget):
        for c in root.treeChildren:
            c.nodeDepth -= 1
            c.setCompacted(False)

            if c.isLeaf():
                c.clicked.connect(self.window().fadeOut)

            self._initNode(c)

    def _adjustViewSize(self, emit=True):
        w = self._suitableWidth()

        # adjust the width of node
        for node in self.visibleTreeNodes():
            node.setFixedWidth(w - 10)
            node.itemWidget.setFixedWidth(w - 10)

        self.view.setFixedSize(w, self.view.sizeHint().height())

        h = min(self.window().parent().height() - 48, self.view.height())

        self.setFixedSize(w, h)

        if emit:
            self.expanded.emit()

    def _suitableWidth(self):
        w = 0

        for node in self.visibleTreeNodes():
            if not node.isHidden():
                w = max(w, node.suitableWidth() + 10)

        window = self.window().parent()  # type: QWidget
        return min(window.width() // 2 - 25, w) + 10

    def visibleTreeNodes(self):
        nodes = []
        queue = deque()
        queue.extend(self.treeChildren)

        while queue:
            node = queue.popleft()  # type: NavigationTreeWidget
            nodes.append(node)
            queue.extend([i for i in node.treeChildren if not i.isHidden()])

        return nodes


class NavigationUserCard(NavigationAvatarWidget):
    """ Navigation user card widget """

    def __init__(self, parent=None):
        super().__init__(name="", parent=parent)

        # text properties
        self._title = ""
        self._subtitle = ""
        self._titleSize = 14
        self._subtitleSize = 12
        self._subtitleColor = None  # type: QColor

        # animation properties
        self._textOpacity = 0.0
        self._animationDuration = 250
        self._animationGroup = QParallelAnimationGroup(self)

        # avatar size animation
        self._radiusAni = QPropertyAnimation(self.avatar, b"radius", self)
        self._radiusAni.setDuration(self._animationDuration)
        self._radiusAni.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._radiusAni.valueChanged.connect(self._updateAvatarPosition)

        # text opacity animation
        self._opacityAni = QPropertyAnimation(self, b"textOpacity", self)
        self._opacityAni.setDuration(int(self._animationDuration * 0.8))
        self._opacityAni.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self._animationGroup.addAnimation(self._radiusAni)
        self._animationGroup.addAnimation(self._opacityAni)
        self._animationGroup.finished.connect(self.update)

        # initial size
        self.setFixedSize(40, 36)

    def setAvatarIcon(self, icon: FIF):
        """ set avatar icon when no image is set """
        self.avatar.setImage(toQIcon(icon).pixmap(64, 64))
        self.update()

    def setAvatarBackgroundColor(self, light: QColor, dark: QColor):
        """ set avatar background color in light/dark theme mode """
        self.avatar.setBackgroundColor(light, dark)
        self.update()

    def title(self):
        """ get user card title """
        return self._title

    def setTitle(self, title: str):
        """ set user card title """
        self._title = title
        self.setName(title)
        self.update()

    def subtitle(self):
        """ get user card subtitle """
        return self._subtitle

    def setSubtitle(self, subtitle: str):
        """ set user card subtitle """
        self._subtitle = subtitle
        self.update()

    def setTitleFontSize(self, size: int):
        """ set title font size """
        self._titleSize = size
        self.update()

    def setSubtitleFontSize(self, size: int):
        """ set subtitle font size """
        self._subtitleSize = size
        self.update()

    def setAnimationDuration(self, duration: int):
        """ set animation duration in milliseconds """
        self._animationDuration = duration
        self._radiusAni.setDuration(duration)
        self._opacityAni.setDuration(int(duration * 0.8))

    def setCompacted(self, isCompacted: bool):
        """ set whether the widget is compacted """
        if isCompacted == self.isCompacted:
            return

        self.isCompacted = isCompacted

        if isCompacted:
            # compact mode: 24x24 avatar like NavigationAvatarWidget
            self.setFixedSize(40, 36)
            self._radiusAni.setStartValue(self.avatar.radius)
            self._radiusAni.setEndValue(12)  # 24px diameter
            self._opacityAni.setStartValue(self._textOpacity)
            self._opacityAni.setEndValue(0.0)
        else:
            # expanded mode: large avatar with text
            self.setFixedSize(self.EXPAND_WIDTH, 80)
            self._radiusAni.setStartValue(self.avatar.radius)
            self._radiusAni.setEndValue(32)  # 64px diameter
            self._opacityAni.setStartValue(self._textOpacity)
            self._opacityAni.setEndValue(1.0)

        self._animationGroup.start()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.RenderHint.SmoothPixmapTransform |
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.TextAntialiasing
        )

        if self.isPressed:
            painter.setOpacity(0.7)

        # draw hover background
        self._drawBackground(painter)

        # draw text in expanded mode
        if not self.isCompacted and self._textOpacity > 0:
            self._drawText(painter)

    def _drawText(self, painter: QPainter):
        """ draw title and subtitle """
        textX = 16 + int(self.avatar.radius * 2) + 12
        textWidth = self.width() - textX - 16

        # draw title
        painter.setFont(getFont(self._titleSize, QFont.Weight.Bold))
        c = self.textColor()
        c.setAlpha(int(255 * self._textOpacity))
        painter.setPen(c)

        titleY = self.height() // 2 - 2
        painter.drawText(QRectF(textX, 0, textWidth, titleY),
                         Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom,
                         self._title)

        # draw subtitle with semi-transparent color
        if self._subtitle:
            painter.setFont(getFont(self._subtitleSize))

            c = self.subtitleColor or self.textColor()
            c.setAlpha(int(150 * self._textOpacity))
            painter.setPen(c)

            subtitleY = self.height() // 2 + 2
            painter.drawText(QRectF(textX, subtitleY, textWidth, self.height() - subtitleY),
                             Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop,
                             self._subtitle)

    def _updateAvatarPosition(self):
        """ update avatar position based on current size """
        if self.isCompacted:
            self.avatar.move(8, 6)
        else:
            self.avatar.move(16, (self.height() - self.avatar.height()) // 2)

    # properties
    @pyqtProperty(float)
    def textOpacity(self):
        return self._textOpacity

    @textOpacity.setter
    def textOpacity(self, value: float):
        self._textOpacity = value
        self.update()

    @pyqtProperty(QColor)
    def subtitleColor(self):
        return self._subtitleColor

    @subtitleColor.setter
    def subtitleColor(self, color: QColor):
        self._subtitleColor = color
        self.update()


class NavigationIndicator(QWidget):
    """ Navigation indicator """

    aniFinished = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.lightColor = QColor()
        self.darkColor = QColor()

        self.scaleSlideAni = ScaleSlideAnimation(self, Qt.Orientation.Vertical)

        self.resize(3, 16)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.hide()

        self.scaleSlideAni.valueChanged.connect(lambda g: self.setGeometry(g.toRect()))
        self.scaleSlideAni.finished.connect(self.aniFinished)

    def startAnimation(self, startRect: QRectF, endRect: QRectF, useCrossFade=False):
        """ Start indicator animation

        Parameters
        -----------
        endRect: QRectF
            the final geometry of indicator

        useCrossFade: bool
            whether to use cross fade animation
        """
        self.setGeometry(startRect.toRect())
        self.show()

        self.scaleSlideAni.setGeometry(startRect)
        self.scaleSlideAni.startAnimation(endRect, useCrossFade)

    def stopAnimation(self):
        """ Stop animation """
        self.scaleSlideAni.stopAnimation()
        self.hide()

    def setIndicatorColor(self, light, dark):
        self.lightColor = QColor(light)
        self.darkColor = QColor(dark)
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(autoFallbackThemeColor(self.lightColor, self.darkColor))
        painter.drawRoundedRect(self.rect(), 1.5, 1.5)
