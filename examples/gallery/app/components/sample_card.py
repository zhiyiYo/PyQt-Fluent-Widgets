# coding:utf-8
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QWidget, QFrame, QLabel, QVBoxLayout, QHBoxLayout

from qfluentwidgets import IconWidget, TextWrap, FlowLayout, isDarkTheme
from ..common.signal_bus import signalBus
from ..common.config import cfg


class SampleCard(QFrame):
    """ Sample card """

    def __init__(self, icon, title, content, routeKey, index, parent=None):
        super().__init__(parent=parent)
        self.index = index
        self.routekey = routeKey

        self.iconWidget = IconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(TextWrap.wrap(content, 46, False)[0], self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedSize(360, 90)
        self.iconWidget.setFixedSize(48, 48)

        self.hBoxLayout.setSpacing(28)
        self.hBoxLayout.setContentsMargins(20, 0, 0, 0)
        self.vBoxLayout.setSpacing(2)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        self.hBoxLayout.addWidget(self.iconWidget)
        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.addStretch(1)

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        signalBus.switchToSampleCard.emit(self.routekey, self.index)


class SampleCardView(QWidget):
    """ Sample card view """

    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = QLabel(title, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.flowLayout = FlowLayout()

        self.vBoxLayout.setContentsMargins(36, 0, 36, 0)
        self.vBoxLayout.setSpacing(10)
        self.flowLayout.setContentsMargins(0, 0, 0, 0)
        self.flowLayout.setHorizontalSpacing(12)
        self.flowLayout.setVerticalSpacing(12)

        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addLayout(self.flowLayout, 1)

        self.titleLabel.setObjectName('viewTitleLabel')
        self.__setQss()
        cfg.themeChanged.connect(self.__setQss)

    def addSampleCard(self, icon, title, content, routeKey, index):
        """ add sample card """
        card = SampleCard(icon, title, content, routeKey, index, self)
        self.flowLayout.addWidget(card)

    def __setQss(self):
        theme = 'dark' if isDarkTheme() else 'light'
        with open(f'app/resource/qss/{theme}/sample_card.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
