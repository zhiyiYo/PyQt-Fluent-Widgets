# coding:utf-8
from config import cfg, HELP_URL, FEEDBACK_URL, AUTHOR, VERSION, YEAR
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, FolderListSettingCard,
                            OptionsSettingCard, RangeSettingCard, PushSettingCard,
                            ColorSettingCard, HyperlinkCard, PrimaryPushSettingCard, ScrollArea,
                            ExpandLayout, setStyleSheet, ToastToolTip)
from qfluentwidgets import SettingIconFactory as SIF
from PySide6.QtCore import Qt, Signal, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget, QLabel, QFontDialog, QFileDialog


class SettingInterface(ScrollArea):
    """ Setting interface """

    checkUpdateSig = Signal()
    musicFoldersChanged = Signal(list)
    acrylicEnableChanged = Signal(bool)
    downloadFolderChanged = Signal(str)
    minimizeToTrayChanged = Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel("Settings", self)

        # music folders
        self.musicInThisPCGroup = SettingCardGroup(
            "Music on this PC", self.scrollWidget)
        self.musicFolderCard = FolderListSettingCard(
            cfg.musicFolders,
            "Local music library",
            parent=self.musicInThisPCGroup
        )
        self.downloadFolderCard = PushSettingCard(
            'Choose folder',
            SIF.create(SIF.DOWNLOAD),
            "Download Directory",
            cfg.get(cfg.downloadFolder),
            self.musicInThisPCGroup
        )

        # personalization
        self.personalGroup = SettingCardGroup('Personalization', self.scrollWidget)
        self.enableAcrylicCard = SwitchSettingCard(
            SIF.create(SIF.TRANSPARENT),
            "Use Acrylic effect",
            "Acrylic effect has better visual experience, but it may cause the window to become stuck",
            configItem=cfg.enableAcrylicBackground,
            parent=self.personalGroup
        )
        self.themeCard = OptionsSettingCard(
            cfg.themeMode,
            SIF.create(SIF.BRUSH),
            'Application theme',
            "Change the appearance of your application",
            texts=[
                'Light', 'Dark',
                'Use system setting'
            ],
            parent=self.personalGroup
        )
        self.zoomCard = OptionsSettingCard(
            cfg.dpiScale,
            SIF.create(SIF.ZOOM),
            "Interface zoom",
            "Change the size of widgets and fonts",
            texts=[
                "100%", "125%", "150%", "175%", "200%",
                "Use system setting"
            ],
            parent=self.personalGroup
        )

        # online music
        self.onlineMusicGroup = SettingCardGroup('Online Music', self.scrollWidget)
        self.onlinePageSizeCard = RangeSettingCard(
            cfg.onlinePageSize,
            SIF.create(SIF.SEARCH),
            "Number of online music displayed on each page",
            parent=self.onlineMusicGroup
        )
        self.onlineMusicQualityCard = OptionsSettingCard(
            cfg.onlineSongQuality,
            SIF.create(SIF.MUSIC),
            'Online music quality',
            texts=[
                'Standard quality', 'High quality',
                'Super quality', 'Lossless quality'
            ],
            parent=self.onlineMusicGroup
        )
        self.onlineMvQualityCard = OptionsSettingCard(
            cfg.onlineMvQuality,
            SIF.create(SIF.VIDEO),
            'Online MV quality',
            texts=[
                'Full HD', 'HD',
                'SD', 'LD'
            ],
            parent=self.onlineMusicGroup
        )

        # desktop lyric
        self.deskLyricGroup = SettingCardGroup('Desktop Lyric', self.scrollWidget)
        self.deskLyricFontCard = PushSettingCard(
            'Choose font',
            SIF.create(SIF.FONT),
            'Font',
            parent=self.deskLyricGroup
        )
        self.deskLyricHighlightColorCard = ColorSettingCard(
            cfg.deskLyricHighlightColor,
            SIF.create(SIF.PALETTE),
            'Foreground color',
            parent=self.deskLyricGroup
        )
        self.deskLyricStrokeColorCard = ColorSettingCard(
            cfg.deskLyricStrokeColor,
            SIF.create(SIF.PENCIL_INK),
            'Stroke color',
            parent=self.deskLyricGroup
        )
        self.deskLyricStrokeSizeCard = RangeSettingCard(
            cfg.deskLyricStrokeSize,
            SIF.create(SIF.FLUORESCENT_PEN),
            'Stroke size',
            parent=self.deskLyricGroup
        )
        self.deskLyricAlignmentCard = OptionsSettingCard(
            cfg.deskLyricAlignment,
            SIF.create(SIF.ALIGNMENT),
            'Alignment',
            texts=[
                'Center aligned', 'Left aligned',
                'Right aligned'
            ],
            parent=self.deskLyricGroup
        )

        # main panel
        self.mainPanelGroup = SettingCardGroup('Main Panel', self.scrollWidget)
        self.minimizeToTrayCard = SwitchSettingCard(
            SIF.create(SIF.MINIMIZE),
            'Minimize to tray after closing',
            'PyQt Fluent Widgets will continue to run in the background',
            configItem=cfg.minimizeToTray,
            parent=self.mainPanelGroup
        )

        # update software
        self.updateSoftwareGroup = SettingCardGroup("Software update", self.scrollWidget)
        self.updateOnStartUpCard = SwitchSettingCard(
            SIF.create(SIF.UPDATE),
            'Check for updates when the application starts',
            'The new version will be more stable and have more features',
            configItem=cfg.checkUpdateAtStartUp,
            parent=self.updateSoftwareGroup
        )

        # application
        self.aboutGroup = SettingCardGroup('About', self.scrollWidget)
        self.helpCard = HyperlinkCard(
            HELP_URL,
            'Open help page',
            SIF.create(SIF.HELP),
            'Help',
            'Discover new features and learn useful tips about PyQt-Fluent-Widgets',
            self.aboutGroup
        )
        self.feedbackCard = PrimaryPushSettingCard(
            'Provide feedback',
            SIF.create(SIF.FEEDBACK),
            'Provide feedback',
            'Help us improve PyQt Fluent Widgets by providing feedback',
            self.aboutGroup
        )
        self.aboutCard = PrimaryPushSettingCard(
            'Check update',
            SIF.create(SIF.INFO),
            'About',
            '© ' + 'Copyright' + f" {YEAR}, {AUTHOR}. " +
            'Version' + f" {VERSION[1:]}",
            self.aboutGroup
        )

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 120, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        setStyleSheet(self, 'setting_interface')

        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(60, 63)

        # add cards to group
        self.musicInThisPCGroup.addSettingCard(self.musicFolderCard)
        self.musicInThisPCGroup.addSettingCard(self.downloadFolderCard)

        self.personalGroup.addSettingCard(self.enableAcrylicCard)
        self.personalGroup.addSettingCard(self.themeCard)
        self.personalGroup.addSettingCard(self.zoomCard)

        self.onlineMusicGroup.addSettingCard(self.onlinePageSizeCard)
        self.onlineMusicGroup.addSettingCard(self.onlineMusicQualityCard)
        self.onlineMusicGroup.addSettingCard(self.onlineMvQualityCard)

        self.deskLyricGroup.addSettingCard(self.deskLyricFontCard)
        self.deskLyricGroup.addSettingCard(self.deskLyricHighlightColorCard)
        self.deskLyricGroup.addSettingCard(self.deskLyricStrokeColorCard)
        self.deskLyricGroup.addSettingCard(self.deskLyricStrokeSizeCard)
        self.deskLyricGroup.addSettingCard(self.deskLyricAlignmentCard)

        self.updateSoftwareGroup.addSettingCard(self.updateOnStartUpCard)

        self.mainPanelGroup.addSettingCard(self.minimizeToTrayCard)

        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.feedbackCard)
        self.aboutGroup.addSettingCard(self.aboutCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(60, 10, 60, 0)
        self.expandLayout.addWidget(self.musicInThisPCGroup)
        self.expandLayout.addWidget(self.personalGroup)
        self.expandLayout.addWidget(self.onlineMusicGroup)
        self.expandLayout.addWidget(self.deskLyricGroup)
        self.expandLayout.addWidget(self.mainPanelGroup)
        self.expandLayout.addWidget(self.updateSoftwareGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def __showRestartTooltip(self):
        """ show restart tooltip """
        w = ToastToolTip(
            self.tr('Configuration updated successfully'),
            self.tr('Configuration takes effect after restart'),
            'info',
            self.window()
        )
        w.show()

    def __onDeskLyricFontCardClicked(self):
        """ desktop lyric font button clicked slot """
        font, isOk = QFontDialog.getFont(
            cfg.desktopLyricFont, self.window(), "Choose Font")
        if isOk:
            cfg.desktopLyricFont = font

    def __onDownloadFolderCardClicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(
            self, "Choose folder", "./")
        if not folder or cfg.get(cfg.downloadFolder) == folder:
            return

        cfg.set(cfg.downloadFolder, folder)
        self.downloadFolderCard.setContent(folder)

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        cfg.appRestartSig.connect(self.__showRestartTooltip)

        # music in the pc
        self.musicFolderCard.folderChanged.connect(
            self.musicFoldersChanged)
        self.downloadFolderCard.clicked.connect(
            self.__onDownloadFolderCardClicked)

        # personalization
        self.enableAcrylicCard.checkedChanged.connect(
            self.acrylicEnableChanged)

        # playing interface
        self.deskLyricFontCard.clicked.connect(self.__onDeskLyricFontCardClicked)

        # main panel
        self.minimizeToTrayCard.checkedChanged.connect(
            self.minimizeToTrayChanged)

        # about
        self.aboutCard.clicked.connect(self.checkUpdateSig)
        self.feedbackCard.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))
