# coding:utf-8
from PyQt6.QtCore import Qt, QSize, QRectF, QModelIndex, QEvent
from PyQt6.QtGui import QPainter, QColor, QPalette
from PyQt6.QtWidgets import QTreeWidget, QStyledItemDelegate, QStyle, QTreeView, QApplication, QStyleOptionViewItem

from ...common.style_sheet import FluentStyleSheet, themeColor, isDarkTheme, setCustomStyleSheet
from ...common.font import getFont
from ...common.color import autoFallbackThemeColor
from .check_box import CheckBoxIcon
from .scroll_area import SmoothScrollDelegate


class TreeItemDelegate(QStyledItemDelegate):
    """ Tree item delegate """

    def __init__(self, parent: QTreeView):
        super().__init__(parent)
        self.lightCheckedColor = QColor()
        self.darkCheckedColor = QColor()

    def setCheckedColor(self, light, dark):
        """ set the color of indicator in checked status

        Parameters
        ----------
        light, dark: str | QColor | Qt.GlobalColor
            color in light/dark theme mode
        """
        self.lightCheckedColor = QColor(light)
        self.darkCheckedColor = QColor(dark)
        self.parent().viewport().update()

    def paint(self, painter, option, index):
        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        super().paint(painter, option, index)

        if index.data(Qt.ItemDataRole.CheckStateRole) is not None:
            self._drawCheckBox(painter, option, index)

        if not (option.state & (QStyle.StateFlag.State_Selected | QStyle.StateFlag.State_MouseOver)):
            return

        painter.save()
        painter.setPen(Qt.PenStyle.NoPen)

        # draw background
        h = option.rect.height() - 4
        c = 255 if isDarkTheme() else 0
        painter.setBrush(QColor(c, c, c, 9))
        painter.drawRoundedRect(
            4, option.rect.y() + 2, self.parent().width() - 8, h, 4, 4)

        # draw indicator
        if option.state & QStyle.StateFlag.State_Selected and self.parent().horizontalScrollBar().value() == 0:
            painter.setBrush(autoFallbackThemeColor(self.lightCheckedColor, self.darkCheckedColor))
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
            color = autoFallbackThemeColor(self.lightCheckedColor, self.darkCheckedColor)
            painter.setPen(color)
            painter.setBrush(color)
            painter.drawRoundedRect(rect, r, r)

            if checkState == Qt.CheckState.Checked:
                CheckBoxIcon.ACCEPT.render(painter, rect)
            else:
                CheckBoxIcon.PARTIAL_ACCEPT.render(painter, rect)

        painter.restore()


    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)

        # font
        option.font = index.data(Qt.ItemDataRole.FontRole) or getFont(13)

        # text color
        textColor = Qt.GlobalColor.white if isDarkTheme() else Qt.GlobalColor.black
        textBrush = index.data(Qt.ItemDataRole.ForegroundRole)
        if textBrush is not None:
            textColor = textBrush.color()

        option.palette.setColor(QPalette.ColorRole.Text, textColor)
        option.palette.setColor(QPalette.ColorRole.HighlightedText, textColor)


class TreeViewBase:
    """ Tree view base class """

    def __init__(self, *args, **kwargs):
        self.scrollDelagate = SmoothScrollDelegate(self)

        self.header().setHighlightSections(False)
        self.header().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setItemDelegate(TreeItemDelegate(self))
        self.setIconSize(QSize(16, 16))
        self.setMouseTracking(True)

        FluentStyleSheet.TREE_VIEW.apply(self)

    def setCheckedColor(self, light, dark):
        """ set the color in checked status

        Parameters
        ----------
        light, dark: str | QColor | Qt.GlobalColor
            color in light/dark theme mode
        """
        self.itemDelegate().setCheckedColor(light, dark)

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


class TreeWidget(QTreeWidget, TreeViewBase):
    """ Tree widget """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def viewportEvent(self, event):
        """
        Catch the click event to override the item "expand/collapse" function which is
        still called in the place it was before moving the branches in the drawBranches method.
        """
        if event.type() != QEvent.Type.MouseButtonPress:
            return super().viewportEvent(event)

        index = self.indexAt(event.pos())
        item = self.itemFromIndex(index)

        if item is None:
            return super().viewportEvent(event)

        level = 0
        while item.parent() is not None:
            item = item.parent()
            level += 1

        indent = level * self.indentation() + 20
        if event.pos().x() > indent and event.pos().x() < indent + 10:
            if self.isExpanded(index):
                self.collapse(index)
            else:
                self.expand(index)

        return super().viewportEvent(event)


class TreeView(QTreeView, TreeViewBase):
    """ Tree view """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def viewportEvent(self, event):
        """
        Catch the click event to override the item "expand/collapse" function which is
        still called in the place it was before moving the branches in the drawBranches method.
        """
        if event.type() != QEvent.Type.MouseButtonPress:
            return super().viewportEvent(event)

        index = self.indexAt(event.pos())
        if not index.isValid():
            return super().viewportEvent(event)

        level = 0
        currentIndex = index
        while currentIndex.parent().isValid():
            currentIndex = currentIndex.parent()
            level += 1

        indent = level * self.indentation() + 20
        if event.pos().x() > indent and event.pos().x() < indent + 10:
            if self.isExpanded(index):
                self.collapse(index)
            else:
                self.expand(index)

        return super().viewportEvent(event)
