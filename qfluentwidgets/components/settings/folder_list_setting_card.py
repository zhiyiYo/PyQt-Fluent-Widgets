# coding:utf-8
from typing import List
from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal, QRectF
from PyQt6.QtGui import QPainter, QIcon
from PyQt6.QtWidgets import (QPushButton, QFileDialog, QWidget, QLabel,
                             QHBoxLayout, QToolButton)
from PyQt6.QtSvg import QSvgRenderer

from ...common.config import ConfigItem, qconfig
from ...common.icon import drawIcon
from ...common.icon import FluentIcon as FIF
from ..dialog_box.dialog import Dialog
from .expand_setting_card import ExpandSettingCard


class ToolButton(QToolButton):
    """ Tool button """

    def __init__(self, icon, size: tuple, iconSize: tuple, parent=None):
        super().__init__(parent=parent)
        self.isPressed = False
        self._icon = icon
        self._iconSize = iconSize
        self.setFixedSize(*size)

    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing |
                               QPainter.RenderHint.SmoothPixmapTransform)
        painter.setOpacity(0.63 if self.isPressed else 1)
        w, h = self._iconSize
        drawIcon(self._icon, painter, QRectF(
            (self.width()-w)//2, (self.height()-h)//2, w, h))


class PushButton(QPushButton):
    """ Push button """

    def __init__(self, icon, text: str, parent=None):
        super().__init__(parent=parent)
        self.isPressed = False
        self._icon = icon
        self.setText(text)

    def mousePressEvent(self, e):
        self.isPressed = True
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        self.isPressed = False
        super().mouseReleaseEvent(e)

    def paintEvent(self, e):
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setOpacity(0.63 if self.isPressed else 1)
        drawIcon(self._icon, painter, QRectF(12, 8, 16, 16))


class FolderItem(QWidget):
    """ Folder item """

    removed = pyqtSignal(QWidget)

    def __init__(self, folder, parent=None):
        super().__init__(parent=parent)
        self.folder = folder
        self.hBoxLayout = QHBoxLayout(self)
        self.folderLabel = QLabel(folder, self)
        self.removeButton = ToolButton(FIF.CLOSE, (39, 29), (12, 12), self)

        self.setFixedHeight(53)
        self.hBoxLayout.setContentsMargins(48, 0, 60, 0)
        self.hBoxLayout.addWidget(self.folderLabel, 0, Qt.AlignmentFlag.AlignLeft)
        self.hBoxLayout.addSpacing(16)
        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.removeButton, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.removeButton.clicked.connect(
            lambda: self.removed.emit(self))


class FolderListSettingCard(ExpandSettingCard):
    """ Folder list setting card """

    folderChanged = pyqtSignal(list)

    def __init__(self, configItem, title, content=None, directory="./", parent=None):
        """
        Parameters
        ----------
        configItem: RangeConfigItem
            configuration item operated by the card

        title: str
            the title of card

        content: str
            the content of card

        directory: str
            working directory of file dialog

        parent: QWidget
            parent widget
        """
        super().__init__(FIF.FOLDER, title, content, parent)
        self.configItem = configItem
        self._dialogDirectory = directory
        self.addFolderButton = PushButton(FIF.FOLDER_ADD, self.tr('Add folder'), self)

        self.folders = qconfig.get(configItem).copy()   # type:List[str]
        self.__initWidget()

    def __initWidget(self):
        self.addWidget(self.addFolderButton)

        # initialize layout
        self.viewLayout.setSpacing(0)
        self.viewLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.viewLayout.setContentsMargins(0, 0, 0, 0)
        for folder in self.folders:
            self.__addFolderItem(folder)

        self.addFolderButton.clicked.connect(self.__showFolderDialog)

    def __showFolderDialog(self):
        """ show folder dialog """
        folder = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), self._dialogDirectory)

        if not folder or folder in self.folders:
            return

        self.__addFolderItem(folder)
        self.folders.append(folder)
        qconfig.set(self.configItem, self.folders)
        self.folderChanged.emit(self.folders)

    def __addFolderItem(self, folder):
        """ add folder item """
        item = FolderItem(folder, self.view)
        item.removed.connect(self.__showConfirmDialog)
        self.viewLayout.addWidget(item)
        self._adjustViewSize()

    def __showConfirmDialog(self, item):
        """ show confirm dialog """
        name = Path(item.folder).name
        title = self.tr('Are you sure you want to delete the folder?')
        content = self.tr("If you delete the ") + f'"{name}"' + \
            self.tr(" folder and remove it from the list, the folder will no "
                    "longer appear in the list, but will not be deleted.")
        w = Dialog(title, content, self.window())
        w.yesSignal.connect(lambda: self.__removeFolder(item))
        w.exec()

    def __removeFolder(self, item):
        """ remove folder """
        if item.folder not in self.folders:
            return

        self.folders.remove(item.folder)
        self.viewLayout.deleteWidget(item)
        self._adjustViewSize()

        self.folderChanged.emit(self.folders)
        qconfig.set(self.configItem, self.folders)
