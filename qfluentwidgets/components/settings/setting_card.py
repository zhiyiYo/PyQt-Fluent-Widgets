# coding:utf-8
from PySide6.QtCore import QUrl, Qt, Signal
from PySide6.QtGui import QColor, QDesktopServices
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QToolButton, QVBoxLayout, QPushButton
from PySide6.QtSvgWidgets import QSvgWidget

from ..dialog_box.color_dialog import ColorDialog
from ..widgets.combo_box import ComboBox
from ..widgets.switch_button import SwitchButton, IndicatorPosition
from ..widgets.slider import Slider
from ...common.style_sheet import setStyleSheet, getStyleSheet
from ...common.config import qconfig


class SettingCard(QFrame):
    """ Setting card """

    def __init__(self, iconPath, title, content=None, parent=None):
        """
        Parameters
        ----------
        iconPath: str
            the path of svg icon

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget
        """
        super().__init__(parent=parent)
        self.iconLabel = QSvgWidget(iconPath, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(content or '', self)
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        if not content:
            self.contentLabel.hide()

        self.setFixedHeight(70 if content else 50)
        self.iconLabel.setFixedSize(16, 16)

        # initialize layout
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(16, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignVCenter)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.addWidget(self.iconLabel, 0, Qt.AlignLeft)
        self.hBoxLayout.addSpacing(16)

        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignLeft)

        self.hBoxLayout.addSpacing(16)
        self.hBoxLayout.addStretch(1)

        self.contentLabel.setObjectName('contentLabel')
        setStyleSheet(self, 'setting_card')

    def setTitle(self, title: str):
        """ set the title of card """
        self.titleLabel.setText(title)

    def setContent(self, content: str):
        """ set the content of card """
        self.contentLabel.setText(content)
        self.contentLabel.setVisible(bool(content))


class SwitchSettingCard(SettingCard):
    """ Setting card with switch button """

    checkedChanged = Signal(bool)

    def __init__(self, iconPath, title, content=None, configItem=None, parent=None):
        """
        Parameters
        ----------
        iconPath: str
            the path of icon

        title: str
            the title of card

        content: str
            the content of card

        configItem: ConfigItem
            configuration item operated by the card

        parent: QWidget
            parent widget
        """
        super().__init__(iconPath, title, content, parent)
        self.configItem = configItem
        self.switchButton = SwitchButton(
            self.tr('Off'), self, IndicatorPosition.RIGHT)

        if configItem:
            self.setChecked(qconfig.get(configItem))

        setStyleSheet(self.switchButton, 'setting_card')

        # add switch button to layout
        self.hBoxLayout.addWidget(self.switchButton, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.switchButton.checkedChanged.connect(self.__onCheckedChanged)

    def __onCheckedChanged(self, isChecked: bool):
        """ switch button checked state changed slot """
        self.setChecked(isChecked)
        self.checkedChanged.emit(isChecked)

    def setChecked(self, isChecked: bool):
        """ set switch button checked state """
        if self.configItem:
            qconfig.set(self.configItem, isChecked)

        self.switchButton.setChecked(isChecked)
        self.switchButton.setText(
            self.tr('On') if isChecked else self.tr('Off'))

    def isChecked(self):
        return self.switchButton.isChecked()


class RangeSettingCard(SettingCard):
    """ Setting card with a slider """

    valueChanged = Signal(int)

    def __init__(self, configItem, iconPath, title, content=None, parent=None):
        """
        Parameters
        ----------
        configItem: RangeConfigItem
            configuration item operated by the card

        iconPath: str
            the path of icon

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget
        """
        super().__init__(iconPath, title, content, parent)
        self.configItem = configItem
        self.slider = Slider(Qt.Horizontal, self)
        self.valueLabel = QLabel(self)
        self.slider.setFixedWidth(268)

        self.slider.setSingleStep(1)
        self.slider.setRange(*configItem.range)
        self.slider.setValue(configItem.value)
        self.valueLabel.setNum(configItem.value)

        self.hBoxLayout.addWidget(self.valueLabel, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(6)
        self.hBoxLayout.addWidget(self.slider, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.valueLabel.setObjectName('valueLabel')
        self.slider.valueChanged.connect(self.__onValueChanged)

    def __onValueChanged(self, value: int):
        """ slider value changed slot """
        qconfig.set(self.configItem, value)
        self.valueLabel.setNum(value)
        self.valueLabel.adjustSize()
        self.valueChanged.emit(value)


class PushSettingCard(SettingCard):
    """ Setting card with a push button """

    clicked = Signal()

    def __init__(self, text, iconPath, title, content=None, parent=None):
        """
        Parameters
        ----------
        text: str
            the text of push button

        iconPath: str
            the path of icon

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget
        """
        super().__init__(iconPath, title, content, parent)
        self.button = QPushButton(text, self)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.button.clicked.connect(self.clicked)


class PrimaryPushSettingCard(PushSettingCard):
    """ Push setting card with primary color """

    def __init__(self, text, iconPath, title, content=None, parent=None):
        super().__init__(text, iconPath, title, content, parent)
        self.button.setObjectName('primaryButton')


class HyperlinkCard(SettingCard):
    """ Hyperlink card """

    def __init__(self, url, text, iconPath, title, content=None, parent=None):
        """
        Parameters
        ----------
        url: str
            the url to be opened

        text: str
            text of url

        iconPath: str
            the path of icon

        title: str
            the title of card

        content: str
            the content of card

        text: str
            the text of push button

        parent: QWidget
            parent widget
        """
        super().__init__(iconPath, title, content, parent)
        self.url = QUrl(url)
        self.linkButton = QPushButton(text, self)

        self.linkButton.setObjectName('hyperlinkButton')
        self.linkButton.setCursor(Qt.PointingHandCursor)
        self.linkButton.clicked.connect(
            lambda i: QDesktopServices.openUrl(self.url))

        self.hBoxLayout.addWidget(self.linkButton, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)


class ColorPickerButton(QToolButton):
    """ Color picker button """

    colorChanged = Signal(QColor)

    def __init__(self, color: QColor, title: str, parent=None):
        super().__init__(parent=parent)
        self.title = title
        self.setFixedSize(96, 32)
        self.setAutoFillBackground(True)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setColor(color)
        self.setCursor(Qt.PointingHandCursor)
        self.clicked.connect(self.__showColorDialog)

    def __showColorDialog(self):
        """ show color dialog """
        w = ColorDialog(self.color, self.tr(
            'Choose ')+self.title, self.window())
        w.updateStyle()
        w.colorChanged.connect(self.__onColorChanged)
        w.exec()

    def __onColorChanged(self, color: QColor):
        """ color changed slot """
        self.setColor(color)
        self.colorChanged.emit(color)

    def setColor(self, color: QColor):
        """ set color """
        self.color = QColor(color)
        qss = getStyleSheet('setting_card')
        qss = qss.replace('--color-picker-background', color.name())
        self.setStyleSheet(qss)


class ColorSettingCard(SettingCard):
    """ Setting card with color picker """

    colorChanged = Signal(QColor)

    def __init__(self, configItem, iconPath, title, content=None, parent=None):
        """
        Parameters
        ----------
        configItem: RangeConfigItem
            configuration item operated by the card

        iconPath: str
            the path of icon

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget
        """
        super().__init__(iconPath, title, content, parent)
        self.configItem = configItem
        self.colorPicker = ColorPickerButton(
            qconfig.get(configItem), title, self)
        self.hBoxLayout.addWidget(self.colorPicker, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.colorPicker.colorChanged.connect(self.__onColorChanged)

    def __onColorChanged(self, color: QColor):
        qconfig.set(self.configItem, color)
        self.colorChanged.emit(color)


class ComboBoxSettingCard(SettingCard):
    """ Setting card with a combo box """

    def __init__(self, configItem, iconPath, title, content=None, texts=None, parent=None):
        """
        Parameters
        ----------
        configItem: OptionsConfigItem
            configuration item operated by the card

        iconPath: str
            the path of icon

        title: str
            the title of card

        content: str
            the content of card

        texts: List[str]
            the text of items

        parent: QWidget
            parent widget
        """
        super().__init__(iconPath, title, content, parent)
        self.configItem = configItem
        self.comboBox = ComboBox(self)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.textToOption = {t: o for t, o in zip(texts, configItem.options)}
        self.optionToText = {o: t for o, t in zip(configItem.options, texts)}
        self.comboBox.addItems(texts)
        self.comboBox.setCurrentText(self.optionToText[qconfig.get(configItem)])
        self.comboBox.currentTextChanged.connect(self._onCurrentTextChanged)

    def _onCurrentTextChanged(self, text):
        qconfig.set(self.configItem, self.textToOption[text])