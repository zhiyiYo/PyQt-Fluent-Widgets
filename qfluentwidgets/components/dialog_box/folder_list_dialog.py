# coding:utf-8
import os

from PySide2.QtCore import Qt, Signal
from PySide2.QtGui import (QBrush, QColor, QFont, QFontMetrics, QMouseEvent,
                         QPainter, QPen, QPixmap)
from PySide2.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
                             QVBoxLayout, QWidget, QPushButton)

from ...common.config import isDarkTheme
from ...common.icon import getIconColor
from ...common.style_sheet import FluentStyleSheet
from .dialog import Dialog
from .mask_dialog_base import MaskDialogBase
from ..widgets.scroll_area import SingleDirectionScrollArea


class FolderListDialog(MaskDialogBase):
    """ Folder list dialog box """

    folderChanged = Signal(list)

    def __init__(self, folderPaths: list, title: str, content: str, parent):
        super().__init__(parent=parent)
        self.title = title
        self.content = content
        self.__originalPaths = folderPaths
        self.folderPaths = folderPaths.copy()

        self.vBoxLayout = QVBoxLayout(self.widget)
        self.titleLabel = QLabel(title, self.widget)
        self.contentLabel = QLabel(content, self.widget)
        self.scrollArea = SingleDirectionScrollArea(self.widget)
        self.scrollWidget = QWidget(self.scrollArea)
        self.completeButton = QPushButton(self.tr('Done'), self.widget)
        self.addFolderCard = AddFolderCard(self.scrollWidget)
        self.folderCards = [FolderCard(i, self.scrollWidget)
                            for i in folderPaths]
        self.__initWidget()

    def __initWidget(self):
        """ initialize widgets """
        self.__setQss()

        w = max(self.titleLabel.width()+48, self.contentLabel.width()+48, 352)
        self.widget.setFixedWidth(w)
        self.scrollArea.resize(294, 72)
        self.scrollWidget.resize(292, 72)
        self.scrollArea.setFixedWidth(294)
        self.scrollWidget.setFixedWidth(292)
        self.scrollArea.setMaximumHeight(400)
        self.scrollArea.setViewportMargins(0, 0, 0, 0)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollWidget)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.hScrollBar.setForceHidden(True)
        self.__initLayout()

        # connect signal to slot
        self.addFolderCard.clicked.connect(self.__showFileDialog)
        self.completeButton.clicked.connect(self.__onButtonClicked)
        for card in self.folderCards:
            card.clicked.connect(self.__showDeleteFolderCardDialog)

    def __initLayout(self):
        """ initialize layout """
        self.vBoxLayout.setContentsMargins(24, 24, 24, 24)
        self.vBoxLayout.setSizeConstraint(QVBoxLayout.SetFixedSize)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setSpacing(0)

        # labels
        layout_1 = QVBoxLayout()
        layout_1.setContentsMargins(0, 0, 0, 0)
        layout_1.setSpacing(6)
        layout_1.addWidget(self.titleLabel, 0, Qt.AlignTop)
        layout_1.addWidget(self.contentLabel, 0, Qt.AlignTop)
        self.vBoxLayout.addLayout(layout_1, 0)
        self.vBoxLayout.addSpacing(12)

        # cards
        layout_2 = QHBoxLayout()
        layout_2.setAlignment(Qt.AlignCenter)
        layout_2.setContentsMargins(4, 0, 4, 0)
        layout_2.addWidget(self.scrollArea, 0, Qt.AlignCenter)
        self.vBoxLayout.addLayout(layout_2, 1)
        self.vBoxLayout.addSpacing(24)

        self.scrollLayout = QVBoxLayout(self.scrollWidget)
        self.scrollLayout.setAlignment(Qt.AlignTop)
        self.scrollLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollLayout.setSpacing(8)
        self.scrollLayout.addWidget(self.addFolderCard, 0, Qt.AlignTop)
        for card in self.folderCards:
            self.scrollLayout.addWidget(card, 0, Qt.AlignTop)

        # buttons
        layout_3 = QHBoxLayout()
        layout_3.setContentsMargins(0, 0, 0, 0)
        layout_3.addStretch(1)
        layout_3.addWidget(self.completeButton)
        self.vBoxLayout.addLayout(layout_3, 0)

        self.__adjustWidgetSize()

    def __showFileDialog(self):
        """ show file dialog to select folder """
        path = QFileDialog.getExistingDirectory(
            self, self.tr("Choose folder"), "./")

        if not path or path in self.folderPaths:
            return

        # create folder card
        card = FolderCard(path, self.scrollWidget)
        self.scrollLayout.addWidget(card, 0, Qt.AlignTop)
        card.clicked.connect(self.__showDeleteFolderCardDialog)
        card.show()

        self.folderPaths.append(path)
        self.folderCards.append(card)

        self.__adjustWidgetSize()

    def __showDeleteFolderCardDialog(self):
        """ show delete folder card dialog """
        sender = self.sender()
        title = self.tr('Are you sure you want to delete the folder?')
        content = self.tr("If you delete the ") + f'"{sender.folderName}"' + \
            self.tr(" folder and remove it from the list, the folder will no "
                    "longer appear in the list, but will not be deleted.")
        dialog = Dialog(title, content, self.window())
        dialog.yesSignal.connect(lambda: self.__deleteFolderCard(sender))
        dialog.exec_()

    def __deleteFolderCard(self, folderCard):
        """ delete selected folder card """
        self.scrollLayout.removeWidget(folderCard)
        index = self.folderCards.index(folderCard)
        self.folderCards.pop(index)
        self.folderPaths.pop(index)
        folderCard.deleteLater()

        # adjust height
        self.__adjustWidgetSize()

    def __setQss(self):
        """ set style sheet """
        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        self.completeButton.setObjectName('completeButton')
        self.scrollWidget.setObjectName('scrollWidget')

        FluentStyleSheet.FOLDER_LIST_DIALOG.apply(self)
        self.setStyle(QApplication.style())

        self.titleLabel.adjustSize()
        self.contentLabel.adjustSize()
        self.completeButton.adjustSize()

    def __onButtonClicked(self):
        """ done button clicked slot """
        if sorted(self.__originalPaths) != sorted(self.folderPaths):
            self.setEnabled(False)
            QApplication.processEvents()
            self.folderChanged.emit(self.folderPaths)

        self.close()

    def __adjustWidgetSize(self):
        N = len(self.folderCards)
        h = 72*(N+1) + 8*N
        self.scrollArea.setFixedHeight(min(h, 400))


class ClickableWindow(QWidget):
    """ Clickable window """

    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setFixedSize(292, 72)
        self._isPressed = None
        self._isEnter = False

    def enterEvent(self, e):
        self._isEnter = True
        self.update()

    def leaveEvent(self, e):
        self._isEnter = False
        self.update()

    def mouseReleaseEvent(self, e):
        self._isPressed = False
        self.update()
        if e.button() == Qt.LeftButton:
            self.clicked.emit()

    def mousePressEvent(self, e: QMouseEvent):
        self._isPressed = True
        self.update()

    def paintEvent(self, e):
        """ paint window """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        isDark = isDarkTheme()
        bg = 51 if isDark else 204
        brush = QBrush(QColor(bg, bg, bg))
        painter.setPen(Qt.NoPen)

        if not self._isEnter:
            painter.setBrush(brush)
            painter.drawRoundedRect(self.rect(), 4, 4)
        else:
            painter.setPen(QPen(QColor(bg, bg, bg), 2))
            painter.drawRect(1, 1, self.width() - 2, self.height() - 2)
            painter.setPen(Qt.NoPen)
            if not self._isPressed:
                bg = 24 if isDark else 230
                brush.setColor(QColor(bg, bg, bg))
                painter.setBrush(brush)
                painter.drawRect(2, 2, self.width() - 4, self.height() - 4)
            else:
                bg = 102 if isDark else 230
                brush.setColor(QColor(153, 153, 153))
                painter.setBrush(brush)
                painter.drawRoundedRect(
                    5, 1, self.width() - 10, self.height() - 2, 2, 2)


class FolderCard(ClickableWindow):
    """ Folder card """

    def __init__(self, folderPath: str, parent=None):
        super().__init__(parent)
        self.folderPath = folderPath
        self.folderName = os.path.basename(folderPath)
        c = getIconColor()
        self.__closeIcon = QPixmap(f":/qfluentwidgets/images/folder_list_dialog/Close_{c}.png").scaled(
            12, 12, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def paintEvent(self, e):
        """ paint card """
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform | QPainter.Antialiasing)

        # paint text and icon
        color = Qt.white if isDarkTheme() else Qt.black
        painter.setPen(color)
        if self._isPressed:
            self.__drawText(painter, 12, 8, 12, 7)
            painter.drawPixmap(self.width() - 26, 18, self.__closeIcon)
        else:
            self.__drawText(painter, 10, 9, 10, 8)
            painter.drawPixmap(self.width() - 24, 20, self.__closeIcon)

    def __drawText(self, painter, x1, fontSize1, x2, fontSize2):
        """ draw text """
        # paint folder name
        font = QFont("Microsoft YaHei", fontSize1, 75)
        painter.setFont(font)
        name = QFontMetrics(font).elidedText(
            self.folderName, Qt.ElideRight, self.width()-48)
        painter.drawText(x1, 30, name)

        # paint folder path
        font = QFont("Microsoft YaHei", fontSize2)
        painter.setFont(font)
        path = QFontMetrics(font).elidedText(
            self.folderPath, Qt.ElideRight, self.width()-24)
        painter.drawText(x2, 37, self.width() - 16, 18, Qt.AlignLeft, path)


class AddFolderCard(ClickableWindow):
    """ Add folder card """

    def __init__(self, parent=None):
        super().__init__(parent)
        c = getIconColor()
        self.__iconPix = QPixmap(f":/qfluentwidgets/images/folder_list_dialog/Add_{c}.png").scaled(
            22, 22, Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def paintEvent(self, e):
        """ paint card """
        super().paintEvent(e)
        painter = QPainter(self)
        w = self.width()
        h = self.height()
        pw = self.__iconPix.width()
        ph = self.__iconPix.height()
        if not self._isPressed:
            painter.drawPixmap(
                int(w/2 - pw/2), int(h/2 - ph/2), self.__iconPix)
        else:
            painter.drawPixmap(
                int(w/2 - (pw - 4)/2), int(h/2 - (ph - 4)/2), pw - 4, ph - 4, self.__iconPix)
