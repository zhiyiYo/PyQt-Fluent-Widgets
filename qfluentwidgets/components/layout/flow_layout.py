# coding:utf-8
from typing import List

from PySide6.QtCore import QSize, QPoint, Qt, QRect, QPropertyAnimation, QParallelAnimationGroup, QEasingCurve, QEvent, QTimer, QObject
from PySide6.QtWidgets import QLayout, QWidgetItem, QLayoutItem


class FlowLayout(QLayout):
    """ Flow layout """

    def __init__(self, parent=None, needAni=False, isTight=False):
        """
        Parameters
        ----------
        parent:
            parent window or layout

        needAni: bool
            whether to add moving animation

        isTight: bool
            whether to use the tight layout when widgets are hidden
        """
        super().__init__(parent)
        self._items = []    # type: List[QLayoutItem]
        self._anis = []    # type: List[QPropertyAnimation]
        self._aniGroup = QParallelAnimationGroup(self)
        self._verticalSpacing = 10
        self._horizontalSpacing = 10
        self.duration = 300
        self.ease = QEasingCurve.Linear
        self.needAni = needAni
        self.isTight = isTight
        self._deBounceTimer = QTimer(self)
        self._deBounceTimer.setSingleShot(True)
        self._deBounceTimer.timeout.connect(lambda: self._doLayout(self.geometry(), True))
        self._wParent = None
        self._isInstalledEventFilter = False

    def addItem(self, item):
        self._items.append(item)

    def insertItem(self, index, item):
        self._items.insert(index, item)

    def addWidget(self, w):
        super().addWidget(w)
        self._onWidgetAdded(w)

    def insertWidget(self, index, w):
        self.insertItem(index, QWidgetItem(w))
        self.addChildWidget(w)
        self._onWidgetAdded(w, index)

    def _onWidgetAdded(self, w, index=-1):
        if not self._isInstalledEventFilter:
            if w.parent():
                self._wParent = w.parent()
                w.parent().installEventFilter(self)
            else:
                w.installEventFilter(self)

        if not self.needAni:
            return

        ani = QPropertyAnimation(w, b'geometry')
        ani.setEndValue(QRect(QPoint(0, 0), w.size()))
        ani.setDuration(self.duration)
        ani.setEasingCurve(self.ease)
        w.setProperty('flowAni', ani)
        self._aniGroup.addAnimation(ani)

        if index == -1:
            self._anis.append(ani)
        else:
            self._anis.insert(index, ani)

    def setAnimation(self, duration, ease=QEasingCurve.Linear):
        """ set the moving animation

        Parameters
        ----------
        duration: int
            the duration of animation in milliseconds

        ease: QEasingCurve
            the easing curve of animation
        """
        if not self.needAni:
            return

        self.duration = duration
        self.ease = ease

        for ani in self._anis:
            ani.setDuration(duration)
            ani.setEasingCurve(ease)

    def count(self):
        return len(self._items)

    def itemAt(self, index: int):
        if 0 <= index < len(self._items):
            return self._items[index]

        return None

    def takeAt(self, index: int):
        if 0 <= index < len(self._items):
            item = self._items[index]   # type: QLayoutItem
            ani = item.widget().property('flowAni')
            if ani:
                self._anis.remove(ani)
                self._aniGroup.removeAnimation(ani)
                ani.deleteLater()

            return self._items.pop(index).widget()

        return None

    def removeWidget(self, widget):
        for i, item in enumerate(self._items):
            if item.widget() is widget:
                return self.takeAt(i)

    def removeAllWidgets(self):
        """ remove all widgets from layout """
        while self._items:
            self.takeAt(0)

    def takeAllWidgets(self):
        """ remove all widgets from layout and delete them """
        while self._items:
            w = self.takeAt(0)
            if w:
                w.deleteLater()

    def expandingDirections(self):
        return Qt.Orientation(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width: int):
        """ get the minimal height according to width """
        return self._doLayout(QRect(0, 0, width, 0), False)

    def setGeometry(self, rect: QRect):
        super().setGeometry(rect)

        if self.needAni:
            self._deBounceTimer.start(80)
        else:
            self._doLayout(rect, True)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self._items:
            size = size.expandedTo(item.minimumSize())

        m = self.contentsMargins()
        size += QSize(m.left()+m.right(), m.top()+m.bottom())

        return size

    def setVerticalSpacing(self, spacing: int):
        """ set vertical spacing between widgets """
        self._verticalSpacing = spacing

    def verticalSpacing(self):
        """ get vertical spacing between widgets """
        return self._verticalSpacing

    def setHorizontalSpacing(self, spacing: int):
        """ set horizontal spacing between widgets """
        self._horizontalSpacing = spacing

    def horizontalSpacing(self):
        """ get horizontal spacing between widgets """
        return self._horizontalSpacing

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if obj in [w.widget() for w in self._items] and event.type() == QEvent.Type.ParentChange:
            self._wParent = obj.parent()
            obj.parent().installEventFilter(self)
            self._isInstalledEventFilter = True

        if obj == self._wParent and event.type() == QEvent.Type.Show:
            self._doLayout(self.geometry(), True)
            self._isInstalledEventFilter = True

        return super().eventFilter(obj, event)

    def _doLayout(self, rect: QRect, move: bool):
        """ adjust widgets position according to the window size """
        aniRestart = False
        margin = self.contentsMargins()
        x = rect.x() + margin.left()
        y = rect.y() + margin.top()
        rowHeight = 0
        spaceX = self.horizontalSpacing()
        spaceY = self.verticalSpacing()

        for i, item in enumerate(self._items):
            if item.widget() and not item.widget().isVisible() and self.isTight:
                continue

            nextX = x + item.sizeHint().width() + spaceX

            if nextX - spaceX > rect.right() - margin.right() and rowHeight > 0:
                x = rect.x() + margin.left()
                y = y + rowHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                rowHeight = 0

            if move:
                target = QRect(QPoint(x, y), item.sizeHint())
                if not self.needAni:
                    item.setGeometry(target)
                elif target != self._anis[i].endValue():
                    self._anis[i].stop()
                    self._anis[i].setEndValue(target)
                    aniRestart = True

            x = nextX
            rowHeight = max(rowHeight, item.sizeHint().height())

        if self.needAni and aniRestart:
            self._aniGroup.stop()
            self._aniGroup.start()

        return y + rowHeight + margin.bottom() - rect.y()


class AdaptiveFlowLayout(FlowLayout):

    def __init__(self, parent=None, needAni=False, isTight=False):
        """
        Parameters
        ----------
        useMinimumSizeHint: bool
            * If `True`, use the widget's minimumSizeHint to calculate the layout,
            maintaining the relative size of widgets but scaling proportionally to fill rows.
            * If `False`, use a uniform minCardWidth as the base width
        """
        super().__init__(parent, needAni, isTight)
        self._widgetMinimumWidth = 200
        self._widgetMaximumWidth = None

    def setWidgetMinimumWidth(self, width: int):
        self._widgetMinimumWidth = width

    def widgetMinimumWidth(self):
        return self._widgetMinimumWidth

    def setWidgetMaximumWidth(self, width):
        self._widgetMaximumWidth = width

    def widgetMaximumWidth(self):
        return self._widgetMaximumWidth

    def _doLayout(self, rect: QRect, move: bool):
        aniRestart = False
        margin = self.contentsMargins()
        spaceX = self.horizontalSpacing()
        spaceY = self.verticalSpacing()

        # Calculate available width
        availableWidth = rect.width() - margin.left() - margin.right()

        # Calculate the number of cards that fit per row
        if self._widgetMinimumWidth + spaceX > 0:
            cardsPerRow = max(1, (availableWidth + spaceX) // (self._widgetMinimumWidth + spaceX))
        else:
            cardsPerRow = 1

        # Calculate card width to fill each row
        if cardsPerRow > 1:
            cardWidth = (availableWidth - (cardsPerRow - 1) * spaceX) // cardsPerRow
        else:
            cardWidth = availableWidth

        # Apply maximum width limit
        if self._widgetMaximumWidth is not None and cardWidth > self._widgetMaximumWidth:
            cardWidth = self._widgetMaximumWidth

        # Perform layout
        x = rect.x() + margin.left()
        y = rect.y() + margin.top()
        rowHeight = 0
        colIndex = 0

        for i, item in enumerate(self._items):
            if item.widget() and not item.widget().isVisible() and self.isTight:
                continue

            # Calculate next position
            nextX = x + cardWidth + spaceX

            # Need to wrap to new line
            if colIndex >= cardsPerRow and cardsPerRow > 0:
                x = rect.x() + margin.left()
                y = y + rowHeight + spaceY
                nextX = x + cardWidth + spaceX
                rowHeight = 0
                colIndex = 0

            if move:
                # Set widget size to calculated card width, maintaining original height
                targetSize = QSize(cardWidth, item.sizeHint().height())
                target = QRect(QPoint(x, y), targetSize)

                if not self.needAni:
                    item.setGeometry(target)
                elif i < len(self._anis) and target != self._anis[i].endValue():
                    self._anis[i].stop()
                    self._anis[i].setEndValue(target)
                    aniRestart = True

            x = nextX
            rowHeight = max(rowHeight, item.sizeHint().height())
            colIndex += 1

        if self.needAni and aniRestart:
            self._aniGroup.stop()
            self._aniGroup.start()

        return y + rowHeight + margin.bottom() - rect.y()
