# coding:utf-8
import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QHBoxLayout,
                             QVBoxLayout)

from qfluentwidgets import (FluentIcon as FIF, Action, MSFluentWindow, RoundMenu,
                            PushButton, PrimaryPushButton, TransparentPushButton,
                            TogglePushButton, HyperlinkButton, DropDownPushButton,
                            ToolButton, TransparentToolButton, RadioButton, CheckBox,
                            SwitchButton, FlowLayout,
                            LineEdit, SearchLineEdit, TextEdit, SpinBox, ComboBox,
                            EditableComboBox, DateEdit, DatePicker, CalendarPicker,
                            SimpleCardWidget, CardWidget, ElevatedCardWidget,
                            HorizontalSeparator, ScrollArea, SkinCardView,
                            CustomSkinDialog, TitleLabel, CaptionLabel,
                            StrongBodyLabel, FluentSkin, FluentSkinSet,
                            FluentSkinSetBase, Theme)


class BrandSkins(FluentSkinSetBase):
    """ a brand palette, it holds nothing but the four skins below

    `FluentSkinSetBase` is the abstract base class, it declares no skin of its
    own. Inheriting from `FluentSkinSet` instead would bring the 32 built-in
    presets along, which is only what you want when you extend them on
    purpose. Call `BrandSkins.register()` as well if you want
    `FluentSkin.get('Aurora')` to find them, the card view doesn't need it
    because the skins are passed in explicitly.

    The window background and the surface tint are what actually change the
    look of a skin. Swapping the accent color alone leaves the large areas
    untouched, and every skin ends up looking the same.
    """

    AURORA_LIGHT = FluentSkin(
        'Aurora', Theme.LIGHT, '#0E8C7F', '#CDE9E4', 0.55,
        lightWindowBackground='#CEE6E1', darkWindowBackground='#0E1211')
    AURORA_DARK = FluentSkin(
        'Aurora dark', Theme.DARK, '#5FD9C6', '#14312D', 0.55,
        lightWindowBackground='#CEE6E1', darkWindowBackground='#0E1211')
    SUNSET = FluentSkin(
        'Sunset', Theme.LIGHT, '#C8552B', '#F7DCC8', 0.60,
        lightWindowBackground='#F5DAC2', darkWindowBackground='#1A1210')
    TERMINAL = FluentSkin(
        'Terminal', Theme.DARK, '#3DDC84', '#0D2A1B', 0.60,
        lightWindowBackground='#EDF3EF', darkWindowBackground='#08120D')



class Section(SimpleCardWidget):
    """ a titled card that groups demo widgets """

    def __init__(self, title: str, parent=None):
        super().__init__(parent)
        self.titleLabel = StrongBodyLabel(title, self)
        self.hintLabel = CaptionLabel('', self)

        self.headerLayout = QHBoxLayout()
        self.headerLayout.setSpacing(8)
        self.headerLayout.addWidget(self.titleLabel)
        self.headerLayout.addStretch(1)
        self.headerLayout.addWidget(self.hintLabel)

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setContentsMargins(24, 16, 24, 20)
        self.vBoxLayout.setSpacing(14)
        self.vBoxLayout.addLayout(self.headerLayout)
        self.vBoxLayout.addSpacing(4)

    def setHint(self, text: str):
        """ show a short hint at the right side of the title """
        self.hintLabel.setText(text)

    def addLayout(self, layout):
        self.vBoxLayout.addLayout(layout)

    def addWidget(self, widget):
        self.vBoxLayout.addWidget(widget)


class DemoInterface(ScrollArea):
    """ the one and only interface of the demo """

    skinChanged = pyqtSignal(object)
    customRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('demoInterface')

        self.scrollWidget = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.scrollWidget)

        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.enableTransparentBackground()

        self.vBoxLayout.setContentsMargins(36, 24, 36, 24)
        self.vBoxLayout.setSpacing(16)

        self.addHeader(
            'Skin & surface tint',
            'A skin bundles the base theme, the accent color, the surface tint '
            'and the window background. Surfaces (cards, flyouts, menus, '
            'navigation…) follow the tint, accent and content colors stay '
            'untouched. Pick a preview below, the last four ones are the '
            'BrandSkins defined at the top of this file.')
        self.__initSkinsSection()
        self.__initCardsSection()
        self.__initButtonsSection()
        self.__initInputSection()
        self.vBoxLayout.addStretch(1)

    def addHeader(self, title: str, content: str):
        self.vBoxLayout.addWidget(TitleLabel(title, self.scrollWidget))
        caption = CaptionLabel(content, self.scrollWidget)
        caption.setWordWrap(True)
        self.vBoxLayout.addWidget(caption)
        self.vBoxLayout.addSpacing(6)
        self.vBoxLayout.addWidget(HorizontalSeparator(self.scrollWidget))

    def __initSkinsSection(self):
        self.skinsSection = Section('Skins', self.scrollWidget)
        skins = FluentSkinSet.skins() + BrandSkins.skins()
        self.skinCardView = SkinCardView(skins, self.skinsSection)
        self.skinCardView.skinChanged.connect(self.skinChanged)
        self.skinCardView.customRequested.connect(self.customRequested)

        self.skinsSection.addWidget(self.skinCardView)
        self.vBoxLayout.addWidget(self.skinsSection)

    def setCurrentSkin(self, skin: FluentSkin):
        """ sync the selected preview without notifying the window again """
        self.skinsSection.setHint(skin.name)

        self.skinCardView.blockSignals(True)
        self.skinCardView.setCurrentSkin(skin)
        self.skinCardView.blockSignals(False)

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


class Demo(MSFluentWindow):

    def __init__(self):
        super().__init__()
        self.currentSkin = None

        # the window background is painted by ourselves, disable the win11
        # mica material so the tinted background is visible on every platform
        self.setMicaEffectEnabled(False)
        self.setWindowTitle('Skin demo')
        self.resize(1000, 860)

        self.demoInterface = DemoInterface(self)
        self.demoInterface.skinChanged.connect(self.applySkin)
        self.demoInterface.customRequested.connect(self.showCustomSkinDialog)
        self.addSubInterface(self.demoInterface, FIF.BRUSH, 'Skin')

        self.applySkin(FluentSkinSet.DEFAULT_LIGHT)

    def applySkin(self, skin: FluentSkin):
        # the skin applies the theme, the accent color and the surface tint,
        # and paints the background of this window with the tinted colors
        skin.apply(self)
        self.currentSkin = skin
        self.demoInterface.setCurrentSkin(skin)

    def showCustomSkinDialog(self):
        dialog = CustomSkinDialog(self.currentSkin, self)
        if dialog.exec():
            self.applySkin(dialog.customSkin())


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    sys.exit(app.exec_())
