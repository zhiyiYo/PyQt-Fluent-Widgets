# coding:utf-8
from typing import List, Union
from PyQt6.QtCore import QEvent, Qt, QPropertyAnimation, pyqtProperty, QEasingCurve, QRectF
from PyQt6.QtGui import QColor, QPainter, QIcon, QPainterPath
from PyQt6.QtWidgets import QFrame, QWidget, QAbstractButton, QApplication, QScrollArea, QVBoxLayout

from ...common.config import isDarkTheme
from ...common.icon import FluentIcon as FIF
from ...common.style_sheet import FluentStyleSheet
from .setting_card import SettingCard
from ..layout.v_box_layout import VBoxLayout


class ExpandButton(QAbstractButton):
    """ Expand button """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(30, 30)
        self.__angle = 0
        self.isHover = False
        self.isPressed = False
        self.rotateAni = QPropertyAnimation(self, b'angle', self)
        self.clicked.connect(self.__onClicked)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing |
                               QPainter.RenderHint.SmoothPixmapTransform)
        painter.setPen(Qt.PenStyle.NoPen)

        # draw background
        r = 255 if isDarkTheme() else 0
        color = Qt.GlobalColor.transparent

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
        self.setExpand(self.angle < 180)

    def setExpand(self, isExpand: bool):
        self.rotateAni.stop()
        self.rotateAni.setEndValue(180 if isExpand else 0)
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
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedHeight(1)


class HeaderSettingCard(SettingCard):
    """ Header setting card """

    def __init__(self, icon, title, content=None, parent=None):
        super().__init__(icon, title, content, parent)
        self.expandButton = ExpandButton(self)

        self.hBoxLayout.addWidget(self.expandButton, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(8)

        self.titleLabel.setObjectName("titleLabel")
        self.installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self:
            if e.type() == QEvent.Type.Enter:
                self.expandButton.setHover(True)
            elif e.type() == QEvent.Type.Leave:
                self.expandButton.setHover(False)
            elif e.type() == QEvent.Type.MouseButtonPress and e.button() == Qt.MouseButton.LeftButton:
                self.expandButton.setPressed(True)
            elif e.type() == QEvent.Type.MouseButtonRelease and e.button() == Qt.MouseButton.LeftButton:
                self.expandButton.setPressed(False)
                self.expandButton.click()

        return super().eventFilter(obj, e)

    def addWidget(self, widget: QWidget):
        """ add widget to tail """
        N = self.hBoxLayout.count()
        self.hBoxLayout.removeItem(self.hBoxLayout.itemAt(N - 1))
        self.hBoxLayout.addWidget(widget, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(19)
        self.hBoxLayout.addWidget(self.expandButton, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(8)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)

        if isDarkTheme():
            painter.setBrush(QColor(255, 255, 255, 13))
        else:
            painter.setBrush(QColor(255, 255, 255, 170))

        p = self.parent()  # type: ExpandSettingCard
        path = QPainterPath()
        path.setFillRule(Qt.FillRule.WindingFill)
        path.addRoundedRect(QRectF(self.rect().adjusted(1, 1, -1, -1)), 6, 6)

        # set the bottom border radius to 0 if parent is expanded
        if p.isExpand:
            path.addRect(1, self.height() - 8, self.width() - 2, 8)

        painter.drawPath(path.simplified())


class ExpandBorderWidget(QWidget):
    """ Expand setting card border widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        parent.installEventFilter(self)

    def eventFilter(self, obj, e):
        if obj is self.parent() and e.type() == QEvent.Type.Resize:
            self.resize(e.size())

        return super().eventFilter(obj, e)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.BrushStyle.NoBrush)

        if isDarkTheme():
            painter.setPen(QColor(0, 0, 0, 50))
        else:
            painter.setPen(QColor(0, 0, 0, 19))

        p = self.parent()  # type: ExpandSettingCard
        r, d = 6, 12
        ch, h, w = p.card.height(), self.height(), self.width()

        # only draw rounded rect if parent is not expanded
        painter.drawRoundedRect(self.rect().adjusted(1, 1, -1, -1), r, r)

        # draw the seperator line under card widget
        if ch < h:
            painter.drawLine(1, ch, w - 1, ch)



class ExpandSettingCard(QScrollArea):
    """ Expandable setting card """

    def __init__(self, icon: Union[str, QIcon, FIF], title: str, content: str = None, parent=None):
        super().__init__(parent=parent)
        self.isExpand = False

        self.scrollWidget = QFrame(self)
        self.view = QFrame(self.scrollWidget)
        self.card = HeaderSettingCard(icon, title, content, self)

        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.viewLayout = QVBoxLayout(self.view)
        self.spaceWidget = SpaceWidget(self.scrollWidget)
        self.borderWidget = ExpandBorderWidget(self)

        # expand animation
        self.expandAni = QPropertyAnimation(self.verticalScrollBar(), b'value', self)

        self.__initWidget()

    def __initWidget(self):
        """ initialize widgets """
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setFixedHeight(self.card.height())
        self.setViewportMargins(0, self.card.height(), 0, 0)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # initialize layout
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setSpacing(0)
        self.scrollLayout.addWidget(self.view)
        self.scrollLayout.addWidget(self.spaceWidget)

        # initialize expand animation
        self.expandAni.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.expandAni.setDuration(200)

        # initialize style sheet
        self.view.setObjectName('view')
        self.scrollWidget.setObjectName('scrollWidget')
        self.setProperty('isExpand', False)
        FluentStyleSheet.EXPAND_SETTING_CARD.apply(self.card)
        FluentStyleSheet.EXPAND_SETTING_CARD.apply(self)

        self.card.installEventFilter(self)
        self.expandAni.valueChanged.connect(self._onExpandValueChanged)
        self.card.expandButton.clicked.connect(self.toggleExpand)

    def addWidget(self, widget: QWidget):
        """ add widget to tail """
        self.card.addWidget(widget)

    def wheelEvent(self, e):
        pass

    def setExpand(self, isExpand: bool):
        """ set the expand status of card """
        if self.isExpand == isExpand:
            return

        # update style sheet
        self.isExpand = isExpand
        self.setProperty('isExpand', isExpand)
        self.setStyle(QApplication.style())

        # start expand animation
        if isExpand:
            h = self.viewLayout.sizeHint().height()
            self.verticalScrollBar().setValue(h)
            self.expandAni.setStartValue(h)
            self.expandAni.setEndValue(0)
        else:
            self.expandAni.setStartValue(0)
            self.expandAni.setEndValue(self.verticalScrollBar().maximum())

        self.expandAni.start()
        self.card.expandButton.setExpand(isExpand)

    def toggleExpand(self):
        """ toggle expand status """
        self.setExpand(not self.isExpand)

    def resizeEvent(self, e):
        self.card.resize(self.width(), self.card.height())
        self.scrollWidget.resize(self.width(), self.scrollWidget.height())

    def _onExpandValueChanged(self):
        vh = self.viewLayout.sizeHint().height()
        h = self.viewportMargins().top()
        self.setFixedHeight(max(h + vh - self.verticalScrollBar().value(), h))

    def _adjustViewSize(self):
        """ adjust view size """
        h = self.viewLayout.sizeHint().height()
        self.spaceWidget.setFixedHeight(h)

        if self.isExpand:
            self.setFixedHeight(self.card.height()+h)

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
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        if isDarkTheme():
            painter.setPen(QColor(0, 0, 0, 50))
        else:
            painter.setPen(QColor(0, 0, 0, 19))

        painter.drawLine(0, 1, self.width(), 1)


class ExpandGroupSettingCard(ExpandSettingCard):
    """ Expand group setting card """

    def __init__(self, icon: Union[str, QIcon, FIF], title: str, content: str = None, parent=None):
        super().__init__(icon, title, content, parent)
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
            self.setFixedHeight(self.card.height()+h)


class SimpleExpandGroupSettingCard(ExpandGroupSettingCard):
    """ Simple expand group setting card """

    def _adjustViewSize(self):
        """ adjust view size """
        h = self.viewLayout.sizeHint().height()
        self.spaceWidget.setFixedHeight(h)

        if self.isExpand:
            self.setFixedHeight(self.card.height()+h)
