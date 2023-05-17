# coding: utf-8
from typing import Type

from PyQt5.QtWidgets import QAction, QWidget
from PyQt5.QtDesigner import QPyDesignerTaskMenuExtension, QExtensionFactory, QDesignerFormWindowInterface, QPyDesignerCustomWidgetPlugin


from qfluentwidgets import MessageBox, LineEdit


class EditTextDialog(MessageBox):

    def __init__(self, widget: QWidget, parent=None):
        super().__init__('Edit text', '', parent)
        self.contentLabel.hide()

        self.lineEdit = LineEdit(self.widget)
        self.propertyName = 'text_' if widget.property('text') is None else 'text'
        self.lineEdit.setText(widget.property(self.propertyName))

        self.lineEdit.selectAll()
        self.lineEdit.setFocus()
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setPlaceholderText('Enter the text of button')

        self.textLayout.addWidget(self.lineEdit)
        self.widget.setFixedSize(
            max(self.contentLabel.width(), self.titleLabel.width()) + 48,
            self.contentLabel.y() + self.lineEdit.height() + 105
        )


class TaskMenuExtensionBase(QPyDesignerTaskMenuExtension):
    """ Task menu extension base class """

    def __init__(self, widget, parent):
        super().__init__(parent)
        self.widget = widget
        self.editTextAction = QAction('Edit text', None)
        self.editTextAction.triggered.connect(self.onEditText)

    def taskActions(self):
        return [self.editTextAction]

    def preferredEditAction(self) -> QAction:
        return self.editTextAction

    def onEditText(self):
        w = EditTextDialog(self.widget, self.widget.window())
        window = QDesignerFormWindowInterface.findFormWindow(self.widget)
        if w.exec():
            window.cursor().setProperty(w.propertyName, w.lineEdit.text())


class EditTextTaskMenuExtension(TaskMenuExtensionBase):
    """ Edit text task menu extension """

    def taskActions(self):
        return [self.editTextAction]



class EditTextIconTaskMenuExtension(TaskMenuExtensionBase):
    """ Edit text and icon task menu extension """

    def taskActions(self):
        return [self.editTextAction, self.editIconAction]

    def preferredEditAction(self):
        return self.editTextAction


class TaskMenuFactoryBase(QExtensionFactory):
    """ Task menu factory base class """

    widgets = []
    Extention = QPyDesignerTaskMenuExtension
    IID = 'org.qt-project.Qt.Designer.TaskMenu'

    def createExtension(self, object, iid, parent):
        if iid != TaskMenuFactoryBase.IID:
            return None

        if object.__class__.__name__ not in self.widgets:
            return None

        return self.Extention(object, parent)

    @classmethod
    def register(cls, Plugin: Type[QPyDesignerCustomWidgetPlugin]):
        if Plugin.__name__ not in cls.widgets:
            cls.widgets.append(Plugin().name())
            Plugin.Factory = cls

        return Plugin


class EditTextTaskMenuFactory(TaskMenuFactoryBase):
    """ Edit text task menu factory """

    Extention = EditTextTaskMenuExtension

