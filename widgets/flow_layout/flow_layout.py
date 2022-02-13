# coding:utf-8
from PyQt5.QtCore import QSize, QPoint, Qt, QMargins, QRect
from PyQt5.QtWidgets import QLayout


class FlowLayout(QLayout):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.__items = []
        self.__verticalSpacing = 10
        self.__horizontalSpacing = 10
        self.__margins = QMargins(0, 0, 0, 0)
        super().setContentsMargins(self.__margins)

    def addItem(self, item):
        self.__items.append(item)

    def count(self):
        return len(self.__items)

    def itemAt(self, index: int):
        if 0 <= index < len(self.__items):
            return self.__items[index]

        return None

    def takeAt(self, index: int):
        if 0 <= index < len(self.__items):
            return self.__items.pop(index)

        return None

    def removeAllWidgets(self):
        """ 从布局中移除所有的部件 """
        while self.__items:
            self.takeAt(0)

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width: int):
        """ 根据宽度计算最小高度 """
        return self.__do_layout(QRect(0, 0, width, 0), False)

    def setGeometry(self, rect: QRect):
        super().setGeometry(rect)
        self.__do_layout(rect, True)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self.__items:
            size = size.expandedTo(item.minimumSize())

        m = self.__margins
        size += QSize(m.left()+m.right(), m.top()+m.bottom())

        return size

    def setVerticalSpacing(self, spacing: int):
        """ 设置竖直方向的间距 """
        self.__verticalSpacing = spacing

    def verticalSpacing(self):
        """ 返回竖直方向的间距 """
        return self.__verticalSpacing

    def setHorizontalSpacing(self, spacing: int):
        """ 设置水平方向的间距 """
        self.__horizontalSpacing = spacing

    def horizontalSpacing(self):
        """ 返回水平方向间距 """
        return self.__horizontalSpacing

    def __do_layout(self, rect: QRect, move: bool):
        """ 根据大小调整小部件位置 """
        margin = self.contentsMargins()
        x = rect.x() + margin.left()
        y = rect.y() + margin.top()
        rowHeight = 0
        spaceX = self.horizontalSpacing()
        spaceY = self.verticalSpacing()

        for item in self.__items:
            nextX = x + item.sizeHint().width() + spaceX

            if nextX - spaceX > rect.right() and rowHeight > 0:
                x = rect.x() + margin.left()
                y = y + rowHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                rowHeight = 0

            if move:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            rowHeight = max(rowHeight, item.sizeHint().height())

        return y + rowHeight - rect.y()
