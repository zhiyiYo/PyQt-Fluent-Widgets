# coding:utf-8
#import sys
from pathlib import Path
from enum import Enum

##sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon
from qfluentwidgets import (FluentWindow, setTheme, Theme, isDarkTheme,
    InfoBar, InfoBarPosition, ExpandLayout, ScrollArea, SettingCardGroup,
    SwitchSettingCard, OptionsSettingCard, PrimaryPushSettingCard, HyperlinkCard,
    setFont, TeachingTip, TeachingTipTailPosition, InfoBarIcon,
    OptionsConfigItem, OptionsValidator, EnumSerializer, qconfig, FluentIcon as FIF)

class WindowEffect(Enum):
    DISABLED = "disabled"
    MICA = "mica"
    MICA_ALT = "mica_alt"
    ACRYLIC = "acrylic"
    DWM_BLUR = "dwm_blur"

class WindowEffectInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)
        self.currentEffect = WindowEffect.DISABLED
        self.titleLabel = QLabel(self.tr("Window Effects"), self)
        
        self.effectGroup = SettingCardGroup(self.tr("Material"), self.scrollWidget)
        self.windowEffectConfig = OptionsConfigItem(
            "WindowEffect", "effect", WindowEffect.DISABLED,
            OptionsValidator(WindowEffect), EnumSerializer(WindowEffect), restart=False)
        self.effectCard = OptionsSettingCard(
            self.windowEffectConfig, FIF.TRANSPARENT,
            self.tr("Window effect"), self.tr("Choose the window transparency effect"),
            texts=[self.tr("Disabled"), self.tr("Mica"), self.tr("Mica Alt"), 
                   self.tr("Acrylic"), self.tr("DWM Blur")],
            parent=self.effectGroup)
        
        self.personalGroup = SettingCardGroup(self.tr("Personalization"), self.scrollWidget)
        self.themeCard = SwitchSettingCard(
            FIF.CONSTRACT, self.tr("Dark theme"),
            self.tr("Switch between light and dark theme (Window Effects performs better in dark theme)"),
            configItem=None, parent=self.personalGroup)
        self.themeCard.setChecked(isDarkTheme())
        
        self.aboutGroup = SettingCardGroup(self.tr("System Information"), self.scrollWidget)
        build = sys.getwindowsversion().build if sys.platform == 'win32' else 0
        osVer = self._getWindowsVersion(build)
        self.systemCard = PrimaryPushSettingCard(
            self.tr("View details"), FIF.DEVELOPER_TOOLS, self.tr("System"),
            f"{osVer} (Build {build})", self.aboutGroup)
        self.compatCard = HyperlinkCard(
            "https://learn.microsoft.com/windows/apps/design/signature-experiences/materials",
            self.tr("Learn more"), FIF.INFO, self.tr("Compatibility"),
            self.tr("Check Windows version requirements for each effect"), self.aboutGroup)
        
        self.__initWidget()
        self.__initLayout()
        self.__connectSignalToSlot()
    
    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('windowEffectInterface')
        self.scrollWidget.setObjectName('scrollWidget')
        self.titleLabel.setObjectName('settingLabel')
        
        self.setStyleSheet("""
            WindowEffectInterface, #scrollWidget { background-color: transparent; }
            QScrollArea { background-color: transparent; border: none; }
        """)
        
        color = "rgb(255, 255, 255)" if isDarkTheme() else "rgb(0, 0, 0)"
        self.titleLabel.setStyleSheet(f"""
            QLabel#settingLabel {{
                color: {color}; background-color: transparent;
                font: 33px 'Segoe UI', 'Microsoft YaHei Light';
            }}""")
        setFont(self.titleLabel, 33)
    
    def __initLayout(self):
        self.titleLabel.move(36, 30)
        self.effectGroup.addSettingCard(self.effectCard)
        self.personalGroup.addSettingCard(self.themeCard)
        self.aboutGroup.addSettingCard(self.systemCard)
        self.aboutGroup.addSettingCard(self.compatCard)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.effectGroup)
        self.expandLayout.addWidget(self.personalGroup)
        self.expandLayout.addWidget(self.aboutGroup)
    
    def __connectSignalToSlot(self):
        self.effectCard.optionChanged.connect(self._onEffectChanged)
        self.themeCard.checkedChanged.connect(self._onThemeChanged)
        self.systemCard.clicked.connect(self._onSystemCardClicked)
    
    def _onEffectChanged(self, item):
        effect = qconfig.get(item)
        if not isinstance(effect, WindowEffect):
            texts = {"Disabled": WindowEffect.DISABLED, "Mica": WindowEffect.MICA,
                     "Mica Alt": WindowEffect.MICA_ALT, "Acrylic": WindowEffect.ACRYLIC,
                     "DWM Blur": WindowEffect.DWM_BLUR}
            for button in self.effectCard.buttonGroup.buttons():
                if button.isChecked():
                    effect = texts.get(button.text(), WindowEffect.DISABLED)
                    break
        self.currentEffect = effect
        parent = self.window()
        if isinstance(parent, FluentWindow):
            self._clearAllEffects(parent)
            QTimer.singleShot(100, lambda: self._applyEffect(parent, effect))
    
    def _clearAllEffects(self, window):
        window.setMicaEffectEnabled(False)
        window.setMicaAltEffectEnabled(False)
        window.setAcrylicEffectEnabled(False)
        window.setDwmBlurEffectEnabled(False)
    
    def _applyEffect(self, window, effect):
        if sys.platform != 'win32':
            QTimer.singleShot(100, lambda: self._showIncompatibleWarning("Window effects are only available on Windows"))
            return
        
        build = sys.getwindowsversion().build
        checks = {
            WindowEffect.MICA: (build >= 22000, "Mica", "Windows 11"),
            WindowEffect.MICA_ALT: (build >= 22621, "Mica Alt", "Windows 11 22H2"),
            WindowEffect.ACRYLIC: (build >= 22000, "Acrylic", "Windows 11"),
            WindowEffect.DWM_BLUR: (build >= 7600, "DWM Blur", "Windows 7")
        }
        
        if effect == WindowEffect.DISABLED:
            QTimer.singleShot(100, lambda: self._showSuccessInfo("All effects disabled"))
        elif effect in checks:
            compatible, name, req = checks[effect]
            if compatible:
                getattr(window, f"set{effect.name.title().replace('_', '')}EffectEnabled")(True)
                QTimer.singleShot(100, lambda: self._showSuccessInfo(f"{name} effect applied"))
            else:
                QTimer.singleShot(100, lambda: self._showIncompatibleWarning(f"{name} requires {req} or later"))
    
    def _onThemeChanged(self, checked):
        theme = Theme.DARK if checked else Theme.LIGHT
        setTheme(theme)
        color = "rgb(255, 255, 255)" if checked else "rgb(0, 0, 0)"
        self.titleLabel.setStyleSheet(f"""
            QLabel#settingLabel {{
                color: {color}; background-color: transparent;
                font: 33px 'Segoe UI', 'Microsoft YaHei Light';
            }}""")
        QTimer.singleShot(100, self._reapplyCurrentEffect)
    
    def _reapplyCurrentEffect(self):
        effect = self.currentEffect
        parent = self.window()
        if isinstance(parent, FluentWindow) and effect != WindowEffect.DISABLED:
            self._clearAllEffects(parent)
            QTimer.singleShot(100, lambda: self._applyEffect(parent, effect))
    
    def _onSystemCardClicked(self):
        if sys.platform == 'win32':
            build = sys.getwindowsversion().build
            info = f"{self._getWindowsVersion(build)} (Build {build})\n\n"
            info += "Effect Compatibility:\n"
            info += f"• Mica: {'✓' if build >= 22000 else '✗'} (Windows 11+)\n"
            info += f"• Mica Alt: {'✓' if build >= 22621 else '✗'} (Windows 11 22H2+)\n"
            info += f"• Acrylic: {'✓' if build >= 22000 else '✗'} (Windows 11+)\n"
            info += f"• DWM Blur: {'✓' if build >= 7600 else '✗'} (Windows 7+)"
            
            TeachingTip.create(
                target=self.systemCard.button, icon=InfoBarIcon.INFORMATION,
                title="System Information", content=info,
                isClosable=True, tailPosition=TeachingTipTailPosition.TOP,
                duration=8000, parent=self)
    
    def _showSuccessInfo(self, message):
        parent = self.window()
        if parent and parent.isVisible():
            InfoBar.success(title="Applied", content=message, orient=Qt.Horizontal,
                            isClosable=True, position=InfoBarPosition.TOP,
                            duration=2000, parent=parent)
    
    def _showIncompatibleWarning(self, message):
        parent = self.window()
        if parent and parent.isVisible():
            InfoBar.warning(title="Incompatible", content=message, orient=Qt.Horizontal,
                            isClosable=True, position=InfoBarPosition.TOP,
                            duration=3000, parent=parent)
        self.currentEffect = WindowEffect.DISABLED
        self.effectCard.setValue(WindowEffect.DISABLED)
    
    def _getWindowsVersion(self, build):
        versions = [(26100, "Windows 11 24H2"), (22631, "Windows 11 23H2"),
                    (22621, "Windows 11 22H2"), (22000, "Windows 11"),
                    (19041, "Windows 10"), (7600, "Windows 7+")]
        for b, v in versions:
            if build >= b: return v
        return "Unknown Windows"

class WindowEffectDemo(FluentWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Window Effect Gallery')
        self.setWindowIcon(QIcon(':/qfluentwidgets/images/logo.png'))
        self._effectsInitialized = False
        self.effectInterface = WindowEffectInterface(self)
        self.addSubInterface(self.effectInterface, FIF.TRANSPARENT, 'Window Effects')
        self.resize(900, 700)
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)
        setTheme(Theme.DARK if isDarkTheme() else Theme.LIGHT)
    
    def showEvent(self, event):
        super().showEvent(event)
        if not self._effectsInitialized:
            self._effectsInitialized = True
            QTimer.singleShot(50, self._disableDefaultEffects)
    
    def _disableDefaultEffects(self):
        if sys.platform == 'win32':
            self._isMicaEnabled = self._isMicaAltEnabled = False
            self._isAcrylicEnabled = self._isDwmBlurEnabled = False
            self.windowEffectManager.removeEffect(self.winId())

if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    w = WindowEffectDemo()
    w.show()
    app.exec_()
