# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton

from ...common.style_sheet import FluentStyleSheet
from ..widgets.button import PrimaryPushButton

from .mask_dialog_base import MaskDialogBase


class MessageBoxBase(MaskDialogBase):
    """ Message box base """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.buttonGroup = QFrame(self.widget)
        self.yesButton = PrimaryPushButton(self.tr('OK'), self.buttonGroup)
        self.cancelButton = QPushButton(self.tr('Cancel'), self.buttonGroup)

        self.vBoxLayout = QVBoxLayout(self.widget)
        self.viewLayout = QVBoxLayout()
        self.buttonLayout = QHBoxLayout(self.buttonGroup)

        self.__initWidget()

    def __initWidget(self):
        self.__setQss()
        self.__initLayout()

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 50))
        self.setMaskColor(QColor(0, 0, 0, 76))

        # fixes https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/19
        self.yesButton.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        self.cancelButton.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        
        self.yesButton.setAttribute(Qt.WA_MacShowFocusRect, False)

        self.yesButton.setFocus()
        self.buttonGroup.setFixedHeight(81)

        self.yesButton.clicked.connect(self.__onYesButtonClicked)
        self.cancelButton.clicked.connect(self.__onCancelButtonClicked)

    def __initLayout(self):
        self._hBoxLayout.removeWidget(self.widget)
        self._hBoxLayout.addWidget(self.widget, 1, Qt.AlignCenter)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.viewLayout, 1)
        self.vBoxLayout.addWidget(self.buttonGroup, 0, Qt.AlignBottom)

        self.viewLayout.setSpacing(12)
        self.viewLayout.setContentsMargins(24, 24, 24, 24)

        self.buttonLayout.setSpacing(12)
        self.buttonLayout.setContentsMargins(24, 24, 24, 24)
        self.buttonLayout.addWidget(self.yesButton, 1, Qt.AlignVCenter)
        self.buttonLayout.addWidget(self.cancelButton, 1, Qt.AlignVCenter)

    def validate(self) -> bool:
        """ validate the data of form before closing dialog

        Returns
        -------
        isValid: bool
            whether the data of form is legal
        """
        return True

    def __onCancelButtonClicked(self):
        self.reject()

    def __onYesButtonClicked(self):
        if self.validate():
            self.accept()

    def __setQss(self):
        self.buttonGroup.setObjectName('buttonGroup')
        self.cancelButton.setObjectName('cancelButton')
        FluentStyleSheet.DIALOG.apply(self)

    def hideYesButton(self):
        self.yesButton.hide()
        self.buttonLayout.insertStretch(0, 1)

    def hideCancelButton(self):
        self.cancelButton.hide()
        self.buttonLayout.insertStretch(0, 1)

