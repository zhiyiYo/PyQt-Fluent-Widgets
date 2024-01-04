# coding:utf-8
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QListWidgetItem, QFrame, QTreeWidgetItem, QHBoxLayout,
                             QTreeWidgetItemIterator, QTableWidgetItem)
from qfluentwidgets import TreeWidget, TableWidget, ListWidget, HorizontalFlipView

from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from ..common.style_sheet import StyleSheet


class ViewInterface(GalleryInterface):
    """ View interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.view,
            subtitle="qfluentwidgets.components.widgets",
            parent=parent
        )
        self.setObjectName('viewInterface')

        # list view
        self.addExampleCard(
            title=self.tr('A simple ListView'),
            widget=ListFrame(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/view/list_view/demo.py'
        )

        # table view
        self.addExampleCard(
            title=self.tr('A simple TableView'),
            widget=TableFrame(self),
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/view/table_view/demo.py'
        )

        # tree view
        frame = TreeFrame(self)
        self.addExampleCard(
            title=self.tr('A simple TreeView'),
            widget=frame,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/view/tree_view/demo.py'
        )

        frame = TreeFrame(self, True)
        self.addExampleCard(
            title=self.tr('A TreeView with Multi-selection enabled'),
            widget=frame,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/view/tree_view/demo.py'
        )

        # flip view
        w = HorizontalFlipView(self)
        w.addImages([
            ":/gallery/images/Shoko1.jpg",
            ":/gallery/images/Shoko2.jpg",
            ":/gallery/images/Shoko3.jpg",
            ":/gallery/images/Shoko4.jpg",
        ])
        self.addExampleCard(
            title=self.tr('Flip view'),
            widget=w,
            sourcePath='https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/view/flip_view/demo.py'
        )


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 8, 0, 0)

        self.setObjectName('frame')
        StyleSheet.VIEW_INTERFACE.apply(self)

    def addWidget(self, widget):
        self.hBoxLayout.addWidget(widget)


class ListFrame(Frame):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.listWidget = ListWidget(self)
        self.addWidget(self.listWidget)

        stands = [
            self.tr("Star Platinum"), self.tr("Hierophant Green"),
            self.tr("Made in Haven"), self.tr("King Crimson"),
            self.tr("Silver Chariot"), self.tr("Crazy diamond"),
            self.tr("Metallica"), self.tr("Another One Bites The Dust"),
            self.tr("Heaven's Door"), self.tr("Killer Queen"),
            self.tr("The Grateful Dead"), self.tr("Stone Free"),
            self.tr("The World"), self.tr("Sticky Fingers"),
            self.tr("Ozone Baby"), self.tr("Love Love Deluxe"),
            self.tr("Hermit Purple"), self.tr("Gold Experience"),
            self.tr("King Nothing"), self.tr("Paper Moon King"),
            self.tr("Scary Monster"), self.tr("Mandom"),
            self.tr("20th Century Boy"), self.tr("Tusk Act 4"),
            self.tr("Ball Breaker"), self.tr("Sex Pistols"),
            self.tr("D4C • Love Train"), self.tr("Born This Way"),
            self.tr("SOFT & WET"), self.tr("Paisley Park"),
            self.tr("Wonder of U"), self.tr("Walking Heart"),
            self.tr("Cream Starter"), self.tr("November Rain"),
            self.tr("Smooth Operators"), self.tr("The Matte Kudasai")
        ]
        for stand in stands:
            self.listWidget.addItem(QListWidgetItem(stand))

        self.setFixedSize(300, 380)


class TreeFrame(Frame):

    def __init__(self, parent=None, enableCheck=False):
        super().__init__(parent)
        self.tree = TreeWidget(self)
        self.addWidget(self.tree)

        item1 = QTreeWidgetItem([self.tr('JoJo 1 - Phantom Blood')])
        item1.addChildren([
            QTreeWidgetItem([self.tr('Jonathan Joestar')]),
            QTreeWidgetItem([self.tr('Dio Brando')]),
            QTreeWidgetItem([self.tr('Will A. Zeppeli')]),
        ])
        self.tree.addTopLevelItem(item1)

        item2 = QTreeWidgetItem([self.tr('JoJo 3 - Stardust Crusaders')])
        item21 = QTreeWidgetItem([self.tr('Jotaro Kujo')])
        item21.addChildren([
            QTreeWidgetItem(['Jotaro Kujo']),
            QTreeWidgetItem(['Empty Banana Wolf']),
            QTreeWidgetItem(['Aqiag']),
            QTreeWidgetItem(['Selling Fish']),
            QTreeWidgetItem(['The Invincible Man']),
        ])
        item2.addChild(item21)
        self.tree.addTopLevelItem(item2)
        self.tree.expandAll()
        self.tree.setHeaderHidden(True)

        self.setFixedSize(300, 380)

        if enableCheck:
            it = QTreeWidgetItemIterator(self.tree)
            while(it.value()):
                it.value().setCheckState(0, Qt.Unchecked)
                it += 1


class TableFrame(TableWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.verticalHeader().hide()
        self.setBorderRadius(8)
        self.setBorderVisible(True)

        self.setColumnCount(5)
        self.setRowCount(60)
        self.setHorizontalHeaderLabels([
            self.tr('Title'), self.tr('Artist'), self.tr('Album'),
            self.tr('Year'), self.tr('Duration')
        ])
        songInfos = [
             ['bag', 'aiko', 'bag', '2004', '5:04'],
             ['Love You', 'Wang Xinling', 'Love You', '2004', '3:39'],
             ['A world without stars', 'aiko', 'A world without stars/profile', '2007', '5:30'],
             ['Profile', 'aiko', 'Starless World/Profile', '2007', '5:06'],
             ['secret', 'aiko', 'secret', '2008', '6:27'],
             ['Shiawase', 'aiko', 'Secret', '2008', '5:25'],
             ['two people', 'aiko', 'two people', '2008', '5:00'],
             ['Sparkle', 'RADWIMPS', 'Your Name. ', '2016', '8:54'],
             ['Nothing', 'RADWIMPS', 'Your Name. ', '2016', '3:16'],
             ['Pre-Zen Pre-Life', 'RADWIMPS', 'Human Flowering', '2016', '4:35'],
             ['I fell in love', 'aiko', 'I fell in love', '2016', '6:02'],
             ['Summer fatigue', 'aiko', 'Koi shita wa', '2016', '4:41'],
             ['more', 'aiko', 'more', '2016', '4:50'],
             ['Question set', 'aiko', 'more', '2016', '4:18'],
             ['short sleeve', 'aiko', 'more', '2016', '5:50'],
             ['Hinekure', 'Chainana', 'Hush a by little girl', '2017', '3:54'],
             ['Stern', 'Kashina', 'Hush a by little girl', '2017', '3:16'],
             ['Love is selfish', 'aiko', 'The beginning of a humid summer', '2018', '5:31'],
             ['Drive Mode', 'aiko', 'Wet Summer Start', '2018', '3:37'],
             ['Yeah. ', 'aiko', 'The beginning of humid summer', '2018', '5:48'],
             ['Glitter', 'aiko\'s poem. ', '2019', '5:08', 'aiko'],
             ['Super Ball of Love', 'aiko', 'aiko\'s poem. ', '2019', '4:31'],
             ['Magnet', 'aiko', 'I can\'t tell you what happened', '2021', '4:24'],
             ['Ai ate', 'aiko', 'Ai ate/us', '2021', '5:17'],
             ['Train', 'aiko', 'I ate love/us', '2021', '4:18'],
             ['Flower Tower', 'Sayuri', 'Flower Tower', '2022', '4:35'],
             ['Summer Love Life', 'aiko', 'Summer Love Life', '2022', '5:03'],
             ['Aka Toki Reload', 'aiko', 'Aka Toki Reload', '2023', '4:04'],
             ['Chapped lips make love disappear', 'aiko', 'The two of us are looking at each other now', '2023', '4:07'],
             ['One Two Three', 'aiko', 'We are looking at each other now', '2023', '4:47'],
         ]
        songInfos += songInfos
        for i, songInfo in enumerate(songInfos):
            for j in range(5):
                self.setItem(i, j, QTableWidgetItem(songInfo[j]))

        self.setFixedSize(625, 440)
        self.resizeColumnsToContents()
