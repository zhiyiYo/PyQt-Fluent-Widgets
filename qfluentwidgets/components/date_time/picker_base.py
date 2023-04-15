# coding:utf-8
from typing import Iterable, List

from PyQt5.QtCore import QEvent, Qt, pyqtSignal, QSize, QRectF, QPoint, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QPainter, QCursor, QRegion
from PyQt5.QtWidgets import (QApplication, QWidget, QFrame, QVBoxLayout, QHBoxLayout,
                             QGraphicsDropShadowEffect, QSizePolicy, QPushButton, QListWidgetItem)

from ..widgets.cycle_list_widget import CycleListWidget
from ..widgets.button import TransparentToolButton
from ...common.icon import FluentIcon
from ...common.style_sheet import FluentStyleSheet, themeColor, isDarkTheme


class SeparatorWidget(QWidget):
    """ Separator widget """

    def __init__(self, orient: Qt.Orientation, parent=None):
        super().__init__(parent=parent)
        if orient == Qt.Horizontal:
            self.setFixedHeight(1)
        else:
            self.setFixedWidth(1)

        self.setAttribute(Qt.WA_StyledBackground)
        FluentStyleSheet.TIME_PICKER.apply(self)


class ItemMaskWidget(QWidget):
    """ Item mask widget """

    def __init__(self, listWidgets: List[CycleListWidget], parent=None):
        super().__init__(parent=parent)
        self.listWidgets = listWidgets
        self.setFixedHeight(37)
        FluentStyleSheet.TIME_PICKER.apply(self)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.TextAntialiasing)

        # draw background
        painter.setPen(Qt.NoPen)
        painter.setBrush(themeColor())
        painter.drawRoundedRect(self.rect().adjusted(4, 0, -3, 0), 5, 5)

        # draw text
        painter.setPen(Qt.black if isDarkTheme() else Qt.white)
        painter.setFont(self.font())
        w, h = 0, self.height()
        for i, p in enumerate(self.listWidgets):
            painter.save()

            # draw first item's text
            x = p.itemSize.width()//2 + 4 + self.x()
            item1 = p.itemAt(QPoint(x, self.y() + 6))
            if not item1:
                painter.restore()
                continue

            iw = item1.sizeHint().width()
            y = p.visualItemRect(item1).y()
            painter.translate(w, y - self.y() + 7)
            self._drawText(item1, painter, 0)

            # draw second item's text
            item2 = p.itemAt(self.pos() + QPoint(x, h - 6))
            self._drawText(item2, painter, h)

            painter.restore()
            w += (iw + 8)  # margin: 0 4px;

    def _drawText(self, item: QListWidgetItem, painter: QPainter, y: int):
        align = item.textAlignment()
        w, h = item.sizeHint().width(), item.sizeHint().height()
        if align & Qt.AlignLeft:
            rect = QRectF(15, y, w, h)      # padding-left: 11px
        elif align & Qt.AlignRight:
            rect = QRectF(4, y, w-15, h)    # padding-right: 11px
        elif align & Qt.AlignCenter:
            rect = QRectF(4, y, w, h)

        painter.drawText(rect, align, item.text())


class PickerColumn:
    """ Picker column """

    def __init__(self, name: str, items: list, width: int, align=Qt.AlignLeft):
        self.name = name
        self.items = items
        self.width = width
        self.align = align
        self.value = None   # type: str


class PickerBase(QPushButton):
    """ Picker base class """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.columns = []   # type: List[PickerColumn]
        self.columnMap = {}
        self.buttons = []   # type: List[QPushButton]

        self.hBoxLayout = QHBoxLayout(self)

        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.setSizeConstraint(QHBoxLayout.SetFixedSize)

        FluentStyleSheet.TIME_PICKER.apply(self)
        self.clicked.connect(self._showPanel)

    def addColumn(self, name: str, items: Iterable, width: int, align=Qt.AlignCenter):
        """ add column

        Parameters
        ----------
        name: str
            the name of column

        items: Iterable
            the items of column

        width: int
            the width of column

        align: Qt.AlignmentFlag
            the text alignment of button
        """
        if name in self.columnMap:
            return

        # create column
        column = PickerColumn(name, list(items), width, align)
        self.columns.append(column)
        self.columnMap[name] = column

        # create button
        button = QPushButton(name, self)
        button.setFixedSize(width, 30)
        button.setObjectName('pickerButton')
        button.setProperty('hasBorder', False)
        button.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.hBoxLayout.addWidget(button, 0, Qt.AlignLeft)
        self.buttons.append(button)

        if align == Qt.AlignLeft:
            button.setProperty('align', 'left')
        elif align == Qt.AlignRight:
            button.setProperty('align', 'right')

        # update the style of buttons
        for btn in self.buttons[:-1]:
            btn.setProperty('hasBorder', True)
            btn.setStyle(QApplication.style())

    def value(self):
        return [c.value for c in self.columns]

    def setColumnValue(self, index: int, value):
        if not 0 <= index < len(self.columns):
            return

        value = str(value)
        self.columns[index].value = value
        self.buttons[index].setText(value)
        self._setButtonProperty('hasValue', True)

    def enterEvent(self, e):
        self._setButtonProperty('enter', True)

    def leaveEvent(self, e):
        self._setButtonProperty('enter', False)

    def mousePressEvent(self, e):
        self._setButtonProperty('pressed', True)
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self._setButtonProperty('pressed', False)
        super().mouseReleaseEvent(e)

    def _setButtonProperty(self, name, value):
        """ send event to picker buttons """
        for button in self.buttons:
            button.setProperty(name, value)
            button.setStyle(QApplication.style())

    def _showPanel(self):
        """ show panel """
        panel = PickerPanel(self)
        for column in self.columns:
            panel.addColumn(column.items, column.width, column.align)

        panel.setValue(self.value())
        panel.confirmed.connect(self._onConfirmed)
        panel.exec(self.mapToGlobal(QPoint(0, -37*4)))

    def _onConfirmed(self, value: list):
        for i, v in enumerate(value):
            self.setColumnValue(i, v)


class PickerPanel(QWidget):
    """ picker panel """

    confirmed = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.itemHeight = 37
        self.listWidgets = []   # type: List[CycleListWidget]

        self.view = QFrame(self)
        self.itemMaskWidget = ItemMaskWidget(self.listWidgets, self)
        self.hSeparatorWidget = SeparatorWidget(Qt.Horizontal, self.view)
        self.yesButton = TransparentToolButton(FluentIcon.ACCEPT, self.view)
        self.cancelButton = TransparentToolButton(FluentIcon.CLOSE, self.view)

        self.hBoxLayout = QHBoxLayout(self)
        self.listLayout = QHBoxLayout()
        self.buttonLayout = QHBoxLayout()
        self.vBoxLayout = QVBoxLayout(self.view)

        self.__initWidget()

    def __initWidget(self):
        self.setWindowFlags(Qt.Popup | Qt.FramelessWindowHint |
                            Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setShadowEffect()
        self.yesButton.setIconSize(QSize(16, 16))
        self.cancelButton.setIconSize(QSize(13, 13))
        self.yesButton.setFixedHeight(33)
        self.cancelButton.setFixedHeight(33)

        self.hBoxLayout.setContentsMargins(12, 8, 12, 20)
        self.hBoxLayout.addWidget(self.view, 1, Qt.AlignCenter)
        self.hBoxLayout.setSizeConstraint(QHBoxLayout.SetMinimumSize)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.listLayout, 1)
        self.vBoxLayout.addWidget(self.hSeparatorWidget)
        self.vBoxLayout.addLayout(self.buttonLayout, 1)
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SetMinimumSize)

        self.buttonLayout.setSpacing(6)
        self.buttonLayout.setContentsMargins(3, 3, 3, 3)
        self.buttonLayout.addWidget(self.yesButton)
        self.buttonLayout.addWidget(self.cancelButton)
        self.yesButton.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cancelButton.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.yesButton.clicked.connect(self._fadeOut)
        self.yesButton.clicked.connect(
            lambda: self.confirmed.emit(self.value()))
        self.cancelButton.clicked.connect(self._fadeOut)

        self.view.setObjectName('view')
        FluentStyleSheet.TIME_PICKER.apply(self)

    def setShadowEffect(self, blurRadius=30, offset=(0, 8), color=QColor(0, 0, 0, 30)):
        """ add shadow to dialog """
        self.shadowEffect = QGraphicsDropShadowEffect(self.view)
        self.shadowEffect.setBlurRadius(blurRadius)
        self.shadowEffect.setOffset(*offset)
        self.shadowEffect.setColor(color)
        self.view.setGraphicsEffect(None)
        self.view.setGraphicsEffect(self.shadowEffect)

    def addColumn(self, items: Iterable, width: int, align=Qt.AlignCenter):
        """ add one column to view

        Parameters
        ----------
        items: Iterable[Any]
            the items to be added

        width: int
            the width of item

        align: Qt.AlignmentFlag
            the text alignment of item
        """
        if self.listWidgets:
            self.listLayout.addWidget(SeparatorWidget(Qt.Vertical))

        w = CycleListWidget(items, QSize(width, self.itemHeight), align, self)
        w.vScrollBar.valueChanged.connect(self.itemMaskWidget.update)

        self.listWidgets.append(w)
        self.listLayout.addWidget(w)

    def resizeEvent(self, e):
        self.itemMaskWidget.resize(self.view.width()-3, self.itemHeight)
        m = self.hBoxLayout.contentsMargins()
        self.itemMaskWidget.move(m.left()+2, m.top() + 148)

    def value(self):
        return [i.currentItem().text() for i in self.listWidgets]

    def setValue(self, value: list):
        for v, w in zip(value, self.listWidgets):
            w.setSelectedItem(v)

    def exec(self, pos, ani=True):
        """ show menu

        Parameters
        ----------
        pos: QPoint
            pop-up position

        ani: bool
            Whether to show pop-up animation
        """
        if self.isVisible():
            return

        rect = QApplication.screenAt(QCursor.pos()).availableGeometry()
        w, h = self.width() + 5, self.height() + 5
        pos.setX(
            min(pos.x() - self.layout().contentsMargins().left(), rect.right() - w))
        pos.setY(max(rect.top(), min(pos.y() - 4, rect.bottom() - h)))
        self.move(pos)

        # show before running animation, or the height calculation will be wrong
        self.show()

        if not ani:
            return

        self.isExpanded = False
        self.ani = QPropertyAnimation(self.view, b'windowOpacity', self)
        self.ani.valueChanged.connect(self._onAniValueChanged)
        self.ani.setStartValue(0)
        self.ani.setEndValue(1)
        self.ani.setDuration(150)
        self.ani.setEasingCurve(QEasingCurve.OutQuad)
        self.ani.start()

    def _onAniValueChanged(self, opacity):
        m = self.layout().contentsMargins()
        w = self.view.width() + m.left() + m.right() + 120
        h = self.view.height() + m.top() + m.bottom() + 12
        if not self.isExpanded:
            y = int(h / 2 * (1 - opacity))
            self.setMask(QRegion(0, y, w, h-y*2))
        else:
            y = int(h / 3 * (1 - opacity))
            self.setMask(QRegion(0, y, w, h-y*2))

    def _fadeOut(self):
        self.isExpanded = True
        self.ani = QPropertyAnimation(self, b'windowOpacity', self)
        self.ani.valueChanged.connect(self._onAniValueChanged)
        self.ani.finished.connect(self.deleteLater)
        self.ani.setStartValue(1)
        self.ani.setEndValue(0)
        self.ani.setDuration(150)
        self.ani.setEasingCurve(QEasingCurve.OutQuad)
        self.ani.start()
