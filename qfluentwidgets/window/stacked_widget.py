# coding:utf-8
from PySide6.QtCore import Qt, Signal, QEasingCurve
from PySide6.QtWidgets import QFrame, QHBoxLayout, QAbstractScrollArea

from ..components.widgets.stacked_widget import PopUpAniStackedWidget



class StackedWidget(QFrame):
    """ Stacked widget """

    currentChanged = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.view = PopUpAniStackedWidget(self)

        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.hBoxLayout.addWidget(self.view)

        self.view.currentChanged.connect(self.currentChanged)
        self.setAttribute(Qt.WA_StyledBackground)

    def addWidget(self, widget):
        """ add widget to view """
        self.view.addWidget(widget)

    def widget(self, index: int):
        return self.view.widget(index)

    def setCurrentWidget(self, widget, popOut=True):
        if isinstance(widget, QAbstractScrollArea):
            widget.verticalScrollBar().setValue(0)

        if not popOut:
            self.view.setCurrentWidget(widget, duration=300)
        else:
            self.view.setCurrentWidget(
                widget, True, False, 200, QEasingCurve.InQuad)

    def setCurrentIndex(self, index, popOut=True):
        self.setCurrentWidget(self.view.widget(index), popOut)

    def currentIndex(self):
        return self.view.currentIndex()

    def currentWidget(self):
        return self.view.currentWidget()

    def indexOf(self, widget):
        return self.view.indexOf(widget)

    def count(self):
        return self.view.count()