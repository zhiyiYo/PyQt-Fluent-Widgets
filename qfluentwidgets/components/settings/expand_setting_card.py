# coding:utf-8
from enum import Enum
from typing import List, Union
from PyQt5.QtCore import QEvent, Qt, QPropertyAnimation, pyqtProperty, QEasingCurve, QRectF, QTimer
from PyQt5.QtGui import QColor, QPainter, QIcon, QPainterPath
from PyQt5.QtWidgets import QFrame, QWidget, QAbstractButton, QApplication, QScrollArea, QVBoxLayout, QLabel, QHBoxLayout

from ...common.config import isDarkTheme
from ...common.icon import FluentIcon as FIF
from ...common.style_sheet import FluentStyleSheet
from .setting_card import SettingCard, SettingIconWidget
from ..layout.v_box_layout import VBoxLayout


class ExpandPosition(Enum):
    """ Expand position """
    UP = 0
    DOWN = 1


class ExpandButton(QAbstractButton):
    """ Expand button """

    def __init__(self, parent=None, expandPosition=ExpandPosition.DOWN):
        super().__init__(parent)
        self.setFixedSize(30, 30)
        self._expandPosition = expandPosition
        # initial angle: 0 for DOWN, 180 for UP
        self.__angle = 0 if expandPosition == ExpandPosition.DOWN else 180
        self.isHover = False
        self.isPressed = False
        self.rotateAni = QPropertyAnimation(self, b'angle', self)
        self.clicked.connect(self.__onClicked)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)
        painter.setPen(Qt.NoPen)

        # draw background
        r = 255 if isDarkTheme() else 0
        color = Qt.transparent

        if self.isEnabled():
            if self.isPressed:
                color = QColor(r, r, r, 10)
            elif self.isHover:
                color = QColor(r, r, r, 14)
        else:
            painter.setOpacity(0.36)

        painter.setBrush(color)
        painter.drawRoundedRect(self.rect(), 4, 4)

        # draw icon
        painter.translate(self.width()//2, self.height()//2)
        painter.rotate(self.__angle)
        FIF.ARROW_DOWN.render(painter, QRectF(-5, -5, 9.6, 9.6))

    def enterEvent(self, e):
        self.setHover(True)

    def leaveEvent(self, e):
        self.setHover(False)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.setPressed(True)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.setPressed(False)

    def setHover(self, isHover: bool):
        self.isHover = isHover
        self.update()

    def setPressed(self, isPressed: bool):
        self.isPressed = isPressed
        self.update()

    def __onClicked(self):
        # check expand state based on position
        if self._expandPosition == ExpandPosition.DOWN:
            self.setExpand(self.angle < 180)
        else:
            self.setExpand(self.angle > 0)

    def setExpand(self, isExpand: bool):
        self.rotateAni.stop()
        if self._expandPosition == ExpandPosition.DOWN:
            self.rotateAni.setEndValue(180 if isExpand else 0)
        else:
            self.rotateAni.setEndValue(0 if isExpand else 180)
        self.rotateAni.setDuration(200)
        self.rotateAni.start()

    def getAngle(self):
        return self.__angle

    def setAngle(self, angle):
        self.__angle = angle
        self.update()

    angle = pyqtProperty(float, getAngle, setAngle)


class SpaceWidget(QWidget):
    """ Spacing widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedHeight(1)


class HeaderSettingCard(SettingCard):
    """ Header setting card """

    def __init__(self, icon, title, content=None, parent=None, expandPosition=ExpandPosition.DOWN):
        super().__init__(icon, title, content, parent)
        self._expandPosition = expandPosition
        self.expandButton = ExpandButton(self, expandPosition)

        self.hBoxLayout.addWidget(self.expandButton, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(8)

        self.titleLabel.setObjectName("titleLabel")
        self.installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self:
            if e.type() == QEvent.Enter:
                self.expandButton.setHover(True)
            elif e.type() == QEvent.Leave:
                self.expandButton.setHover(False)
            elif e.type() == QEvent.MouseButtonPress and e.button() == Qt.LeftButton:
                self.expandButton.setPressed(True)
            elif e.type() == QEvent.MouseButtonRelease and e.button() == Qt.LeftButton:
                self.expandButton.setPressed(False)
                self.expandButton.click()

        return super().eventFilter(obj, e)

    def addWidget(self, widget: QWidget):
        """ add widget to tail """
        N = self.hBoxLayout.count()
        self.hBoxLayout.removeItem(self.hBoxLayout.itemAt(N - 1))
        self.hBoxLayout.addWidget(widget, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(19)
        self.hBoxLayout.addWidget(self.expandButton, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(8)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)

        if isDarkTheme():
            painter.setBrush(QColor(255, 255, 255, 13))
        else:
            painter.setBrush(QColor(255, 255, 255, 170))

        p = self.parent()  # type: ExpandSettingCard
        path = QPainterPath()
        path.setFillRule(Qt.WindingFill)
        path.addRoundedRect(QRectF(self.rect().adjusted(1, 1, -1, -1)), 6, 6)

        # adjust border radius based on expand state and position
        if hasattr(p, 'isExpand') and p.isExpand:
            if self._expandPosition == ExpandPosition.DOWN:
                # expand down: bottom corners should be square
                path.addRect(1, self.height() - 8, self.width() - 2, 8)
            else:
                # expand up: top corners should be square
                path.addRect(1, 0, self.width() - 2, 8)

        painter.drawPath(path.simplified())


class ExpandBorderWidget(QWidget):
    """ Expand setting card border widget """

    def __init__(self, parent=None, expandPosition=ExpandPosition.DOWN):
        super().__init__(parent=parent)
        self._expandPosition = expandPosition
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        parent.installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.parent() and e.type() == QEvent.Resize:
            self.resize(e.size())

        return super().eventFilter(obj, e)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)

        if isDarkTheme():
            painter.setPen(QColor(0, 0, 0, 50))
        else:
            painter.setPen(QColor(0, 0, 0, 19))

        p = self.parent()  # type: ExpandSettingCard
        r, d = 6, 12
        ch, h, w = p.card.height(), self.height(), self.width()

        # draw rounded rect border
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), r, r)

        # draw separator line based on expand position
        if ch < h:
            if self._expandPosition == ExpandPosition.DOWN:
                # separator below header
                painter.drawLine(1, ch, w - 1, ch)
            else:
                # separator above header
                painter.drawLine(1, h - ch, w - 1, h - ch)



class ExpandSettingCard(QScrollArea):
    """ Expandable setting card """

    def __init__(self, icon: Union[str, QIcon, FIF], title: str, content: str = None,
                 parent=None, expandPosition: ExpandPosition = ExpandPosition.DOWN):
        super().__init__(parent=parent)
        self.isExpand = False
        self._expandPosition = expandPosition

        self.scrollWidget = QFrame(self)
        self.view = QFrame(self.scrollWidget)
        self.card = HeaderSettingCard(icon, title, content, self, expandPosition)

        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.viewLayout = QVBoxLayout(self.view)
        self.spaceWidget = SpaceWidget(self.scrollWidget)
        self.borderWidget = ExpandBorderWidget(self, expandPosition)

        # expand animation
        self.expandAni = QPropertyAnimation(self.verticalScrollBar(), b'value', self)

        self.__initWidget()

    def __initWidget(self):
        """ initialize widgets """
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setFixedHeight(self.card.height())
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # set viewport margins based on expand position
        if self._expandPosition == ExpandPosition.DOWN:
            self.setViewportMargins(0, self.card.height(), 0, 0)
        else:
            self.setViewportMargins(0, 0, 0, self.card.height())

        # initialize layout
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setSpacing(0)

        # layout order depends on expand position
        if self._expandPosition == ExpandPosition.DOWN:
            self.scrollLayout.addWidget(self.view)
            self.scrollLayout.addWidget(self.spaceWidget)
        else:
            self.scrollLayout.addWidget(self.spaceWidget)
            self.scrollLayout.addWidget(self.view)

        # initialize expand animation
        self.expandAni.setEasingCurve(QEasingCurve.OutQuad)
        self.expandAni.setDuration(200)

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.setProperty('isExpand', False)

        # set view object name based on expand position
        if self._expandPosition == ExpandPosition.DOWN:
            self.view.setObjectName('view')
        else:
            self.view.setObjectName('viewUp')

        FluentStyleSheet.EXPAND_SETTING_CARD.apply(self.card)
        FluentStyleSheet.EXPAND_SETTING_CARD.apply(self)

        self.card.installEventFilter(self)
        self.expandAni.valueChanged.connect(self._onExpandValueChanged)
        self.card.expandButton.clicked.connect(self.toggleExpand)

    def addWidget(self, widget: QWidget):
        """ add widget to tail """
        self.card.addWidget(widget)
        self._adjustViewSize()

    def wheelEvent(self, e):
        pass

    def setExpand(self, isExpand: bool):
        """ set the expand status of card """
        if self.isExpand == isExpand:
            return

        self._adjustViewSize()

        # update style sheet
        self.isExpand = isExpand
        self.setProperty('isExpand', isExpand)
        self.setStyle(QApplication.style())

        # start expand animation
        h = self.viewLayout.sizeHint().height()

        if self._expandPosition == ExpandPosition.DOWN:
            # expand down: scroll from bottom to top
            if isExpand:
                self.verticalScrollBar().setValue(h)
                self.expandAni.setStartValue(h)
                self.expandAni.setEndValue(0)
            else:
                self.expandAni.setStartValue(0)
                self.expandAni.setEndValue(self.verticalScrollBar().maximum())
        else:
            # expand up: scroll from top to bottom
            if isExpand:
                self.verticalScrollBar().setValue(0)
                self.expandAni.setStartValue(0)
                self.expandAni.setEndValue(h)
            else:
                self.expandAni.setStartValue(self.verticalScrollBar().value())
                self.expandAni.setEndValue(0)

        self.expandAni.start()
        self.card.expandButton.setExpand(isExpand)

    def toggleExpand(self):
        """ toggle expand status """
        self.setExpand(not self.isExpand)

    def resizeEvent(self, e):
        self.card.resize(self.width(), self.card.height())
        self.scrollWidget.resize(self.width(), self.scrollWidget.height())

        # update card position based on expand position
        if self._expandPosition == ExpandPosition.UP:
            self.card.move(0, self.height() - self.card.height())

    def _onExpandValueChanged(self):
        vh = self.viewLayout.sizeHint().height()
        h = self.card.height()

        if self._expandPosition == ExpandPosition.DOWN:
            self.setFixedHeight(max(h + vh - self.verticalScrollBar().value(), h))
        else:
            self.setFixedHeight(max(h + self.verticalScrollBar().value(), h))
            # update card position when expanding up
            self.card.move(0, self.height() - self.card.height())

    def _adjustViewSize(self):
        """ adjust view size """
        h = self.viewLayout.sizeHint().height()
        self.spaceWidget.setFixedHeight(h)

        if self.isExpand:
            self.setFixedHeight(self.card.height() + h)
            if self._expandPosition == ExpandPosition.UP:
                self.card.move(0, self.height() - self.card.height())
                # delay scrollbar update to ensure layout is complete
                QTimer.singleShot(0, lambda: self.verticalScrollBar().setValue(h))

    def setValue(self, value):
        """ set the value of config item """
        pass



class GroupSeparator(QWidget):
    """ group separator """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(3)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        if isDarkTheme():
            painter.setPen(QColor(0, 0, 0, 50))
        else:
            painter.setPen(QColor(0, 0, 0, 19))

        painter.drawLine(0, 1, self.width(), 1)


class GroupWidget(QWidget):

    def __init__(self, icon: Union[str, QIcon, FIF], title: str, content: str, widget: QWidget, stretch=0, parent=None):
        super().__init__(parent=parent)
        self.iconWidget = SettingIconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(content, self)
        self.widget = widget

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        if not content:
            self.contentLabel.hide()

        self.iconWidget.setFixedSize(16, 16)
        self.setMinimumHeight(60)
        self.setIcon(icon)

        # initialize layout
        self.hBoxLayout.setSpacing(16)
        self.hBoxLayout.setContentsMargins(48, 12, 48, 12)
        self.hBoxLayout.setAlignment(Qt.AlignVCenter)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.addWidget(self.iconWidget, 0, Qt.AlignLeft)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignLeft)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(widget, stretch)

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')

    def setTitle(self, title: str):
        self.titleLabel.setText(title)

    def setContent(self, content: str):
        self.contentLabel.setText(content)
        self.contentLabel.setVisible(bool(content))

    def setIconSize(self, width: int, height: int):
        """ set the icon fixed size """
        self.iconWidget.setFixedSize(width, height)

    def setIcon(self, icon: Union[str, QIcon, FIF]):
        self.iconWidget.setIcon(icon)
        self.iconWidget.setHidden(self.iconWidget.icon.isNull())



class ExpandGroupSettingCard(ExpandSettingCard):
    """ Expand group setting card """

    def __init__(self, icon: Union[str, QIcon, FIF], title: str, content: str = None,
                 parent=None, expandPosition: ExpandPosition = ExpandPosition.DOWN):
        super().__init__(icon, title, content, parent, expandPosition)
        self.widgets = []   # type: List[QWidget]

        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        self.viewLayout.setSpacing(0)

    def addGroupWidget(self, widget: QWidget):
        """ add widget to group """
        # add separator
        if self.viewLayout.count() >= 1:
            self.viewLayout.addWidget(GroupSeparator(self.view))

        widget.setParent(self.view)
        self.widgets.append(widget)
        self.viewLayout.addWidget(widget)
        self._adjustViewSize()

    def addGroup(self, icon: Union[str, QIcon, FIF], title: str, content: str, widget: QWidget, stretch=0) -> GroupWidget:
        """ add group

        Parameters
        ----------
        icon: str | QIcon | FluentIconBase
            the icon of group

        title: str
            the title of group

        content: str
            the description of group

        widget: str
            the widget of group

        stretch: int
            the stretch of widget
        """
        group = GroupWidget(icon, title, content, widget, stretch)
        self.addGroupWidget(group)
        return group

    def removeGroupWidget(self, widget: QWidget):
        """ remove a group from card """
        if widget not in self.widgets:
            return

        layoutIndex = self.viewLayout.indexOf(widget)
        index = self.widgets.index(widget)

        self.viewLayout.removeWidget(widget)
        self.widgets.remove(widget)

        if not self.widgets:
            return self._adjustViewSize()

        # remove separator
        if layoutIndex >= 1:
            separator = self.viewLayout.itemAt(layoutIndex - 1).widget()
            separator.deleteLater()
            self.viewLayout.removeWidget(separator)
        elif index == 0:
            separator = self.viewLayout.itemAt(0).widget()
            separator.deleteLater()
            self.viewLayout.removeWidget(separator)

        self._adjustViewSize()

    def _adjustViewSize(self):
        """ adjust view size """
        h = sum(w.sizeHint().height() + 3 for w in self.widgets)
        self.spaceWidget.setFixedHeight(h)

        if self.isExpand:
            self.setFixedHeight(self.card.height() + h)
            if self._expandPosition == ExpandPosition.UP:
                self.card.move(0, self.height() - self.card.height())
                # delay scrollbar update to ensure layout is complete
                QTimer.singleShot(0, lambda: self.verticalScrollBar().setValue(h))


class SimpleExpandGroupSettingCard(ExpandGroupSettingCard):
    """ Simple expand group setting card """

    def __init__(self, icon: Union[str, QIcon, FIF], title: str, content: str = None,
                 parent=None, expandPosition: ExpandPosition = ExpandPosition.DOWN):
        super().__init__(icon, title, content, parent, expandPosition)

    def _adjustViewSize(self):
        """ adjust view size """
        h = self.viewLayout.sizeHint().height()
        self.spaceWidget.setFixedHeight(h)

        if self.isExpand:
            self.setFixedHeight(self.card.height() + h)
            if self._expandPosition == ExpandPosition.UP:
                self.card.move(0, self.height() - self.card.height())
                # delay scrollbar update to ensure layout is complete
                QTimer.singleShot(0, lambda: self.verticalScrollBar().setValue(h))
