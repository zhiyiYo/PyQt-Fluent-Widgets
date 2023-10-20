# coding:utf-8
from PySide6.QtCore import Qt, QEasingCurve
from PySide6.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QSizePolicy
from qfluentwidgets import (Pivot, qrouter, SegmentedWidget, TabBar, CheckBox, ComboBox,
                            TabCloseButtonDisplayMode, BodyLabel, SpinBox, BreadcrumbBar,
                            SegmentedToggleToolWidget, FluentIcon)

from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from ..common.style_sheet import StyleSheet


class NavigationViewInterface(GalleryInterface):
    """ Navigation view interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.navigation,
            subtitle="qfluentwidgets.components.navigation",
            parent=parent
        )
        self.setObjectName('navigationViewInterface')

        # breadcrumb bar
        breadcrumb = BreadcrumbBar(self)
        items = [
            self.tr("Home"), self.tr("Documents"), self.tr("Study"),
            self.tr("Janpanese Sensei"), self.tr("Action Film"), self.tr("G Cup"),
            self.tr("Mikami Yua"), self.tr("Folder1"), self.tr("Folder2"),
        ]
        for i in items:
            breadcrumb.addItem(i, i)

        self.addExampleCard(
            title=self.tr('Breadcrumb bar'),
            widget=breadcrumb,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/navigation/breadcrumb_bar/demo.py',
            stretch=1
        )

        self.addExampleCard(
            title=self.tr('A basic pivot'),
            widget=PivotInterface(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/navigation/pivot/demo.py'
        )

        self.addExampleCard(
            title=self.tr('A segmented control'),
            widget=SegmentedInterface(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/navigation/segmented_widget/demo.py'
        )

        self.addExampleCard(
            title=self.tr('Another segmented control'),
            widget=self.createToggleToolWidget(),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/navigation/segmented_tool_widget/demo.py'
        )

        card = self.addExampleCard(
            title=self.tr('A tab bar'),
            widget=TabInterface(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/PySide6/examples/navigation/tab_view/demo.py',
            stretch=1
        )
        card.topLayout.setContentsMargins(12, 0, 0, 0)

    def createToggleToolWidget(self):
        w = SegmentedToggleToolWidget(self)
        w.addItem('k1', FluentIcon.TRANSPARENT)
        w.addItem('k2', FluentIcon.CHECKBOX)
        w.addItem('k3', FluentIcon.CONSTRACT)
        w.setCurrentItem('k1')
        return w


class PivotInterface(QWidget):
    """ Pivot interface """

    Nav = Pivot

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(300, 140)

        self.pivot = self.Nav(self)
        self.stackedWidget = QStackedWidget(self)
        self.vBoxLayout = QVBoxLayout(self)

        self.songInterface = QLabel('Song Interface', self)
        self.albumInterface = QLabel('Album Interface', self)
        self.artistInterface = QLabel('Artist Interface', self)

        # add items to pivot
        self.addSubInterface(self.songInterface, 'songInterface', self.tr('Song'))
        self.addSubInterface(self.albumInterface, 'albumInterface', self.tr('Album'))
        self.addSubInterface(self.artistInterface, 'artistInterface', self.tr('Artist'))

        self.vBoxLayout.addWidget(self.pivot, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        StyleSheet.NAVIGATION_VIEW_INTERFACE.apply(self)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.stackedWidget.setCurrentWidget(self.songInterface)
        self.pivot.setCurrentItem(self.songInterface.objectName())

        qrouter.setDefaultRouteKey(self.stackedWidget, self.songInterface.objectName())

    def addSubInterface(self, widget: QLabel, objectName, text):
        widget.setObjectName(objectName)
        widget.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.stackedWidget.addWidget(widget)
        self.pivot.addItem(
            routeKey=objectName,
            text=text,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        self.pivot.setCurrentItem(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())


class SegmentedInterface(PivotInterface):

    Nav = SegmentedWidget

    def __init__(self, parent=None):
        super().__init__(parent)
        self.vBoxLayout.removeWidget(self.pivot)
        self.vBoxLayout.insertWidget(0, self.pivot)


class TabInterface(QWidget):
    """ Tab interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.tabCount = 1

        self.tabBar = TabBar(self)
        self.stackedWidget = QStackedWidget(self)
        self.tabView = QWidget(self)
        self.controlPanel = QFrame(self)

        self.movableCheckBox = CheckBox(self.tr('IsTabMovable'), self)
        self.scrollableCheckBox = CheckBox(self.tr('IsTabScrollable'), self)
        self.shadowEnabledCheckBox = CheckBox(self.tr('IsTabShadowEnabled'), self)
        self.tabMaxWidthLabel = BodyLabel(self.tr('TabMaximumWidth'), self)
        self.tabMaxWidthSpinBox = SpinBox(self)
        self.closeDisplayModeLabel = BodyLabel(self.tr('TabCloseButtonDisplayMode'), self)
        self.closeDisplayModeComboBox = ComboBox(self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout(self.tabView)
        self.panelLayout = QVBoxLayout(self.controlPanel)

        self.songInterface = QLabel('Song Interface', self)
        self.albumInterface = QLabel('Album Interface', self)
        self.artistInterface = QLabel('Artist Interface', self)

        # add items to pivot
        self.__initWidget()

    def __initWidget(self):
        self.initLayout()

        self.shadowEnabledCheckBox.setChecked(True)

        self.tabMaxWidthSpinBox.setRange(60, 400)
        self.tabMaxWidthSpinBox.setValue(self.tabBar.tabMaximumWidth())

        self.closeDisplayModeComboBox.addItem(self.tr('Always'), userData=TabCloseButtonDisplayMode.ALWAYS)
        self.closeDisplayModeComboBox.addItem(self.tr('OnHover'), userData=TabCloseButtonDisplayMode.ON_HOVER)
        self.closeDisplayModeComboBox.addItem(self.tr('Never'), userData=TabCloseButtonDisplayMode.NEVER)
        self.closeDisplayModeComboBox.currentIndexChanged.connect(self.onDisplayModeChanged)

        self.addSubInterface(self.songInterface,
                             'tabSongInterface', self.tr('Song'), ':/gallery/images/MusicNote.png')
        self.addSubInterface(self.albumInterface,
                             'tabAlbumInterface', self.tr('Album'), ':/gallery/images/Dvd.png')
        self.addSubInterface(self.artistInterface,
                             'tabArtistInterface', self.tr('Artist'), ':/gallery/images/Singer.png')

        self.controlPanel.setObjectName('controlPanel')
        StyleSheet.NAVIGATION_VIEW_INTERFACE.apply(self)

        self.connectSignalToSlot()

        qrouter.setDefaultRouteKey(
            self.stackedWidget, self.songInterface.objectName())

    def connectSignalToSlot(self):
        self.movableCheckBox.stateChanged.connect(
            lambda: self.tabBar.setMovable(self.movableCheckBox.isChecked()))
        self.scrollableCheckBox.stateChanged.connect(
            lambda: self.tabBar.setScrollable(self.scrollableCheckBox.isChecked()))
        self.shadowEnabledCheckBox.stateChanged.connect(
            lambda: self.tabBar.setTabShadowEnabled(self.shadowEnabledCheckBox.isChecked()))

        self.tabMaxWidthSpinBox.valueChanged.connect(self.tabBar.setTabMaximumWidth)

        self.tabBar.tabAddRequested.connect(self.addTab)
        self.tabBar.tabCloseRequested.connect(self.removeTab)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)

    def initLayout(self):
        self.tabBar.setTabMaximumWidth(200)

        self.setFixedHeight(280)
        self.controlPanel.setFixedWidth(220)
        self.hBoxLayout.addWidget(self.tabView, 1)
        self.hBoxLayout.addWidget(self.controlPanel, 0, Qt.AlignRight)
        self.hBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.tabBar)
        self.vBoxLayout.addWidget(self.stackedWidget)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.panelLayout.setSpacing(8)
        self.panelLayout.setContentsMargins(14, 16, 14, 14)
        self.panelLayout.setAlignment(Qt.AlignTop)

        self.panelLayout.addWidget(self.movableCheckBox)
        self.panelLayout.addWidget(self.scrollableCheckBox)
        self.panelLayout.addWidget(self.shadowEnabledCheckBox)

        self.panelLayout.addSpacing(4)
        self.panelLayout.addWidget(self.tabMaxWidthLabel)
        self.panelLayout.addWidget(self.tabMaxWidthSpinBox)

        self.panelLayout.addSpacing(4)
        self.panelLayout.addWidget(self.closeDisplayModeLabel)
        self.panelLayout.addWidget(self.closeDisplayModeComboBox)

    def addSubInterface(self, widget: QLabel, objectName, text, icon):
        widget.setObjectName(objectName)
        widget.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.stackedWidget.addWidget(widget)
        self.tabBar.addTab(
            routeKey=objectName,
            text=text,
            icon=icon,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onDisplayModeChanged(self, index):
        mode = self.closeDisplayModeComboBox.itemData(index)
        self.tabBar.setCloseButtonDisplayMode(mode)

    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        if not widget:
            return

        self.tabBar.setCurrentTab(widget.objectName())
        qrouter.push(self.stackedWidget, widget.objectName())

    def addTab(self):
        text = f'硝子酱一级棒卡哇伊×{self.tabCount}'
        self.addSubInterface(QLabel('🥰 ' + text), text, text, ':/gallery/images/Smiling_with_heart.png')
        self.tabCount += 1

    def removeTab(self, index):
        item = self.tabBar.tabItem(index)
        widget = self.findChild(QLabel, item.routeKey())

        self.stackedWidget.removeWidget(widget)
        self.tabBar.removeTab(index)
        widget.deleteLater()