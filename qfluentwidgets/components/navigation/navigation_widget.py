# coding:utf-8
from typing import Union, List

from PySide6.QtCore import (Qt, Signal, QRect, QRectF, QPropertyAnimation, Property, QMargins,
                          QEasingCurve, QPoint, QEvent, QSize)
from PySide6.QtGui import QColor, QPainter, QPen, QIcon, QCursor, QFont, QBrush, QPixmap, QImage
from PySide6.QtWidgets import QWidget, QVBoxLayout
from collections import deque

from ...common.config import isDarkTheme
from ...common.style_sheet import themeColor
from ...common.icon import drawIcon, toQIcon
from ...common.icon import FluentIcon as FIF
from ...common.font import setFont
from ..widgets.scroll_area import ScrollArea
from ..widgets.info_badge import InfoBadgeManager, InfoBadgePosition


class NavigationWidget(QWidget):
    """ Navigation widget """

    clicked = Signal(bool)  # whether triggered by the user
    selectedChanged = Signal(bool)
    EXPAND_WIDTH = 312

    def __init__(self, isSelectable: bool, parent=None):
        super().__init__(parent)
        self.isCompacted = True
        self.isSelected = False
        self.isPressed = False
        self.isEnter = False
        self.isSelectable = isSelectable
        self.treeParent = None
        self.nodeDepth = 0
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
        self.update()
        self.selectedChanged.emit(isSelected)


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

    def _margins(self):
        return QMargins(0, 0, 0, 0)

    def _canDrawIndicator(self):
        return self.isSelected

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)

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
            painter.setBrush(themeColor())
            painter.drawRoundedRect(pl, 10, 3, 16, 1.5, 1.5)
        elif self.isEnter and self.isEnabled() and globalRect.contains(QCursor.pos()):
            painter.setBrush(QColor(c, c, c, 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

        drawIcon(self._icon, painter, QRectF(11.5+pl, 10, 16, 16))

        # draw text
        if self.isCompacted:
            return

        painter.setFont(self.font())
        painter.setPen(QColor(c, c, c))

        left = 44 + pl if not self.icon().isNull() else pl + 16
        painter.drawText(QRectF(left, 0, self.width()-13-left-pr, self.height()), Qt.AlignVCenter, self.text())


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


class NavigationTreeItem(NavigationPushButton):
    """ Navigation tree item widget """

    itemClicked = Signal(bool, bool)    # triggerByUser, clickArrow

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
        clickArrow = QRectF(self.width()-30, 8, 20, 20).contains(e.pos())
        self.itemClicked.emit(True, clickArrow and not self.parent().isLeaf())
        self.update()

    def _canDrawIndicator(self):
        p = self.parent()   # type: NavigationTreeWidget
        if p.isLeaf() or p.isSelected:
            return p.isSelected

        for child in p.treeChildren:
            if child.itemWidget._canDrawIndicator() and not child.isVisible():
                return True

        return False

    def _margins(self):
        p = self.parent()   # type: NavigationTreeWidget
        return QMargins(p.nodeDepth*28, 0, 20*bool(p.treeChildren), 0)

    def paintEvent(self, e):
        super().paintEvent(e)
        if self.isCompacted or not self.parent().treeChildren:
            return

        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        if self.isPressed:
            painter.setOpacity(0.7)
        if not self.isEnabled():
            painter.setOpacity(0.4)

        painter.translate(self.width() - 20, 18)
        painter.rotate(self.arrowAngle)
        FIF.ARROW_DOWN.render(painter, QRectF(-5, -5, 9.6, 9.6))

    def getArrowAngle(self):
        return self._arrowAngle

    def setArrowAngle(self, angle):
        self._arrowAngle = angle
        self.update()

    arrowAngle = Property(float, getArrowAngle, setArrowAngle)


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


class NavigationTreeWidget(NavigationTreeWidgetBase):
    """ Navigation tree widget """

    expanded = Signal()

    def __init__(self, icon: Union[str, QIcon, FIF], text: str, isSelectable: bool, parent=None):
        super().__init__(isSelectable, parent)

        self.treeChildren = []  # type: List[NavigationTreeWidget]
        self.isExpanded = False
        self._icon = icon

        self.itemWidget = NavigationTreeItem(icon, text, isSelectable, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.expandAni = QPropertyAnimation(self, b'geometry', self)

        self.__initWidget()

    def __initWidget(self):
        self.vBoxLayout.setSpacing(4)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.itemWidget, 0, Qt.AlignTop)

        self.itemWidget.itemClicked.connect(self._onClicked)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.expandAni.valueChanged.connect(lambda g: self.setFixedSize(g.size()))
        self.expandAni.valueChanged.connect(self.expanded)

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

    def setFont(self, font: QFont):
        super().setFont(font)
        self.itemWidget.setFont(font)

    def clone(self):
        root = NavigationTreeWidget(self._icon, self.text(), self.isSelectable, self.parent())
        root.setSelected(self.isSelected)
        root.setFixedSize(self.size())
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
        self.vBoxLayout.insertWidget(index, child, 0, Qt.AlignTop)

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
            self.expandAni.setEasingCurve(QEasingCurve.OutQuad)
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

    def _onClicked(self, triggerByUser, clickArrow):
        if not self.isCompacted:
            if self.isSelectable and not self.isSelected and not clickArrow:
                self.setExpanded(True, ani=True)
            else:
                self.setExpanded(not self.isExpanded, ani=True)

        if not clickArrow or self.isCompacted:
            self.clicked.emit(triggerByUser)


class NavigationAvatarWidget(NavigationWidget):
    """ Avatar widget """

    def __init__(self, name: str, avatar: Union[str, QPixmap, QImage], parent=None):
        super().__init__(isSelectable=False, parent=parent)
        self.name = name
        self.setAvatar(avatar)
        setFont(self)

    def setName(self, name: str):
        self.name = name
        self.update()

    def setAvatar(self, avatar: Union[str, QPixmap, QImage]):
        if isinstance(avatar, str):
            avatar = QImage(avatar)
        elif isinstance(avatar, QPixmap):
            avatar = avatar.toImage()

        self.avatar = avatar.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.SmoothPixmapTransform | QPainter.Antialiasing)

        painter.setPen(Qt.NoPen)

        if self.isPressed:
            painter.setOpacity(0.7)

        # draw background
        if self.isEnter:
            c = 255 if isDarkTheme() else 0
            painter.setBrush(QColor(c, c, c, 10))
            painter.drawRoundedRect(self.rect(), 5, 5)

        # draw avatar
        painter.setBrush(QBrush(self.avatar))
        painter.translate(8, 6)
        painter.drawEllipse(0, 0, 24, 24)
        painter.translate(-8, -6)

        if not self.isCompacted:
            painter.setPen(Qt.white if isDarkTheme() else Qt.black)
            painter.setFont(self.font())
            painter.drawText(QRect(44, 0, 255, 36), Qt.AlignVCenter, self.name)


@InfoBadgeManager.register(InfoBadgePosition.NAVIGATION_ITEM)
class NavigationItemInfoBadgeManager(InfoBadgeManager):
    """ Navigation item info badge manager """

    def eventFilter(self, obj, e: QEvent):
        if obj is self.target:
            if e.type() == QEvent.Show:
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

    expanded = Signal()

    def __init__(self, tree: NavigationTreeWidget, parent=None):
        super().__init__(parent)
        self.view = QWidget(self)

        self.treeWidget = tree
        self.treeChildren = []

        self.vBoxLayout = QVBoxLayout(self.view)

        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("ScrollArea{border:none;background:transparent}")
        self.view.setStyleSheet("QWidget{border:none;background:transparent}")

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