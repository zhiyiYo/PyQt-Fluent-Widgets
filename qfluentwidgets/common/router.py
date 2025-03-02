# coding:utf-8
from typing import Dict, List
from itertools import groupby

from PyQt6.QtCore import Qt, QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget, QStackedWidget


class RouteItem:
    """ Route item """

    def __init__(self, stacked: QStackedWidget, routeKey: str):
        self.stacked = stacked
        self.routeKey = routeKey

    def __eq__(self, other):
        if other is None:
            return False

        return other.stacked is self.stacked and self.routeKey == other.routeKey


class StackedHistory:
    """ Stacked history """

    def __init__(self, stacked: QStackedWidget):
        self.stacked = stacked
        self.defaultRouteKey = None  # type: str
        self.history = [self.defaultRouteKey]   # type: List[str]

    def __len__(self):
        return len(self.history)

    def isEmpty(self):
        return len(self) <= 1

    def push(self, routeKey: str):
        if self.history[-1] == routeKey:
            return False

        self.history.append(routeKey)
        return True

    def pop(self):
        if self.isEmpty():
            return

        self.history.pop()
        self.goToTop()

    def remove(self, routeKey: str):
        if routeKey not in self.history:
            return

        self.history[1:] = [i for i in self.history[1:] if i != routeKey]
        self.history = [k for k, g in groupby(self.history)]
        self.goToTop()

    def top(self):
        return self.history[-1]

    def setDefaultRouteKey(self, routeKey: str):
        self.defaultRouteKey = routeKey
        self.history[0] = routeKey

    def goToTop(self):
        w = self.stacked.findChild(QWidget, self.top())
        if w:
            self.stacked.setCurrentWidget(w)


class Router(QObject):
    """ Router """

    emptyChanged = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.history = []   # type: List[RouteItem]
        self.stackHistories = {}  # type: Dict[QStackedWidget, StackedHistory]

    def setDefaultRouteKey(self, stacked: QStackedWidget, routeKey: str):
        """ set the default route key of stacked widget """
        if stacked not in self.stackHistories:
            self.stackHistories[stacked] = StackedHistory(stacked)

        self.stackHistories[stacked].setDefaultRouteKey(routeKey)

    def push(self, stacked: QStackedWidget, routeKey: str):
        """ push history

        Parameters
        ----------
        stacked: QStackedWidget
            stacked widget

        routeKey: str
            route key of sub insterface, it should be the object name of sub interface
        """
        item = RouteItem(stacked, routeKey)

        if stacked not in self.stackHistories:
            self.stackHistories[stacked] = StackedHistory(stacked)

        # don't add duplicated history
        success = self.stackHistories[stacked].push(routeKey)
        if success:
            self.history.append(item)

        self.emptyChanged.emit(not bool(self.history))

    def pop(self):
        """ pop history """
        if not self.history:
            return

        item = self.history.pop()
        self.emptyChanged.emit(not bool(self.history))
        self.stackHistories[item.stacked].pop()

    def remove(self, routeKey: str):
        """ remove history """
        self.history = [i for i in self.history if i.routeKey != routeKey]
        self.history = [list(g)[0] for k, g in groupby(self.history, lambda i: i.routeKey)]
        self.emptyChanged.emit(not bool(self.history))

        for stacked, history in self.stackHistories.items():
            w = stacked.findChild(QWidget, routeKey)
            if w:
                return history.remove(routeKey)


qrouter = Router()