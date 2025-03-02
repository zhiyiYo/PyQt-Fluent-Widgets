# coding:utf-8
from PySide6.QtCore import Qt, QSize, QRectF, QModelIndex
from PySide6.QtGui import QPainter, QColor, QPalette
from PySide6.QtWidgets import QTreeWidget, QStyledItemDelegate, QStyle, QTreeView, QApplication, QStyleOptionViewItem

from ...common.style_sheet import FluentStyleSheet, themeColor, isDarkTheme, setCustomStyleSheet
from ...common.font import getFont
from .check_box import CheckBoxIcon
from .scroll_area import SmoothScrollDelegate


class TreeItemDelegate(QStyledItemDelegate):
    """ Tree item delegate """

    def __init__(self, parent: QTreeView):
        super().__init__(parent)

    def paint(self, painter, option, index):
        painter.setRenderHints(
            QPainter.Antialiasing | QPainter.TextAntialiasing)
        super().paint(painter, option, index)

        if index.data(Qt.CheckStateRole) is not None:
            self._drawCheckBox(painter, option, index)

        if not (option.state & (QStyle.State_Selected | QStyle.State_MouseOver)):
            return

        painter.save()
        painter.setPen(Qt.NoPen)

        # draw background
        h = option.rect.height() - 4
        c = 255 if isDarkTheme() else 0
        painter.setBrush(QColor(c, c, c, 9))
        painter.drawRoundedRect(
            4, option.rect.y() + 2, self.parent().width() - 8, h, 4, 4)

        # draw indicator
        if option.state & QStyle.State_Selected and self.parent().horizontalScrollBar().value() == 0:
            painter.setBrush(themeColor())
            painter.drawRoundedRect(4, 9+option.rect.y(), 3, h - 13, 1.5, 1.5)

        painter.restore()

    def _drawCheckBox(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        painter.save()
        checkState = Qt.CheckState(index.data(Qt.ItemDataRole.CheckStateRole))

        isDark = isDarkTheme()

        r = 4.5
        x = option.rect.x() + 23
        y = option.rect.center().y() - 9
        rect = QRectF(x, y, 19, 19)

        if checkState == Qt.CheckState.Unchecked:
            painter.setBrush(QColor(0, 0, 0, 26)
                             if isDark else QColor(0, 0, 0, 6))
            painter.setPen(QColor(255, 255, 255, 142)
                           if isDark else QColor(0, 0, 0, 122))
            painter.drawRoundedRect(rect, r, r)
        else:
            painter.setPen(themeColor())
            painter.setBrush(themeColor())
            painter.drawRoundedRect(rect, r, r)

            if checkState == Qt.CheckState.Checked:
                CheckBoxIcon.ACCEPT.render(painter, rect)
            else:
                CheckBoxIcon.PARTIAL_ACCEPT.render(painter, rect)

        painter.restore()


    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)

        # font
        option.font = index.data(Qt.FontRole) or getFont(13)

        # text color
        textColor = Qt.white if isDarkTheme() else Qt.black
        textBrush = index.data(Qt.ForegroundRole)
        if textBrush is not None:
            textColor = textBrush.color()

        option.palette.setColor(QPalette.Text, textColor)
        option.palette.setColor(QPalette.HighlightedText, textColor)


class TreeViewBase:
    """ Tree view base class """

    def _initView(self):
        self.scrollDelagate = SmoothScrollDelegate(self)

        self.header().setHighlightSections(False)
        self.header().setDefaultAlignment(Qt.AlignCenter)

        self.setItemDelegate(TreeItemDelegate(self))
        self.setIconSize(QSize(16, 16))

        FluentStyleSheet.TREE_VIEW.apply(self)

    def drawBranches(self, painter, rect, index):
        rect.moveLeft(15)
        return QTreeView.drawBranches(self, painter, rect, index)

    def setBorderVisible(self, isVisible: bool):
        """ set the visibility of border """
        self.setProperty("isBorderVisible", isVisible)
        self.setStyle(QApplication.style())

    def setBorderRadius(self, radius: int):
        """ set the radius of border """
        qss = f"QTreeView{{border-radius: {radius}px}}"
        setCustomStyleSheet(self, qss, qss)


class TreeWidget(TreeViewBase, QTreeWidget):
    """ Tree widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initView()


class TreeView(TreeViewBase, QTreeView):
    """ Tree view """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._initView()
