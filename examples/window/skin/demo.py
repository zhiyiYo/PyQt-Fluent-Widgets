# coding:utf-8
import sys

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor, QImage, QPainter, QLinearGradient
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QHBoxLayout,
                             QVBoxLayout, QTableWidgetItem, QHeaderView)

from qfluentwidgets import (FluentIcon as FIF, Action,
                            MSFluentWindow, NavigationItemPosition, RoundMenu,
                            PushButton, PrimaryPushButton, TransparentPushButton,
                            TransparentToolButton, TogglePushButton, HyperlinkButton,
                            DropDownPushButton, ToolButton, RadioButton, CheckBox,
                            SwitchButton, FlowLayout,
                            LineEdit, SearchLineEdit, TextEdit, SpinBox, ComboBox,
                            EditableComboBox, DateEdit, DatePicker, CalendarPicker,
                            Slider, ProgressBar, IndeterminateProgressBar, ProgressRing,
                            IndeterminateProgressRing,
                            SegmentedWidget, HorizontalPipsPager, TableWidget,
                            SimpleCardWidget, CardWidget, ElevatedCardWidget,
                            HorizontalSeparator, ScrollArea,
                            Flyout, InfoBar, InfoBarIcon, InfoBarPosition,
                            TeachingTip, TeachingTipTailPosition, MessageBox,
                            MessageBoxBase, TitleLabel, CaptionLabel, StrongBodyLabel,
                            BodyLabel, SubtitleLabel, ColorPickerButton,
                            SwitchSettingCard, ComboBoxSettingCard,
                            SettingCardGroup, ExpandGroupSettingCard,
                            CommandBar,
                            ConfigItem, OptionsConfigItem, BoolValidator, OptionsValidator,
                            HorizontalFlipView,
                            tintColor, setTheme, setThemeColor, setSurfaceTint, Theme)

# not exported from the package root
from qfluentwidgets.components.settings.expand_setting_card import HeaderSettingCard


SKINS = [
    # name, base theme, accent color, surface tint, tint strength
    ('Default',    Theme.LIGHT, '#009faa', None,       0),
    ('Dark',       Theme.DARK,  '#009faa', None,       0),
    ('Dark gold',  Theme.DARK,  '#D4AF37', '#3A2D12',  0.28),
    ('Deep ocean', Theme.DARK,  '#4CC2FF', '#12304E',  0.28),
    ('Paper ink',  Theme.LIGHT, '#7A5C2E', '#F2E8D5',  0.20),
    ('Celadon',    Theme.LIGHT, '#2F7D6C', '#E7F2EC',  0.22),
]

# in-memory config items, they are not persisted anywhere
syncEnabledItem = ConfigItem('SkinDemo', 'SyncEnabled', False, BoolValidator())
languageItem = OptionsConfigItem(
    'SkinDemo', 'Language', 'English', OptionsValidator(['English', '简体中文']))


def makeFlipImage(text: str) -> QImage:
    """ create a placeholder image for the flip view """
    image = QImage(280, 150, QImage.Format_ARGB32)
    painter = QPainter(image)
    painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

    gradient = QLinearGradient(0, 0, 280, 150)
    gradient.setColorAt(0, QColor(72, 76, 82))
    gradient.setColorAt(1, QColor(38, 40, 44))
    painter.fillRect(image.rect(), gradient)

    painter.setPen(QColor(245, 245, 245))
    font = painter.font()
    font.setPointSize(16)
    painter.setFont(font)
    painter.drawText(image.rect(), Qt.AlignCenter, text)
    painter.end()
    return image


class Section(SimpleCardWidget):
    """ a titled card that groups demo widgets """

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.titleLabel = StrongBodyLabel(title, self)
        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(24, 16, 24, 20)
        self.vBoxLayout.setSpacing(14)
        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addSpacing(4)

    def addLayout(self, layout):
        self.vBoxLayout.addLayout(layout)

    def addWidget(self, widget):
        self.vBoxLayout.addWidget(widget)


class CustomSkinDialog(MessageBoxBase):
    """ custom skin dialog

    The six presets in the header are demo data; this dialog shows that any
    combination of the three theme APIs forms a custom skin:
    setTheme, setThemeColor and setSurfaceTint.
    """

    def __init__(self, skin, parent=None):
        super().__init__(parent)
        self.skin = skin
        self.titleLabel = SubtitleLabel('Custom skin', self)

        # base theme
        self.lightRadioButton = RadioButton('Light', self)
        self.darkRadioButton = RadioButton('Dark', self)
        if skin[1] == Theme.DARK:
            self.darkRadioButton.setChecked(True)
        else:
            self.lightRadioButton.setChecked(True)

        # accent color
        self.accentButton = ColorPickerButton(QColor(skin[2]), 'Accent color', self)

        # surface tint
        self.tintEnabledBox = CheckBox('Enable surface tint', self)
        self.tintEnabledBox.setChecked(skin[3] is not None)
        self.tintButton = ColorPickerButton(
            QColor(skin[3] or '#3A2D12'), 'Surface tint', self)
        self.tintButton.setEnabled(skin[3] is not None)
        self.tintEnabledBox.toggled.connect(self.tintButton.setEnabled)

        # tint strength
        self.strengthSlider = Slider(Qt.Horizontal, self)
        self.strengthSlider.setRange(0, 100)
        self.strengthSlider.setValue(int((skin[4] or 0.28) * 100))
        self.strengthLabel = CaptionLabel(f'{(skin[4] or 0.28):.2f}', self)
        self.strengthSlider.valueChanged.connect(
            lambda value: self.strengthLabel.setText(f'{value / 100:.2f}'))

        # assemble the form
        self.viewLayout.addWidget(self.titleLabel)
        themeRow = QHBoxLayout()
        themeRow.addStretch(1)
        themeRow.addWidget(self.lightRadioButton)
        themeRow.addWidget(self.darkRadioButton)
        self.__addRow('Base theme', themeRow)
        self.__addRow('Accent color', self.accentButton)
        self.__addRow('Surface tint', self.tintButton)
        self.__addRow('Enable tint', self.tintEnabledBox)

        strengthRow = QHBoxLayout()
        strengthRow.addWidget(self.strengthSlider, 1)
        strengthRow.addWidget(self.strengthLabel)
        self.__addRow('Strength', strengthRow)

        self.yesButton.setText('Apply')
        self.cancelButton.setText('Cancel')
        self.widget.setMinimumWidth(380)

    def __addRow(self, label: str, item):
        row = QHBoxLayout()
        row.addWidget(BodyLabel(label, self))
        row.addStretch(1)
        if isinstance(item, QWidget):
            row.addWidget(item)
        else:
            row.addLayout(item)
        self.viewLayout.addLayout(row)

    def customSkin(self):
        """ return the skin tuple assembled from the current form state """
        return (
            'Custom',
            Theme.DARK if self.darkRadioButton.isChecked() else Theme.LIGHT,
            self.accentButton.color.name(),
            self.tintButton.color.name() if self.tintEnabledBox.isChecked() else None,
            self.strengthSlider.value() / 100,
        )


class Interface(ScrollArea):
    """ transparent scrollable interface hosted by the fluent window """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scrollWidget = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)

        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.enableTransparentBackground()

        self.vBoxLayout.setContentsMargins(36, 24, 36, 24)
        self.vBoxLayout.setSpacing(16)

    def addHeader(self, title: str, content: str):
        self.vBoxLayout.addWidget(TitleLabel(title, self.scrollWidget))
        caption = CaptionLabel(content, self.scrollWidget)
        caption.setWordWrap(True)
        self.vBoxLayout.addWidget(caption)
        self.vBoxLayout.addSpacing(6)

        # every interface carries the skin buttons in its header
        skinLayout = QHBoxLayout()
        skinLayout.setSpacing(10)
        for skin in SKINS:
            button = PrimaryPushButton(skin[0], self.scrollWidget)
            button.setFixedHeight(33)
            button.clicked.connect(lambda _, s=skin: self.window().applySkin(s))
            skinLayout.addWidget(button)

        customButton = PushButton('Custom…', self.scrollWidget)
        customButton.setFixedHeight(33)
        customButton.clicked.connect(lambda: self.window().showCustomSkinDialog())
        skinLayout.addWidget(customButton)

        skinLayout.addStretch(1)
        self.vBoxLayout.addLayout(skinLayout)

        self.vBoxLayout.addWidget(HorizontalSeparator(self.scrollWidget))


class BasicInterface(Interface):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('basicInterface')

        self.addHeader(
            'Skin & surface tint',
            'Surfaces (cards, flyouts, menus, navigation…) follow the tint, '
            'accent and content colors stay untouched. Pick a skin from the '
            'buttons in the header of every interface.')

        self.__initCardsSection()
        self.__initButtonsSection()
        self.__initInputSection()
        self.vBoxLayout.addStretch(1)

    # ------------------------------------------------------------------ cards

    def __initCardsSection(self):
        section = Section('Cards', self.scrollWidget)
        layout = QHBoxLayout()
        layout.setSpacing(12)

        for cardClass, name, desc in [
                (CardWidget, 'CardWidget', 'Clickable, hover and press states'),
                (SimpleCardWidget, 'SimpleCardWidget', 'Static card surface'),
                (ElevatedCardWidget, 'ElevatedCardWidget', 'Card with drop shadow')]:
            card = cardClass(self.scrollWidget)
            card.setFixedHeight(104)
            layout.addWidget(card, 1)

            vBox = QVBoxLayout(card)
            vBox.setContentsMargins(20, 16, 20, 16)
            vBox.setSpacing(4)
            vBox.addWidget(StrongBodyLabel(name, card))
            vBox.addWidget(CaptionLabel(desc, card))
            vBox.addStretch(1)

        section.addLayout(layout)
        self.vBoxLayout.addWidget(section)

    # ---------------------------------------------------------------- buttons

    def __initButtonsSection(self):
        section = Section('Buttons & switches', self.scrollWidget)
        flow = FlowLayout()

        menu = RoundMenu(parent=self)
        menu.addAction(Action(FIF.CUT, 'Cut'))
        menu.addAction(Action(FIF.COPY, 'Copy'))
        menu.addAction(Action(FIF.PASTE, 'Paste'))
        dropButton = DropDownPushButton('More')
        dropButton.setMenu(menu)

        for widget in [
                PushButton(FIF.ALBUM, 'Push'),
                PrimaryPushButton(FIF.BASKETBALL, 'Primary'),
                TransparentPushButton(FIF.BOOK_SHELF, 'Transparent'),
                TogglePushButton(FIF.DEVELOPER_TOOLS, 'Toggle'),
                dropButton,
                HyperlinkButton('https://github.com/zhiyiYo/PyQt-Fluent-Widgets', 'Hyperlink'),
                ToolButton(FIF.SETTING),
                TransparentToolButton(FIF.BRUSH),
                RadioButton('Option A'),
                CheckBox('Check me'),
                SwitchButton(),
        ]:
            flow.addWidget(widget)

        section.addLayout(flow)
        self.vBoxLayout.addWidget(section)

    # ------------------------------------------------------------------ input

    def __initInputSection(self):
        section = Section('Input & pickers', self.scrollWidget)
        grid = QGridLayout()
        grid.setHorizontalSpacing(12)
        grid.setVerticalSpacing(12)

        lineEdit = LineEdit()
        lineEdit.setPlaceholderText('Type something...')
        searchEdit = SearchLineEdit()
        searchEdit.setPlaceholderText('Search...')
        textEdit = TextEdit()
        textEdit.setFixedHeight(72)
        textEdit.setPlaceholderText('Text edit')

        comboBox = ComboBox()
        comboBox.addItems(['Cheetah', 'Leopard', 'Tiger'])
        editableComboBox = EditableComboBox()
        editableComboBox.addItems(['Cat', 'Dog', 'Bird'])

        widgets = [lineEdit, searchEdit, comboBox, editableComboBox,
                   SpinBox(), DateEdit(), DatePicker(), CalendarPicker()]
        for i, widget in enumerate(widgets):
            grid.addWidget(widget, i // 4, i % 4)
        grid.addWidget(textEdit, 2, 0, 1, 4)
        for column in range(4):
            grid.setColumnStretch(column, 1)

        section.addLayout(grid)
        self.vBoxLayout.addWidget(section)


class ViewsInterface(Interface):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('viewsInterface')
        self.addHeader('Views & progress', 'Progress, segmented and paged views, '
                                          'tables, command bar and flip view.')

        self.__initProgressSection()
        self.__initNavigationSection()
        self.__initCommandSection()
        self.vBoxLayout.addStretch(1)

    # --------------------------------------------------------------- progress

    def __initProgressSection(self):
        section = Section('Progress & slider', self.scrollWidget)

        slider = Slider(Qt.Horizontal)
        slider.setValue(30)

        barRow = QHBoxLayout()
        barRow.setSpacing(12)
        progressBar = ProgressBar()
        progressBar.setValue(60)
        indeterminateBar = IndeterminateProgressBar()
        indeterminateBar.start()
        barRow.addWidget(progressBar, 1)
        barRow.addWidget(indeterminateBar, 1)

        ringRow = QHBoxLayout()
        ringRow.setSpacing(24)
        ring = ProgressRing()
        ring.setValue(70)
        indeterminateRing = IndeterminateProgressRing()
        indeterminateRing.start()
        ringRow.addWidget(ring)
        ringRow.addWidget(indeterminateRing)
        ringRow.addStretch(1)

        section.addWidget(slider)
        section.addLayout(barRow)
        section.addLayout(ringRow)
        self.vBoxLayout.addWidget(section)

    # ------------------------------------------------------------- navigation

    def __initNavigationSection(self):
        section = Section('Navigation & views', self.scrollWidget)

        navRow = QHBoxLayout()
        navRow.setSpacing(24)
        segmentedWidget = SegmentedWidget(self.scrollWidget)
        for key, text in [('song', 'Song'), ('album', 'Album'), ('artist', 'Artist')]:
            segmentedWidget.addItem(routeKey=key, text=text)
        segmentedWidget.setCurrentItem('song')
        pager = HorizontalPipsPager(self.scrollWidget)
        pager.setPageNumber(6)
        pager.setCurrentIndex(1)
        navRow.addWidget(segmentedWidget, 1)
        navRow.addWidget(pager, 0, Qt.AlignVCenter)

        tableView = TableWidget(self.scrollWidget)
        tableView.setBorderVisible(True)
        tableView.setBorderRadius(8)
        tableView.setWordWrap(False)
        tableView.setFixedHeight(190)
        tableView.verticalHeader().hide()
        tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        tableView.setRowCount(4)
        tableView.setColumnCount(3)
        tableView.setHorizontalHeaderLabels(['Name', 'Type', 'Note'])
        for row, cells in enumerate([
                ['Card', 'Surface', 'Follows the tint'],
                ['Flyout', 'Surface', 'Follows the tint'],
                ['Text', 'Content', 'Stays as it is'],
                ['Accent', 'Content', 'Stays as it is']]):
            for column, cell in enumerate(cells):
                tableView.setItem(row, column, QTableWidgetItem(cell))

        section.addLayout(navRow)
        section.addWidget(tableView)
        self.vBoxLayout.addWidget(section)

    # ---------------------------------------------------------- command & flip

    def __initCommandSection(self):
        section = Section('Command bar & flip view', self.scrollWidget)

        commandBar = CommandBar(self.scrollWidget)
        commandBar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        commandBar.addActions([
            Action(FIF.ADD, 'Add'),
            Action(FIF.ROTATE, 'Rotate'),
            Action(FIF.ZOOM_IN, 'Zoom in'),
        ])
        commandBar.addSeparator()
        commandBar.addActions([
            Action(FIF.EDIT, 'Edit', checkable=True),
            Action(FIF.DELETE, 'Delete'),
        ])

        flipView = HorizontalFlipView(self.scrollWidget)
        flipView.setItemSize(QSize(280, 150))
        flipView.setFixedHeight(160)
        for i in range(3):
            flipView.addImage(makeFlipImage(f'Page {i + 1}'))

        section.addWidget(commandBar)
        section.addWidget(flipView)
        self.vBoxLayout.addWidget(section)


class DialogsInterface(Interface):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('dialogsInterface')
        self.addHeader('Flyouts, tips & dialogs',
                       'Every popup surface follows the tint as well.')

        section = Section('Popups', self.scrollWidget)

        self.flyoutButton = PushButton(FIF.INFO, 'Show flyout')
        self.flyoutButton.clicked.connect(
            lambda: self.window().showFlyout(self.flyoutButton))
        tipButton = PushButton(FIF.EDUCATION, 'Show teaching tip')
        tipButton.clicked.connect(lambda: self.window().showTeachingTip(tipButton))
        infoBarButton = PushButton(FIF.MESSAGE, 'Show info bar')
        infoBarButton.clicked.connect(lambda: self.window().showInfoBar())
        messageBoxButton = PushButton(FIF.FLAG, 'Show message box')
        messageBoxButton.clicked.connect(lambda: self.window().showMessageBox())

        for button in (self.flyoutButton, tipButton, infoBarButton, messageBoxButton):
            section.addWidget(button)

        self.vBoxLayout.addWidget(section)
        self.vBoxLayout.addStretch(1)


class SettingsInterface(Interface):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('settingsInterface')
        self.addHeader('Setting cards', 'Setting cards paint their own surfaces, '
                                        'they follow the tint too.')

        self.vBoxLayout.addWidget(HeaderSettingCard(
            FIF.BRUSH, 'Personalization', 'Customize the look and feel of the app',
            self.scrollWidget))

        personalGroup = SettingCardGroup('Sync & language', self.scrollWidget)
        personalGroup.addSettingCards([
            SwitchSettingCard(
                FIF.SYNC, 'Sync settings',
                'Sync your preferences between devices',
                configItem=syncEnabledItem, parent=personalGroup),
            ComboBoxSettingCard(
                languageItem, FIF.LANGUAGE, 'Language', 'The interface language',
                texts=['English', '简体中文'], parent=personalGroup),
        ])
        self.vBoxLayout.addWidget(personalGroup)

        expandCard = ExpandGroupSettingCard(
            FIF.SETTING, 'More settings', 'Expand to see the grouped options',
            self.scrollWidget)
        expandCard.addGroup(
            FIF.WIFI, 'Auto connect', 'Connect to known networks automatically',
            SwitchButton())
        expandCard.addGroup(
            FIF.TAG, 'Compact mode', 'Reduce the spacing between widgets',
            RadioButton(''))
        expandCard.addGroup(
            FIF.QUIET_HOURS, 'Quiet hours', 'Silence notifications',
            CheckBox(''))
        self.vBoxLayout.addWidget(expandCard)
        self.vBoxLayout.addStretch(1)


class Demo(MSFluentWindow):

    def __init__(self):
        super().__init__()
        self.currentSkin = None

        # the window background is painted by ourselves, disable the win11
        # mica material so the tinted background is visible on every platform
        self.setMicaEffectEnabled(False)
        self.setWindowTitle('Surface tint demo')
        self.resize(1000, 720)

        # sub interfaces
        self.basicInterface = BasicInterface(self)
        self.viewsInterface = ViewsInterface(self)
        self.dialogsInterface = DialogsInterface(self)
        self.settingsInterface = SettingsInterface(self)

        self.addSubInterface(self.basicInterface, FIF.HOME, 'Basic')
        self.addSubInterface(self.viewsInterface, FIF.ALBUM, 'Views')
        self.addSubInterface(self.dialogsInterface, FIF.MESSAGE, 'Dialogs')
        self.addSubInterface(
            self.settingsInterface, FIF.SETTING, 'Settings',
            position=NavigationItemPosition.BOTTOM)

        self.applySkin(SKINS[0])

    def applySkin(self, skin):
        name, base, accent, tint, strength = skin
        setTheme(base, save=False)
        setThemeColor(accent, save=False)
        setSurfaceTint(tint, strength)

        # the fluent window paints its own background, so it is one of the
        # custom-color APIs: feed it the tinted colors ourselves
        self.setCustomBackgroundColor(
            tintColor(QColor(240, 244, 249)), tintColor(QColor(32, 32, 32)))
        self.currentSkin = skin

    def showCustomSkinDialog(self):
        dialog = CustomSkinDialog(self.currentSkin, self)
        if dialog.exec():
            self.applySkin(dialog.customSkin())

    def showFlyout(self, target):
        Flyout.create(
            icon=InfoBarIcon.INFORMATION,
            title='Flyout',
            content='The flyout background follows the surface tint as well',
            target=target,
            parent=self,
            isClosable=True
        )

    def showTeachingTip(self, target):
        TeachingTip.create(
            target=target,
            icon=InfoBarIcon.SUCCESS,
            title='Teaching tip',
            content='The bubble and border of the teaching tip are tinted too.',
            isClosable=True,
            tailPosition=TeachingTipTailPosition.TOP,
            duration=2500,
            parent=self
        )

    def showInfoBar(self):
        InfoBar.success(
            title='Info bar',
            content='A success message from the info bar.',
            position=InfoBarPosition.TOP,
            duration=2500,
            parent=self
        )

    def showMessageBox(self):
        MessageBox(
            'Message box', 'The message box background follows the surface tint.',
            self).exec_()


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    sys.exit(app.exec_())
