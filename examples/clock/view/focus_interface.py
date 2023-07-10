# coding:utf-8
from PySide2.QtCore import Qt, QSize
from PySide2.QtGui import QPixmap, QPainter, QColor
from PySide2.QtWidgets import QWidget, QGraphicsDropShadowEffect

from view.Ui_FocusInterface import Ui_FocusInterface
from qfluentwidgets import FluentIcon, setFont


class FocusInterface(Ui_FocusInterface, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.timePicker.setSecondVisible(True)

        # set button icon
        self.pinButton.setIcon(FluentIcon.PIN)
        self.moreButton.setIcon(FluentIcon.MORE)
        self.startFocusButton.setIcon(FluentIcon.POWER_BUTTON)
        self.editButton.setIcon(FluentIcon.EDIT)

        setFont(self.progressRing, 14)
        self.hintLabel.setTextColor(QColor(96, 96, 96), QColor(206, 206, 206))

        # add shadow effect to card
        self.focusShadowEffect = QGraphicsDropShadowEffect(self)
        self.progressShadowEffect = QGraphicsDropShadowEffect(self)

        self.focusCard.setGraphicsEffect(self.focusShadowEffect)
        self.progressCard.setGraphicsEffect(self.progressShadowEffect)

        self.focusShadowEffect.setColor(QColor(0, 0, 0, 15))
        self.focusShadowEffect.setBlurRadius(10)
        self.focusShadowEffect.setOffset(0, 0)

        self.progressShadowEffect.setColor(QColor(0, 0, 0, 15))
        self.progressShadowEffect.setBlurRadius(10)
        self.progressShadowEffect.setOffset(0, 0)
