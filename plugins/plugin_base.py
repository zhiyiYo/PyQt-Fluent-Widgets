# coding:utf-8
import re

from PyQt5.QtGui import QIcon
from PyQt5.QtDesigner import QDesignerFormEditorInterface


class PluginBase:

	Factory = None

	def __init__(self, parent=None):
		super().__init__(parent)
		self.initialized = False
		self.factory = None
		self.pattern = re.compile(r'(?<!^)(?=[A-Z])')

	def initialize(self, editor: QDesignerFormEditorInterface):
		if self.initialized:
			return

		self.initialized = True
		if not self.Factory:
			return

		manager = editor.extensionManager()
		self.factory = self.Factory(manager)
		manager.registerExtensions(self.factory, self.factory.IID)

	def isInitialized(self):
		return self.initialized

	def icon(self, name: str):
		return QIcon(f":/qfluentwidgets/images/controls/{name}.png")

	def name(self):
		return "PluginBase"

	def group(self):
		return "PyQt-Fluent-Widgets"

	def toolTip(self):
		name = self.pattern.sub(' ', self.name()).lower()
		return name[0].upper() + name[1:]

	def whatsThis(self):
		return self.toolTip()

	def isContainer(self):
		return False

	def domXml(self):
		return f'<widget class="{self.name()}" name="{self.name()}"></widget>'

	def includeFile(self):
		return "qfluentwidgets"
