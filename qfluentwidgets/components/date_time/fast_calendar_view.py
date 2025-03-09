# coding: utf-8
from math import ceil
from collections import defaultdict, Counter
from typing import Type

from PySide2.QtCore import Qt, Signal, QSize, QDate, QCalendar, QLocale
from PySide2.QtGui import QPainter, QColor
from PySide2.QtWidgets import QHBoxLayout, QListWidgetItem, QLabel, QWidget, QStackedWidget, QStyle

from ..widgets.flyout import FlyoutViewBase
from ...common.style_sheet import isDarkTheme, themeColor, ThemeColor


from .calendar_view import (ScrollItemDelegate, ScrollViewBase,
                            CalendarViewBase)


class FastScrollItemDelegate(ScrollItemDelegate):
    """ Fast scroll item delegate """

    def __init__(self, min, max):
        super().__init__(min, max)
        self.selectedDate = None
        self.currentDate = QDate.currentDate()

    def setSelectedDate(self, date: QDate):
        self.selectedDate = date

    def setCurrentDate(self, date: QDate):
        self.currentDate = date

    def _drawBackground(self, painter, option, index):
        date = index.data(Qt.UserRole)
        if not date:
            return

        painter.save()

        # outer ring
        if date != self.selectedDate:
            painter.setPen(Qt.PenStyle.NoPen)
        else:
            painter.setPen(themeColor())

        if date == self.currentDate:
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

    def _drawText(self, painter, option, index):
        date = index.data(Qt.UserRole)
        if not date:
            return

        painter.save()
        painter.setFont(self.font)

        if date == self.currentDate:
            c = 0 if isDarkTheme() else 255
            painter.setPen(QColor(c, c, c))
        else:
            painter.setPen(Qt.white if isDarkTheme() else Qt.black)
            if not (self.min <= date <= self.max or option.state & QStyle.State_MouseOver) or \
                    index == self.pressedIndex:
                painter.setOpacity(0.6)

        text = index.data(Qt.DisplayRole)
        painter.drawText(option.rect, Qt.AlignCenter, text)
        painter.restore()


class FastYearScrollItemDelegate(FastScrollItemDelegate):
    """ Year scroll item delegate """

    def _itemMargin(self):
        return 8


class FastDayScrollItemDelegate(FastScrollItemDelegate):
    """ Fast day scroll item delegate """

    def _itemMargin(self):
        return 3



class FastScrollViewBase(ScrollViewBase):
    """ Scroll view base class """

    pageChanged = Signal(int)

    def __init__(self, Delegate: Type[FastScrollItemDelegate], parent=None):
        super().__init__(Delegate, parent)
        self.delegate.setRange(*self.currentPageRange())
        self.delegate.setCurrentDate(self.currentDate)

    def scrollToPage(self, page: int):
        if not 0 <= page < self.pageCount():
            return

        self.currentPage = page
        self._updateItems()
        self.delegate.setRange(*self.currentPageRange())
        self.pageChanged.emit(page)

    def wheelEvent(self, e):
        pass

    def _updateItems(self):
        """ update the items of current page """
        pass

    def pageCount(self):
        return ceil((self.maxYear - self.minYear + 1) / (self.pageRows * self.cols))

    def pageSize(self):
        return self.pageRows * self.cols

    def _setSelectedDate(self, date: QDate):
        self.delegate.setSelectedDate(date)
        self.viewport().update()


class FastYearScrollView(FastScrollViewBase):
    """ Year scroll view """

    def __init__(self, parent=None):
        super().__init__(FastYearScrollItemDelegate, parent)
        self.delegate.setCurrentDate(QDate(self.currentDate.year(), 1, 1))

    def _initItems(self):
        self.years = list(range(self.minYear, self.maxYear+1))
        count = self.cols * self.cols
        years = self.years[:count]
        self.addItems([str(i) for i in years])

        for i, year in enumerate(years):
            item = self.item(i)
            item.setData(Qt.ItemDataRole.UserRole, QDate(year, 1, 1))
            item.setSizeHint(self.sizeHint())

    def scrollToDate(self, date: QDate):
        page = (date.year() - self._startYear()) // 10
        self.scrollToPage(page)

    def currentPageRange(self):
        year = self.currentPage * 10 + self._startYear()
        return QDate(year, 1, 1), QDate(year + 9, 1, 1)

    def _startYear(self):
        if self.minYear % 10 <= 2:
            return self.minYear - self.minYear % 10

        return self.minYear - self.minYear % 10 + 10

    def _updateItems(self):
        start, _ = self.currentPageRange()
        index = (start.year() - self.minYear) % 4
        left = start.year() - index
        right = left + 16

        for i, year in enumerate(range(left, right)):
            item = self.item(i)
            item.setText(str(year))
            item.setData(Qt.ItemDataRole.UserRole, QDate(year, 1, 1))



class FastMonthScrollView(FastScrollViewBase):
    """ Month scroll view """

    def __init__(self, parent=None):
        super().__init__(FastYearScrollItemDelegate, parent)
        self.delegate.setCurrentDate(QDate(self.currentDate.year(), self.currentDate.month(), 1))

    def _initItems(self):
        self.months = [
            self.tr('Jan'), self.tr('Feb'), self.tr('Mar'), self.tr('Apr'),
            self.tr('May'), self.tr('Jun'), self.tr('Jul'), self.tr('Aug'),
            self.tr('Sep'), self.tr('Oct'), self.tr('Nov'), self.tr('Dec'),
            self.tr('Jan'), self.tr('Feb'), self.tr('Mar'), self.tr('Apr'),
        ]
        self.addItems(self.months)

        # add month items
        for i in range(len(self.months)):
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

    def pageCount(self):
        return (self.maxYear - self.minYear + 1) * 12

    def _updateItems(self):
        year = self.minYear + self.currentPage

        for i in range(16):
            m = i % 12 + 1
            y = year + (i > 11)
            self.item(i).setData(Qt.ItemDataRole.UserRole, QDate(y, m, 1))


class FastDayScrollView(FastScrollViewBase):
    """ Day scroll view """

    def __init__(self, parent=None):
        super().__init__(FastDayScrollItemDelegate, parent)
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
            self.weekDayLayout.addWidget(label, 1, Qt.AlignHCenter)

        self.setViewportMargins(0, 38, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.weekDayLayout.setSpacing(0)
        self.weekDayLayout.setContentsMargins(3, 12, 3, 12)
        self.vBoxLayout.addWidget(self.weekDayGroup)

    def gridSize(self) -> QSize:
        return QSize(44, 44)

    def _initItems(self):
        self.cols = 7
        self.pageRows = 6

        startDate = QDate(self.minYear, 1, 1)
        currentDate = startDate

        # add placeholder
        bias = currentDate.dayOfWeek() - 1
        for i in range(bias):
            item = QListWidgetItem(self)
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.addItem(item)

        # add day items
        items, dates = [], []
        endDate = startDate.addDays(self.pageSize() - bias)
        while currentDate < endDate:
            items.append(str(currentDate.day()))
            dates.append(QDate(currentDate))
            currentDate = currentDate.addDays(1)

        self.addItems(items)
        for i in range(bias, self.count()):
            item = self.item(i)
            item.setData(Qt.ItemDataRole.UserRole, dates[i-bias])
            item.setSizeHint(self.gridSize())

        self.delegate.setCurrentIndex(
            self.model().index(self._dateToRow(self.currentDate)))

    def setDate(self, date: QDate):
        self.scrollToDate(date)
        self.delegate.setSelectedDate(date)

    def scrollToDate(self, date: QDate):
        page = (date.year() - self.minYear) * 12 + date.month() - 1
        self.scrollToPage(page)

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

    def _updateItems(self):
        startDate = QDate(self.minYear, 1, 1)
        bias = startDate.dayOfWeek() - 1

        left = startDate.addMonths(self.currentPage)
        left = left.addDays(-left.dayOfWeek() + 1)
        right = left.addDays(self.pageRows * self.cols)

        if self.currentPage == 0:
            for i in range(bias):
                self.item(i).setText("")
                self.item(i).setFlags(Qt.ItemFlag.NoItemFlags)

        currentDate = left
        for i in range(left.daysTo(right)):
            item = self.item(i + bias if self.currentPage == 0 else i)
            if item:
                item.setText(str(currentDate.day()))
                item.setData(Qt.ItemDataRole.UserRole, currentDate)
                currentDate = currentDate.addDays(1)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        item = self.currentItem()
        if item:
            self._setSelectedDate(item.data(Qt.ItemDataRole.UserRole))

    def pageCount(self):
        return (self.maxYear - self.minYear + 1) * 12


class FastYearCalendarView(CalendarViewBase):
    """ Year calendar view """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScrollView(FastYearScrollView(self))
        self.titleButton.setEnabled(False)

    def _updateTitle(self):
        left, right = self.scrollView.currentPageRange()
        self.setTitle(f'{left.year()} - {right.year()}')


class FastMonthCalendarView(CalendarViewBase):
    """ Month calendar view """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScrollView(FastMonthScrollView(self))

    def _updateTitle(self):
        date, _ = self.scrollView.currentPageRange()
        self.setTitle(str(date.year()))

    def currentPageDate(self) -> QDate:
        date, _ = self.scrollView.currentPageRange()
        item = self.scrollView.currentItem()
        month = item.data(Qt.UserRole).month() if item else 1
        return QDate(date.year(), month, 1)


class FastDayCalendarView(CalendarViewBase):
    """ Day calendar view """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setScrollView(FastDayScrollView(self))

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


class FastCalendarView(FlyoutViewBase):

    dateChanged = Signal(QDate)
    resetted = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.date = QDate()
        self._isResetEnabled = False

        self.hBoxLayout = QHBoxLayout(self)
        self.stackedWidget = QStackedWidget(self)
        self.yearView = FastYearCalendarView(self)
        self.monthView = FastMonthCalendarView(self)
        self.dayView = FastDayCalendarView(self)

        self.__initWidget()

    def __initWidget(self):
        self.stackedWidget.addWidget(self.dayView)
        self.stackedWidget.addWidget(self.monthView)
        self.stackedWidget.addWidget(self.yearView)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.stackedWidget)

        self.dayView.setDate(QDate.currentDate())

        self.dayView.titleClicked.connect(self._onDayViewTitleClicked)
        self.monthView.titleClicked.connect(self._onMonthTitleClicked)

        self.monthView.itemClicked.connect(self._onMonthItemClicked)
        self.yearView.itemClicked.connect(self._onYearItemClicked)
        self.dayView.itemClicked.connect(self._onDayItemClicked)

        self.monthView.resetted.connect(self._onResetted)
        self.yearView.resetted.connect(self._onResetted)
        self.dayView.resetted.connect(self._onResetted)

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

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        painter.setBrush(
            QColor(40, 40, 40) if isDarkTheme() else QColor(248, 248, 248))
        painter.setPen(
            QColor(23, 23, 23) if isDarkTheme() else QColor(234, 234, 234))

        rect = self.rect().adjusted(1, 1, -1, -1)
        painter.drawRoundedRect(rect, 8, 8)
