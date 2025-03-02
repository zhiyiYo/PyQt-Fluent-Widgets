# coding:utf-8
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QVBoxLayout, QWidget


class VBoxLayout(QVBoxLayout):
    """ Vertical box layout """

    def __init__(self, parent):
        super().__init__(parent)
        self.widgets = []

    def addWidgets(self, widgets, stretch=0, alignment=Qt.AlignmentFlag.AlignTop):
        """ add widgets to layout """
        for widget in widgets:
            self.addWidget(widget, stretch, alignment)

    def addWidget(self, widget, stretch=0, alignment=Qt.AlignmentFlag.AlignTop):
        """ add widget to layout """
        super().addWidget(widget, stretch, alignment)
        self.widgets.append(widget)
        widget.show()

    def removeWidget(self, widget):
        """ remove widget from layout but not delete it """
        super().removeWidget(widget)
        self.widgets.remove(widget)

    def deleteWidget(self, widget):
        """ remove widget from layout and delete it """
        self.removeWidget(widget)
        widget.hide()
        widget.deleteLater()

    def removeAllWidget(self):
        """ remove all widgets from layout """
        for widget in self.widgets:
            super().removeWidget(widget)

        self.widgets.clear()
