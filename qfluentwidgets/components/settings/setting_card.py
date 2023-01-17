# coding:utf-8
from PyQt5.QtCore import QUrl, Qt, pyqtSignal
from PyQt5.QtGui import QPixmap, QColor, QDesktopServices
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QToolButton, QVBoxLayout, QPushButton

from ..dialog_box.color_dialog import ColorDialog
from ..widgets.switch_button import SwitchButton, IndicatorPosition
from ..widgets.slider import Slider
from ..widgets.label import PixmapLabel
from ...common.style_sheet import setStyleSheet, getStyleSheet
from ...common.config import ConfigItem, config, RangeConfigItem
from ...common.icon import getIconColor


class SettingCard(QFrame):
    """ Setting card """

    def __init__(self, iconPath: str, title: str, content: str = None, parent=None):
        """
        Parameters
        ----------
        iconPath: str
            the path of icon

        title: str
            the title of card

        content: str
            the content of card

        parent: QWidget
            parent widget
        """
        super().__init__(parent=parent)
        self.iconLabel = PixmapLabel(self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(content or '', self)
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        if not content:
            self.contentLabel.hide()

        self.setFixedHeight(88 if content else 62)
        self.iconLabel.setFixedSize(20, 20)
        self.iconLabel.setPixmap(QPixmap(iconPath))

        # initialize layout
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(20, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignVCenter)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.addWidget(self.iconLabel, 0, Qt.AlignLeft)
        self.hBoxLayout.addSpacing(20)

        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignLeft)

        self.hBoxLayout.addSpacing(20)
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

    checkedChanged = pyqtSignal(bool)

    def __init__(self, iconPath: str, title: str, content: str = None, configItem: ConfigItem = None, parent=None):
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
            self.setChecked(config.get(configItem))

        setStyleSheet(self.switchButton, 'setting_card')

        # add switch button to layout
        self.hBoxLayout.addWidget(self.switchButton, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(20)

        self.switchButton.checkedChanged.connect(self.__onCheckedChanged)

    def __onCheckedChanged(self, isChecked: bool):
        """ switch button checked state changed slot """
        self.setChecked(isChecked)
        self.checkedChanged.emit(isChecked)

    def setChecked(self, isChecked: bool):
        """ set switch button checked state """
        if self.configItem:
            config.set(self.configItem, isChecked)

        self.switchButton.setChecked(isChecked)
        self.switchButton.setText(
            self.tr('On') if isChecked else self.tr('Off'))

    def isChecked(self):
        return self.switchButton.isChecked()


class RangeSettingCard(SettingCard):
    """ Setting card with a slider """

    valueChanged = pyqtSignal(int)

    def __init__(self, configItem: RangeConfigItem, iconPath: str, title: str, content: str = None, parent=None):
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
        self.slider.setFixedWidth(335)

        self.slider.setSingleStep(1)
        self.slider.setRange(*configItem.range)
        self.slider.setValue(configItem.value)
        self.valueLabel.setNum(configItem.value)

        self.hBoxLayout.addWidget(self.valueLabel, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(8)
        self.hBoxLayout.addWidget(self.slider, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(20)

        self.valueLabel.setObjectName('valueLabel')
        self.slider.valueChanged.connect(self.__onValueChanged)

    def __onValueChanged(self, value: int):
        """ slider value changed slot """
        config.set(self.configItem, value)
        self.valueLabel.setNum(value)
        self.valueLabel.adjustSize()
        self.valueChanged.emit(value)


class PushSettingCard(SettingCard):
    """ Setting card with a push button """

    clicked = pyqtSignal()

    def __init__(self, text, iconPath: str, title: str, content: str = None, parent=None):
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
        self.hBoxLayout.addSpacing(20)
        self.button.clicked.connect(self.clicked)


class PrimaryPushSettingCard(PushSettingCard):
    """ Push setting card with primary color """

    def __init__(self, text: str, iconPath: str, title: str, content: str = None, parent=None):
        super().__init__(text, iconPath, title, content, parent)
        self.button.setObjectName('primaryButton')


class HyperlinkCard(SettingCard):
    """ Hyperlink card """

    def __init__(self, url: str, text: str, iconPath: str, title: str, content: str = None, parent=None):
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
        self.hBoxLayout.addSpacing(20)


class ColorPickerButton(QToolButton):
    """ Color picker button """

    colorChanged = pyqtSignal(QColor)

    def __init__(self, color: QColor, title: str, parent=None):
        super().__init__(parent=parent)
        self.title = title
        self.setFixedSize(120, 40)
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

    colorChanged = pyqtSignal(QColor)

    def __init__(self, configItem: ConfigItem, iconPath: str, title: str, content: str = None, parent=None):
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
            config.get(configItem), title, self)
        self.hBoxLayout.addWidget(self.colorPicker, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(20)
        self.colorPicker.colorChanged.connect(self.__onColorChanged)

    def __onColorChanged(self, color: QColor):
        config.set(self.configItem, color)
        self.colorChanged.emit(color)


class SettingIconFactory:
    """ Setting icon factory """

    WEB = "Web"
    LINK = "Link"
    HELP = "Help"
    FONT = "Font"
    INFO = "Info"
    ZOOM = "Zoom"
    CLOSE = "Close"
    MOVIE = "Movie"
    BRUSH = "Brush"
    MUSIC = "Music"
    VIDEO = "Video"
    EMBED = "Embed"
    ALBUM = "Album"
    FOLDER = "Folder"
    SEARCH = "Search"
    UPDATE = "Update"
    PALETTE = "Palette"
    FEEDBACK = "Feedback"
    MINIMIZE = "Minimize"
    DOWNLOAD = "Download"
    QUESTION = "Question"
    ALIGNMENT = "Alignment"
    PENCIL_INK = "PencilInk"
    FOLDER_ADD = "FolderAdd"
    ARROW_DOWN = "ChevronDown"
    FILE_SEARCH = "FileSearch"
    TRANSPARENT = "Transparent"
    MUSIC_FOLDER = "MusicFolder"
    BACKGROUND_FILL = "BackgroundColor"
    FLUORESCENT_PEN = "FluorescentPen"

    @staticmethod
    def create(iconType: str):
        """ create icon """
        return f':/qfluentwidgets/images/setting_card/{iconType}_{getIconColor()}.png'
