# coding: utf-8
from math import ceil
from collections import defaultdict, Counter
from typing import Tuple, Type

from PyQt6.QtCore import (Qt, QRectF, pyqtSignal, QSize, QModelIndex, QDate, QCalendar, QEasingCurve, QPropertyAnimation,
                          QParallelAnimationGroup, QPoint, QRect, QStringListModel)
from PyQt6.QtGui import QPainter, QColor, QCursor
from PyQt6.QtWidgets import (QApplication, QFrame, QPushButton, QHBoxLayout, QVBoxLayout, QListWidget,
                             QListWidgetItem, QStyledItemDelegate, QStyle, QStyleOptionViewItem,
                             QLabel, QWidget, QStackedWidget, QGraphicsDropShadowEffect, QListView)

from ...common.icon import FluentIcon as FIF
from ...common.style_sheet import isDarkTheme, FluentStyleSheet, themeColor, ThemeColor
from ...common.font import getFont
from ...common.screen import getCurrentScreenGeometry
from ..widgets.button import TransparentToolButton
from ..widgets.scroll_bar import SmoothScrollBar


class ScrollButton(TransparentToolButton):
    """ Scroll button """

    def _drawIcon(self, icon, painter: QPainter, rect: QRectF):
        pass

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        if not self.isPressed:
            w, h = 10, 10
        else:
            w, h = 9, 9

        x = (self.width() - w) / 2
        y = (self.height() - h) / 2

        if not isDarkTheme():
            self._icon.render(painter, QRectF(x, y, w, h), fill="#5e5e5e")
        else:
            self._icon.render(painter, QRectF(x, y, w, h), fill="#9c9c9c")


class ScrollItemDelegate(QStyledItemDelegate):

    def __init__(self, min, max):
        super().__init__()
        self.setRange(min, max)
        self.font = getFont()
        self.pressedIndex = QModelIndex()
        self.currentIndex = QModelIndex()
        self.selectedIndex = QModelIndex()

    def setRange(self, min, max):
        self.min = min
        self.max = max

    def setPressedIndex(self, index: QModelIndex):
        self.pressedIndex = index

    def setCurrentIndex(self, index: QModelIndex):
        self.currentIndex = index

    def setSelectedIndex(self, index: QModelIndex):
        self.selectedIndex = index

    def paint(self, painter, option, index):
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)
        self._drawBackground(painter, option, index)
        self._drawText(painter, option, index)

    def _drawBackground(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        painter.save()

        # outer ring
        if index != self.selectedIndex:
            painter.setPen(Qt.PenStyle.NoPen)
        else:
            painter.setPen(themeColor())

        if index == self.currentIndex:
            if index == self.pressedIndex:
                painter.setBrush(ThemeColor.LIGHT_2.color())
            elif option.state & QStyle.StateFlag.State_MouseOver:
                painter.setBrush(ThemeColor.LIGHT_1.color())
            else:
                painter.setBrush(themeColor())
        else:
            c = 255 if isDarkTheme() else 0
            if index == self.pressedIndex:
                painter.setBrush(QColor(c, c, c, 7))
            elif option.state & QStyle.StateFlag.State_MouseOver:
                painter.setBrush(QColor(c, c, c, 9))
            else:
                painter.setBrush(Qt.GlobalColor.transparent)

        m = self._itemMargin()
        painter.drawEllipse(option.rect.adjusted(m, m, -m, -m))
        painter.restore()

    def _drawText(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex):
        painter.save()
        painter.setFont(self.font)

        if index == self.currentIndex:
            c = 0 if isDarkTheme() else 255
            painter.setPen(QColor(c, c, c))
        else:
            painter.setPen(Qt.GlobalColor.white if isDarkTheme() else Qt.GlobalColor.black)
            if not (self.min <= index.data(Qt.ItemDataRole.UserRole) <= self.max or option.state & QStyle.StateFlag.State_MouseOver) or \
                    index == self.pressedIndex:
                painter.setOpacity(0.6)

        text = index.data(Qt.ItemDataRole.DisplayRole)
        painter.drawText(option.rect, Qt.AlignmentFlag.AlignCenter, text)
        painter.restore()

    def _itemMargin(self):
        return 0


class YearScrollItemDelegate(ScrollItemDelegate):
    """ Year scroll item delegate """

    def _itemMargin(self):
        return 8


class DayScrollItemDelegate(ScrollItemDelegate):
    """ Day scroll item delegate """

    def _itemMargin(self):
        return 3


class ScrollViewBase(QListWidget):
    """ Scroll view base class """

    pageChanged = pyqtSignal(int)

    def __init__(self, Delegate: Type[ScrollItemDelegate], parent=None):
        super().__init__(parent)
        self.cols = 4
        self.pageRows = 3
        self.currentPage = 0
        self.vScrollBar = SmoothScrollBar(Qt.Orientation.Vertical, self)

        self.delegate = Delegate(0, 0)
        self.currentDate = QDate.currentDate()
        self.date = QDate.currentDate()

        self.minYear = self.currentDate.year() - 100
        self.maxYear = self.currentDate.year() + 100

        self.setUniformItemSizes(True)
        self._initItems()
        self.__initWidget()

    def __initWidget(self):
        self.setSpacing(0)
        self.setMovement(QListWidget.Movement.Static)
        self.setGridSize(self.gridSize())
        self.setViewportMargins(0, 0, 0, 0)
        self.setItemDelegate(self.delegate)
        self.setViewMode(QListWidget.ViewMode.IconMode)
        self.setResizeMode(QListWidget.ResizeMode.Adjust)

        self.vScrollBar.ani.finished.connect(self._onFirstScrollFinished)
        self.vScrollBar.setScrollAnimation(1)
        self.setDate(self.date)

        self.vScrollBar.setForceHidden(True)
        self.setVerticalScrollMode(self.ScrollMode.ScrollPerPixel)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

    def _onFirstScrollFinished(self):
        self.vScrollBar.setScrollAnimation(300, QEasingCurve.Type.OutQuad)
        self.vScrollBar.ani.disconnect()

    def _onFirstScrollFinished(self):
        self.vScrollBar.setScrollAnimation(300, QEasingCurve.Type.OutQuad)
        self.vScrollBar.ani.disconnect()

    def scrollUp(self):
        self.scrollToPage(self.currentPage - 1)

    def scrollDown(self):
        self.scrollToPage(self.currentPage + 1)

    def scrollToPage(self, page: int):
        if not 0 <= page <= ceil(self.model().rowCount() / (self.pageRows * self.cols)):
            return

        self.currentPage = page
        y = self.gridSize().height() * self.pageRows * page
        self.vScrollBar.setValue(y)
        self.delegate.setRange(*self.currentPageRange())
        self.pageChanged.emit(page)

    def currentPageRange(self):
        return 0, 0

    def setDate(self, date: QDate):
        self.scrollToDate(date)

    def scrollToDate(self, date: QDate):
        pass

    def _setPressedIndex(self, index):
        self.delegate.setPressedIndex(index)
        self.viewport().update()

    def _setSelectedIndex(self, index):
        self.delegate.setSelectedIndex(index)
        self.viewport().update()

    def wheelEvent(self, e):
        if self.vScrollBar.ani.state() == QPropertyAnimation.State.Running:
            return

        if e.angleDelta().y() < 0:
            self.scrollDown()
        else:
            self.scrollUp()

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == Qt.MouseButton.LeftButton and self.indexAt(e.pos()).row() >= 0:
            self._setPressedIndex(self.currentIndex())

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self._setPressedIndex(QModelIndex())

    def gridSize(self) -> QSize:
        return QSize(76, 76)


class CalendarViewBase(QFrame):
    """ Calendar view base class """

    resetted = pyqtSignal()
    titleClicked = pyqtSignal()
    itemClicked = pyqtSignal(QDate)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.titleButton = QPushButton(self)
        self.resetButton = ScrollButton(FIF.CANCEL, self)
        self.upButton = ScrollButton(FIF.CARE_UP_SOLID, self)
        self.downButton = ScrollButton(FIF.CARE_DOWN_SOLID, self)

        self.scrollView = None  # type: ScrollViewBase

        self.hBoxLayout = QHBoxLayout()
        self.vBoxLayout = QVBoxLayout(self)

        self.__initWidget()

    def __initWidget(self):
        self.setFixedSize(314, 355)
        self.upButton.setFixedSize(32, 34)
        self.downButton.setFixedSize(32, 34)
        self.resetButton.setFixedSize(32, 34)
        self.titleButton.setFixedHeight(34)

        self.hBoxLayout.setContentsMargins(9, 8, 9, 8)
        self.hBoxLayout.setSpacing(7)
        self.hBoxLayout.addWidget(self.titleButton, 1, Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addWidget(self.resetButton, 0, Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addWidget(self.upButton, 0, Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addWidget(self.downButton, 0, Qt.AlignmentFlag.AlignVCenter)
        self.setResetEnabled(False)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addLayout(self.hBoxLayout)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.titleButton.setObjectName('titleButton')
        FluentStyleSheet.CALENDAR_PICKER.apply(self)

        self.titleButton.clicked.connect(self.titleClicked)
        self.resetButton.clicked.connect(self.resetted)
        self.upButton.clicked.connect(self._onScrollUp)
        self.downButton.clicked.connect(self._onScrollDown)

    def setScrollView(self, view: ScrollViewBase):
        self.scrollView = view
        self.scrollView.itemClicked.connect(lambda i: self.itemClicked.emit(i.data(Qt.ItemDataRole.UserRole)))
        self.vBoxLayout.addWidget(view)
        view.pageChanged.connect(self._updateTitle)
        self._updateTitle()

    def setResetEnabled(self, isEnabled: bool):
        self.resetButton.setVisible(isEnabled)

    def isResetEnabled(self):
        return self.resetButton.isVisible()

    def setDate(self, date: QDate):
        self.scrollView.setDate(date)
        self._updateTitle()

    def setTitle(self, title: str):
        self.titleButton.setText(title)

    def currentPageDate(self) -> QDate:
        raise NotImplementedError

    def _onScrollUp(self):
        self.scrollView.scrollUp()
        self._updateTitle()

    def _onScrollDown(self):
        self.scrollView.scrollDown()
        self._updateTitle()

    def _updateTitle(self):
        pass


class YearScrollView(ScrollViewBase):
    """ Year scroll view """

    def __init__(self, parent=None):
        super().__init__(YearScrollItemDelegate, parent)

    def _initItems(self):
        years = range(self.minYear, self.maxYear+1)
        self.addItems([str(i) for i in years])

        for i, year in enumerate(years):
            item = self.item(i)
            item.setData(Qt.ItemDataRole.UserRole, QDate(year, 1, 1))
            item.setSizeHint(self.sizeHint())
            if year == self.currentDate.year():
                self.delegate.setCurrentIndex(self.indexFromItem(item))

    def scrollToDate(self, date: QDate):
        page = (date.year() - self.minYear) // 12
        self.scrollToPage(page)

    def currentPageRange(self):
        pageSize = self.pageRows * self.cols
        left = self.currentPage * pageSize + self.minYear

        years = defaultdict(int)
        for i in range(left, left + 16):
            y = i // 10 * 10
            years[y] += 1

        year = Counter(years).most_common()[0][0]
        return QDate(year, 1, 1), QDate(year + 10, 1, 1)


class YearCalendarView(CalendarViewBase):
    """ Year calendar view """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScrollView(YearScrollView(self))
        self.titleButton.setEnabled(False)

    def _updateTitle(self):
        left, right = self.scrollView.currentPageRange()
        self.setTitle(f'{left.year()} - {right.year()}')


class MonthScrollView(ScrollViewBase):
    """ Month scroll view """

    def __init__(self, parent=None):
        super().__init__(YearScrollItemDelegate, parent)

    def _initItems(self):
        self.months = [
            self.tr('Jan'), self.tr('Feb'), self.tr('Mar'), self.tr('Apr'),
            self.tr('May'), self.tr('Jun'), self.tr('Jul'), self.tr('Aug'),
            self.tr('Sep'), self.tr('Oct'), self.tr('Nov'), self.tr('Dec'),
        ]
        self.addItems(self.months * 201)

        # add month items
        for i in range(12 * 201):
            year = i // 12 + self.minYear
            m = i % 12 + 1
            item = self.item(i)
            item.setData(Qt.ItemDataRole.UserRole, QDate(year, m, 1))
            item.setSizeHint(self.gridSize())

            if year == self.currentDate.year() and m == self.currentDate.month():
                self.delegate.setCurrentIndex(self.indexFromItem(item))

    def scrollToDate(self, date: QDate):
        page = date.year() - self.minYear
        self.scrollToPage(page)

    def currentPageRange(self):
        year = self.minYear + self.currentPage
        return QDate(year, 1, 1), QDate(year, 12, 31)


class MonthCalendarView(CalendarViewBase):
    """ Month calendar view """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScrollView(MonthScrollView(self))

    def _updateTitle(self):
        date, _ = self.scrollView.currentPageRange()
        self.setTitle(str(date.year()))

    def currentPageDate(self) -> QDate:
        date, _ = self.scrollView.currentPageRange()
        item = self.scrollView.currentItem()
        month = item.data(Qt.ItemDataRole.UserRole).month() if item else 1
        return QDate(date.year(), month, 1)


class DayScrollView(ScrollViewBase):
    """ Day scroll view """

    def __init__(self, parent=None):
        super().__init__(DayScrollItemDelegate, parent)
        self.cols = 7
        self.pageRows = 4
        self.vBoxLayout = QHBoxLayout(self)

        # add week day labels
        self.weekDays = [
            self.tr('Mo'), self.tr('Tu'), self.tr('We'),
            self.tr('Th'), self.tr('Fr'), self.tr('Sa'), self.tr('Su')
        ]
        self.weekDayGroup = QWidget(self)
        self.weekDayLayout = QHBoxLayout(self.weekDayGroup)
        self.weekDayGroup.setObjectName('weekDayGroup')
        for day in self.weekDays:
            label = QLabel(day)
            label.setObjectName('weekDayLabel')
            self.weekDayLayout.addWidget(label, 1, Qt.AlignmentFlag.AlignHCenter)

        self.setViewportMargins(0, 38, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.weekDayLayout.setSpacing(0)
        self.weekDayLayout.setContentsMargins(3, 12, 3, 12)
        self.vBoxLayout.addWidget(self.weekDayGroup)

    def gridSize(self) -> QSize:
        return QSize(44, 44)

    def _initItems(self):
        startDate = QDate(self.minYear, 1, 1)
        endDate = QDate(self.maxYear, 12, 31)
        currentDate = startDate

        # add placeholder
        bias = currentDate.dayOfWeek() - 1
        for i in range(bias):
            item = QListWidgetItem(self)
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.addItem(item)

        # add day items
        items, dates = [], []
        while currentDate <= endDate:
            items.append(str(currentDate.day()))
            dates.append(QDate(currentDate))
            currentDate = currentDate.addDays(1)

        self.addItems(items)
        for i in range(bias, self.count()):
            item = self.item(i)
            item.setData(Qt.ItemDataRole.UserRole, dates[i-bias])
            item.setSizeHint(self.gridSize())

        self.delegate.setCurrentIndex(self.model().index(self._dateToRow(self.currentDate)))

    def setDate(self, date: QDate):
        self.scrollToDate(date)
        self.setCurrentIndex(self.model().index(self._dateToRow(date)))
        self.delegate.setSelectedIndex(self.currentIndex())

    def scrollToDate(self, date: QDate):
        page = (date.year() - self.minYear) * 12 + date.month() - 1
        self.scrollToPage(page)

    def scrollToPage(self, page: int):
        if not 0 <= page <= 201 * 12 - 1:
            return

        self.currentPage = page

        index = self._dateToRow(self._pageToDate())
        y = index // self.cols * self.gridSize().height()
        self.vScrollBar.scrollTo(y)

        self.delegate.setRange(*self.currentPageRange())
        self.pageChanged.emit(page)

    def currentPageRange(self):
        date = self._pageToDate()
        return date, date.addMonths(1).addDays(-1)

    def _pageToDate(self):
        year = self.currentPage // 12 + self.minYear
        month = self.currentPage % 12 + 1
        return QDate(year, month, 1)

    def _dateToRow(self, date: QDate):
        startDate = QDate(self.minYear, 1, 1)
        days = startDate.daysTo(date)
        return days + startDate.dayOfWeek() - 1

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self._setSelectedIndex(self.currentIndex())


class DayCalendarView(CalendarViewBase):
    """ Day calendar view """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScrollView(DayScrollView(self))

    def _updateTitle(self):
        date = self.currentPageDate()
        name = QCalendar().monthName(self.locale(), date.month(), date.year())
        self.setTitle(f'{name} {date.year()}')

    def currentPageDate(self) -> QDate:
        date, _ = self.scrollView.currentPageRange()
        return date

    def scrollToDate(self, date: QDate):
        self.scrollView.scrollToDate(date)
        self._updateTitle()


class CalendarView(QWidget):
    """ Calendar view """

    resetted = pyqtSignal()
    dateChanged = pyqtSignal(QDate)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.date = QDate()
        self._isResetEnabled = False

        self.stackedWidget = QStackedWidget(self)
        self.yearView = YearCalendarView(self)
        self.monthView = MonthCalendarView(self)
        self.dayView = DayCalendarView(self)

        self.opacityAni = QPropertyAnimation(self, b'windowOpacity', self)
        self.slideAni = QPropertyAnimation(self, b'geometry', self)
        self.aniGroup = QParallelAnimationGroup(self)

        self.__initWidget()

    def __initWidget(self):
        self.setWindowFlags(Qt.WindowType.Popup | Qt.WindowType.FramelessWindowHint |
                            Qt.WindowType.NoDropShadowWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, True)

        self.stackedWidget.addWidget(self.dayView)
        self.stackedWidget.addWidget(self.monthView)
        self.stackedWidget.addWidget(self.yearView)

        self.hBoxLayout.setContentsMargins(12, 8, 12, 20)
        self.hBoxLayout.addWidget(self.stackedWidget)
        self.setShadowEffect()

        self.dayView.setDate(QDate.currentDate())

        self.aniGroup.addAnimation(self.opacityAni)
        self.aniGroup.addAnimation(self.slideAni)

        self.dayView.titleClicked.connect(self._onDayViewTitleClicked)
        self.monthView.titleClicked.connect(self._onMonthTitleClicked)

        self.monthView.itemClicked.connect(self._onMonthItemClicked)
        self.yearView.itemClicked.connect(self._onYearItemClicked)
        self.dayView.itemClicked.connect(self._onDayItemClicked)

        self.monthView.resetted.connect(self._onResetted)
        self.yearView.resetted.connect(self._onResetted)
        self.dayView.resetted.connect(self._onResetted)

    def setShadowEffect(self, blurRadius=30, offset=(0, 8), color=QColor(0, 0, 0, 30)):
        """ add shadow to dialog """
        self.shadowEffect = QGraphicsDropShadowEffect(self.stackedWidget)
        self.shadowEffect.setBlurRadius(blurRadius)
        self.shadowEffect.setOffset(*offset)
        self.shadowEffect.setColor(color)
        self.stackedWidget.setGraphicsEffect(None)
        self.stackedWidget.setGraphicsEffect(self.shadowEffect)

    def isRestEnabled(self):
        return self._isResetEnabled

    def setResetEnabled(self, isEnabled: bool):
        """ set the visibility of reset button """
        self._isResetEnabled = isEnabled
        self.yearView.setResetEnabled(isEnabled)
        self.monthView.setResetEnabled(isEnabled)
        self.dayView.setResetEnabled(isEnabled)

    def _onResetted(self):
        self.resetted.emit()
        self.close()

    def _onDayViewTitleClicked(self):
        self.stackedWidget.setCurrentWidget(self.monthView)
        self.monthView.setDate(self.dayView.currentPageDate())

    def _onMonthTitleClicked(self):
        self.stackedWidget.setCurrentWidget(self.yearView)
        self.yearView.setDate(self.monthView.currentPageDate())

    def _onMonthItemClicked(self, date: QDate):
        self.stackedWidget.setCurrentWidget(self.dayView)
        self.dayView.scrollToDate(date)

    def _onYearItemClicked(self, date: QDate):
        self.stackedWidget.setCurrentWidget(self.monthView)
        self.monthView.setDate(date)

    def _onDayItemClicked(self, date: QDate):
        self.close()
        if date != self.date:
            self.date = date
            self.dateChanged.emit(date)

    def setDate(self, date: QDate):
        """ set the selected date """
        self.dayView.setDate(date)
        self.date = date

    def exec(self, pos: QPoint, ani=True):
        """ show calendar view """
        if self.isVisible():
            return

        rect = getCurrentScreenGeometry()
        w, h = self.sizeHint().width() + 5, self.sizeHint().height()
        pos.setX(max(rect.left(), min(pos.x(), rect.right() - w)))
        pos.setY(max(rect.top(), min(pos.y() - 4, rect.bottom() - h + 5)))
        self.move(pos)

        if not ani:
            return self.show()

        self.opacityAni.setStartValue(0)
        self.opacityAni.setEndValue(1)
        self.opacityAni.setDuration(150)
        self.opacityAni.setEasingCurve(QEasingCurve.Type.OutQuad)

        self.slideAni.setStartValue(QRect(pos-QPoint(0, 8), self.sizeHint()))
        self.slideAni.setEndValue(QRect(pos, self.sizeHint()))
        self.slideAni.setDuration(150)
        self.slideAni.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.aniGroup.start()

        self.show()
