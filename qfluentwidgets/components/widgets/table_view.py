# coding: utf-8
from PyQt6.QtCore import Qt, QMargins, QModelIndex
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtWidgets import (QStyledItemDelegate, QApplication, QStyleOptionViewItem,
                             QTableView, QTableWidget, QWidget)

from ...common.smooth_scroll import SmoothScroll
from ...common.style_sheet import isDarkTheme, FluentStyleSheet, themeColor
from .line_edit import LineEdit


class TableItemDelegate(QStyledItemDelegate):

    def __init__(self, parent: QTableView):
        super().__init__(parent)
        self.margin = 2
        self.hoverRow = -1
        self.pressedRow = -1
        self.currentRow = -1

    def setHoverRow(self, row: int):
        self.hoverRow = row

    def setPressedRow(self, row: int):
        self.pressedRow = row

    def setCurrentRow(self, row: int):
        self.currentRow = row
        if row == self.pressedRow:
            self.pressedRow = -1

    def sizeHint(self, option, index):
        # increase original sizeHint to accommodate space needed for border
        size = super().sizeHint(option, index)
        size = size.grownBy(QMargins(0, self.margin, 0, self.margin))
        return size

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        lineEdit = LineEdit(parent)
        lineEdit.setProperty("transparent", False)
        lineEdit.setStyle(QApplication.style())
        lineEdit.setText(option.text)
        lineEdit.setClearButtonEnabled(True)
        return lineEdit

    def updateEditorGeometry(self, editor: QWidget, option: QStyleOptionViewItem, index: QModelIndex):
        rect = option.rect
        h = super().sizeHint(option, index).height()
        y = rect.y() + self.margin + (h - editor.height()) // 2
        x, w = max(4, rect.x()), rect.width()
        if index.column() == 0:
            w -= 4

        editor.setGeometry(x, y, w, rect.height())

    def _drawBackground(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        """ draw row background """
        r = 5
        if index.column() == 0:
            rect = option.rect.adjusted(4, 0, r + 1, 0)
            painter.drawRoundedRect(rect, r, r)
        elif index.column() == index.model().columnCount(index.parent()) - 1:
            rect = option.rect.adjusted(-r - 1, 0, -4, 0)
            painter.drawRoundedRect(rect, r, r)
        else:
            rect = option.rect.adjusted(-1, 0, 1, 0)
            painter.drawRect(rect)

    def paint(self, painter, option, index):
        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # set clipping rect of painter to avoid painting outside the borders
        painter.setClipping(True)
        painter.setClipRect(option.rect)

        # call original paint method where option.rect is adjusted to account for border
        option.rect.adjust(0, self.margin, 0, -self.margin)

        # draw highlight background
        isHover = self.hoverRow == index.row()
        isPressed = self.pressedRow == index.row()
        isAlternate = index.row() % 2 == 0
        isDark = isDarkTheme()

        c = 255 if isDark else 0
        alpha = 0

        if self.currentRow != index.row():
            if isPressed:
                alpha = 9 if isDark else 6
            elif isHover:
                alpha = 12
            elif isAlternate:
                alpha = 5
        else:
            if isPressed:
                alpha = 15 if isDark else 9
            elif isHover:
                alpha = 25
            else:
                alpha = 17

            # draw indicator
            if index.column() == 0 and self.parent().horizontalScrollBar().value() == 0:
                y, h = option.rect.y() ,option.rect.height()
                ph = round(0.35*h if isPressed else 0.257*h)
                painter.setBrush(themeColor())
                painter.drawRoundedRect(4, ph + y, 3, h - 2*ph, 1.5, 1.5)

        painter.setBrush(QColor(c, c, c, alpha))
        self._drawBackground(painter, option, index)

        painter.restore()
        super().paint(painter, option, index)



class TableBase:
    """ Table base class """

    def __init__(self, *args, **kwargs):
        self.delegate = TableItemDelegate(self)
        self.verticalSmoothScroll = SmoothScroll(self, Qt.Orientation.Vertical)
        self.horizonSmoothScroll = SmoothScroll(self, Qt.Orientation.Horizontal)

        # set style sheet
        FluentStyleSheet.TABLE_VIEW.apply(self)
        FluentStyleSheet.TABLE_VIEW.apply(self.verticalScrollBar())
        FluentStyleSheet.TABLE_VIEW.apply(self.horizontalScrollBar())

        self.setShowGrid(False)
        self.setMouseTracking(True)
        self.setItemDelegate(self.delegate)
        self.setVerticalScrollMode(QTableView.ScrollMode.ScrollPerPixel)
        self.setHorizontalScrollMode(QTableView.ScrollMode.ScrollPerPixel)

        self.entered.connect(lambda i: self.setHoverRow(i.row()))
        self.pressed.connect(lambda i: self.setPressedRow(i.row()))

    def showEvent(self, e):
        QTableView.showEvent(self, e)
        self.resizeRowsToContents()

    def setHoverRow(self, row: int):
        """ set hovered row """
        self.delegate.setHoverRow(row)
        self.viewport().update()

    def setPressedRow(self, row: int):
        """ set pressed row """
        self.delegate.setPressedRow(row)
        self.viewport().update()

    def setCurrentRow(self, row: int):
        self.delegate.setCurrentRow(row)
        self.viewport().update()

    def leaveEvent(self, e):
        QTableView.leaveEvent(self, e)
        self.setHoverRow(-1)

    def resizeEvent(self, e):
        QTableView.resizeEvent(self, e)
        self.viewport().update()

    def wheelEvent(self, e):
        if e.angleDelta().y() != 0:
            self.verticalSmoothScroll.wheelEvent(e)
        else:
            self.horizonSmoothScroll.wheelEvent(e)

        e.setAccepted(True)

    def mouseReleaseEvent(self, e):
        row = self.indexAt(e.pos()).row()
        if row >= 0 and e.button() != Qt.MouseButton.RightButton:
            self.setCurrentRow(row)
        else:
            self.setPressedRow(-1)

        return TableView.mouseReleaseEvent(self, e)


class TableWidget(QTableWidget, TableBase):
    """ Table widget """

    def __init__(self, parent=None):
        super().__init__(parent)


class TableView(QTableView, TableBase):
    """ Table view """

    def __init__(self, parent=None):
        super().__init__(parent)

