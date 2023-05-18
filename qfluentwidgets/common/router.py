# coding:utf-8
from typing import List
from PyQt5.QtCore import Qt, QObject, pyqtSignal
from PyQt5.QtWidgets import QWidget, QStackedWidget


class RouteItem:
    """ Route item """

    def __init__(self, stackedWidget: QStackedWidget, routeKey: str):
        self.stackedWidget = stackedWidget
        self.routeKey = routeKey

    def __eq__(self, other):
        if other is None:
            return False

        return other.stackedWidget is self.stackedWidget and self.routeKey == other.routeKey


class Router(QObject):
    """ Router """

    emptyChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.history = []   # type: List[RouteItem]
        self.defaultItem = None  # type: RouteItem

    def setDefaultRouteKey(self, stackedWidget: QStackedWidget, routeKey: str):
        self.defaultItem = RouteItem(stackedWidget, routeKey)

    def push(self, stackedWidget: QStackedWidget, routeKey: str):
        """ push history

        Parameters
        ----------
        stackedWidget: QStackedWidget
            stacked widget

        routeKey: str
            route key of sub insterface, it should be the object name of sub interface
        """
        item = RouteItem(stackedWidget, routeKey)

        if not self.history and self.defaultItem != item:
            self.history.append(item)
            self.emptyChanged.emit(False)
        elif self.history and self.history[-1] != item:
            self.history.append(item)

    def pop(self):
        """ pop history """
        if not self.history:
            return

        self.history.pop()
        self._navigate()

    def remove(self, routeKey: str, all=False):
        """ remove history """
        if routeKey not in self.history:
            return

        if all:
            self.history = [i for i in self.history if i.routeKey != routeKey]
        else:
            for i in range(len(self.history)-1, -1, -1):
                if self.history[i].routeKey == routeKey:
                    self.history.pop(i)
                    break

        self._navigate()

    def _navigate(self):
        if self.history:
            self._setCurrentWidget(self.history[-1])
        else:
            if self.defaultItem is not None:
                self._setCurrentWidget(self.defaultItem)

            self.emptyChanged.emit(True)

    def _setCurrentWidget(self, item: RouteItem):
        w = item.stackedWidget.findChild(QWidget, item.routeKey)
        item.stackedWidget.setCurrentWidget(w)


qrouter = Router()