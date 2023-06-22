# coding:utf-8
from typing import List

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout

from ...common.style_sheet import FluentStyleSheet
from ...common.font import setFont
from ..layout.expand_layout import ExpandLayout


class SettingCardGroup(QWidget):
    """ Setting card group """

    def __init__(self, title: str, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = QLabel(title, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.cardLayout = ExpandLayout()

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setSpacing(0)
        self.cardLayout.setContentsMargins(0, 0, 0, 0)
        self.cardLayout.setSpacing(2)

        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(12)
        self.vBoxLayout.addLayout(self.cardLayout, 1)

        FluentStyleSheet.SETTING_CARD_GROUP.apply(self)
        setFont(self.titleLabel, 20)
        self.titleLabel.adjustSize()

    def addSettingCard(self, card: QWidget):
        """ add setting card to group """
        card.setParent(self)
        self.cardLayout.addWidget(card)
        self.adjustSize()

    def addSettingCards(self, cards: List[QWidget]):
        """ add setting cards to group """
        for card in cards:
            self.addSettingCard(card)

    def adjustSize(self):
        h = self.cardLayout.heightForWidth(self.width()) + 46
        return self.resize(self.width(), h)
