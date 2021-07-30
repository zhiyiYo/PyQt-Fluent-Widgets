# coding:utf-8
import os

from PyQt5.QtCore import QEasingCurve, QPropertyAnimation, Qt, pyqtSignal
from PyQt5.QtGui import (QBrush, QColor, QFont, QFontMetrics, QMouseEvent,
                         QPainter, QPen, QPixmap)
from PyQt5.QtWidgets import (QDialog, QGraphicsDropShadowEffect,
                             QGraphicsOpacityEffect, QLabel, QPushButton,
                             QWidget, QFileDialog, QHBoxLayout)

from dialog import Dialog


class FolderListDialog(QDialog):
    """ 文件夹列表对话框 """

    folderChanged = pyqtSignal(list)

    def __init__(self, folderPaths: list, title: str, content: str, parent):
        super().__init__(parent=parent)
        self.title = title
        self.content = content
        self.__original_paths = folderPaths
        self.folderPaths = folderPaths.copy()
        self.hBox = QHBoxLayout(self)
        self.windowMask = QWidget(self)
        self.widget = QWidget(self)
        self.titleLabel = QLabel(title, self.widget)
        self.contentLabel = QLabel(content, self.widget)
        self.completeButton = QPushButton('完成', self.widget)
        self.addFolderCard = AddFolderCard(self.widget)
        self.folderCards = [FolderCard(i, self.widget)
                            for i in folderPaths]
        self.__initWidget()

    def __initWidget(self):
        """ 初始化小部件 """
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.widget.setFixedSize(440, 324 + 100*len(self.folderPaths))
        self.setGeometry(0, 0, self.parent().width(), self.parent().height())
        self.windowMask.resize(self.size())
        self.__setQss()
        self.__initLayout()
        self.__setShadowEffect()
        # 信号连接到槽
        self.addFolderCard.clicked.connect(self.showFileDialog)
        self.completeButton.clicked.connect(self.__onButtonClicked)
        for card in self.folderCards:
            card.clicked.connect(self.showDeleteFolderCardDialog)

    def __initLayout(self):
        """ 初始化布局 """
        self.hBox.addWidget(self.widget)
        self.titleLabel.move(30, 30)
        self.contentLabel.move(30, 79)
        self.addFolderCard.move(35, 120)
        self.completeButton.move(223, self.widget.height() - 71)
        for i, folderCard in enumerate(self.folderCards):
            folderCard.move(36, 220 + i*100)

    def __setShadowEffect(self):
        """ 添加阴影 """
        shadowEffect = QGraphicsDropShadowEffect(self.widget)
        shadowEffect.setBlurRadius(50)
        shadowEffect.setOffset(0, 5)
        self.widget.setGraphicsEffect(shadowEffect)

    def showFileDialog(self):
        """ 显示文件对话框 """
        path = QFileDialog.getExistingDirectory(self, "选择文件夹", "./")
        if path and path not in self.folderPaths:
            # 创建文件路径卡
            self.widget.setFixedHeight(self.widget.height() + 100)
            folderCard = FolderCard(path, self.widget)
            folderCard.move(36, self.widget.height() - 206)
            folderCard.clicked.connect(self.showDeleteFolderCardDialog)
            folderCard.show()
            self.folderPaths.append(path)
            self.folderCards.append(folderCard)
            self.completeButton.move(223, self.widget.height() - 71)

    def showDeleteFolderCardDialog(self):
        """ 显示删除文件夹卡片对话框 """
        sender = self.sender()
        title = '确认删除文件夹吗？'
        content = f'如果将"{sender.folderName}"文件夹从列表中移除，则该文件夹不会再出现在列表中，但不会被删除。'
        dialog = Dialog(title, content, self.window())
        dialog.yesSignal.connect(lambda: self.deleteFolderCard(sender))
        dialog.exec_()

    def deleteFolderCard(self, folderCard):
        """ 删除选中的文件卡 """
        # 获取下标
        index = self.folderCards.index(folderCard)
        self.folderCards.pop(index)
        self.folderPaths.pop(index)
        folderCard.deleteLater()
        # 将下面的卡片上移
        for card in self.folderCards[index:]:
            card.move(card.x(), card.y() - 100)
        # 更新高度
        self.widget.setFixedHeight(self.widget.height() - 100)
        self.completeButton.move(223, self.widget.height() - 71)

    def showEvent(self, e):
        """ 淡入 """
        opacityEffect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacityEffect)
        opacityAni = QPropertyAnimation(opacityEffect, b'opacity', self)
        opacityAni.setStartValue(0)
        opacityAni.setEndValue(1)
        opacityAni.setDuration(200)
        opacityAni.setEasingCurve(QEasingCurve.InSine)
        opacityAni.finished.connect(opacityEffect.deleteLater)
        opacityAni.start()
        super().showEvent(e)

    def closeEvent(self, e):
        """ 淡出 """
        self.widget.setGraphicsEffect(None)
        opacityEffect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(opacityEffect)
        opacityAni = QPropertyAnimation(opacityEffect, b'opacity', self)
        opacityAni.setStartValue(1)
        opacityAni.setEndValue(0)
        opacityAni.setDuration(100)
        opacityAni.setEasingCurve(QEasingCurve.OutCubic)
        opacityAni.finished.connect(self.deleteLater)
        opacityAni.start()
        e.ignore()

    def __setQss(self):
        """ 设置层叠样式 """
        self.windowMask.setObjectName('windowMask')
        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        self.completeButton.setObjectName('completeButton')
        with open('resource/style/folder_list_dialog.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def __onButtonClicked(self):
        """ 完成按钮点击槽函数 """
        if sorted(self.__original_paths) != sorted(self.folderPaths):
            self.folderChanged.emit(self.folderPaths)
        self.close()


class ClickableWindow(QWidget):
    """ 可点击窗口 """

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.resize(365, 90)
        # 设置标志位
        self._isPressed = None
        self._isEnter = False

    def enterEvent(self, e):
        """ 鼠标进入界面就置位进入标志位 """
        self._isEnter = True
        self.update()

    def leaveEvent(self, e):
        """ 鼠标离开就清零置位标志位 """
        self._isEnter = False
        self.update()

    def mouseReleaseEvent(self, e):
        """ 鼠标松开时更新界面 """
        self._isPressed = False
        self.update()
        if e.button() == Qt.LeftButton:
            self.clicked.emit()

    def mousePressEvent(self, e: QMouseEvent):
        self._isPressed = True
        self.update()

    def paintEvent(self, e):
        """ 绘制背景 """
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        brush = QBrush(QColor(204, 204, 204))
        painter.setPen(Qt.NoPen)
        if not self._isEnter:
            painter.setBrush(brush)
            painter.drawRoundedRect(self.rect(), 5, 5)
        else:
            painter.setPen(QPen(QColor(204, 204, 204), 2))
            painter.drawRect(1, 1, self.width() - 2, self.height() - 2)
            painter.setPen(Qt.NoPen)
            if not self._isPressed:
                brush.setColor(QColor(230, 230, 230))
                painter.setBrush(brush)
                painter.drawRect(2, 2, self.width() - 4, self.height() - 4)
            else:
                brush.setColor(QColor(153, 153, 153))
                painter.setBrush(brush)
                painter.drawRoundedRect(
                    6, 1, self.width() - 12, self.height() - 2, 3, 3)


class FolderCard(ClickableWindow):
    """ 文件夹卡片 """

    def __init__(self, folderPath: str, parent=None):
        super().__init__(parent)
        self.folderPath = folderPath
        self.folderName = os.path.basename(folderPath)
        self.__closeIcon = QPixmap("resource/images/黑色叉号.png")

    def paintEvent(self, e):
        """ 绘制背景 """
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(
            QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform
        )
        # 绘制文字和图标
        if self._isPressed:
            self.__drawText(painter, 15, 10, 15, 9)
            painter.drawPixmap(
                self.width() - 33, 23, self.__closeIcon.width(), self.__closeIcon.height(), self.__closeIcon)
        else:
            self.__drawText(painter, 12, 11, 12, 10)
            painter.drawPixmap(
                self.width() - 30, 25, self.__closeIcon.width(), self.__closeIcon.height(), self.__closeIcon)

    def __drawText(self, painter, x1, fontSize1, x2, fontSize2):
        """ 绘制文字 """
        # 绘制文件夹名字
        font = QFont("Microsoft YaHei", fontSize1, 75)
        painter.setFont(font)
        name = QFontMetrics(font).elidedText(
            self.folderName, Qt.ElideRight, self.width()-60)
        painter.drawText(x1, 37, name)
        # 绘制路径
        font = QFont("Microsoft YaHei", fontSize2)
        painter.setFont(font)
        path = QFontMetrics(font).elidedText(
            self.folderPath, Qt.ElideRight, self.width()-30)
        painter.drawText(x2, 46, self.width() - 20, 23, Qt.AlignLeft, path)


class AddFolderCard(ClickableWindow):
    """ 点击选择模型 """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__iconPix = QPixmap("resource/images/黑色加号.png")

    def paintEvent(self, e):
        """ 绘制背景 """
        super().paintEvent(e)
        painter = QPainter(self)
        if not self._isPressed:
            painter.drawPixmap(
                int(self.width() / 2 - self.__iconPix.width() / 2),
                int(self.height() / 2 - self.__iconPix.height() / 2),
                self.__iconPix.width(),
                self.__iconPix.height(),
                self.__iconPix,
            )
        else:
            painter.drawPixmap(
                int(self.width() / 2 - (self.__iconPix.width() - 4) / 2),
                int(self.height() / 2 - (self.__iconPix.height() - 4) / 2),
                self.__iconPix.width() - 4,
                self.__iconPix.height() - 4,
                self.__iconPix,
            )
