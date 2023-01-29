# coding:utf-8
from typing import List
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QWidget


class VBoxLayout(QVBoxLayout):
    """ Vertical box layout """

    def __init__(self, parent):
        super().__init__(parent)
        self.widgets = []

    def addWidgets(self, widgets: List[QWidget], stretch=0, alignment=Qt.AlignTop):
        """ add widgets to layout """
        for widget in widgets:
            self.addWidget(widget, stretch, alignment)

    def addWidget(self, widget: QWidget, stretch=0, alignment=Qt.AlignTop):
        """ add widget to layout """
        super().addWidget(widget, stretch, alignment)
        self.widgets.append(widget)
        widget.show()

    def removeWidget(self, widget: QWidget):
        """ remove widget from layout but not delete it """
        super().removeWidget(widget)
        self.widgets.remove(widget)

    def deleteWidget(self, widget: QWidget):
        """ remove widget from layout and delete it """
        self.removeWidget(widget)
        widget.hide()
        widget.deleteLater()

    def removeAllWidget(self):
        """ remove all widgets from layout """
        for widget in self.widgets:
            super().removeWidget(widget)

        self.widgets.clear()
