# coding:utf-8
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QAction


from .acrylic_menu import AcrylicMenuBase, AcrylicMenuActionListWidget
from .acrylic_line_edit import AcrylicLineEditBase
from ..widgets.combo_box import ComboBoxMenu, ComboBox, EditableComboBox
from ..widgets.menu import MenuAnimationType, RoundMenu, IndicatorMenuItemDelegate
from ..settings import SettingCard
from ...common.config import OptionsConfigItem, qconfig


class AcrylicComboMenuActionListWidget(AcrylicMenuActionListWidget):

    def _topMargin(self):
        return 2


class AcrylicComboBoxMenu(AcrylicMenuBase, RoundMenu):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setUpMenu(AcrylicComboMenuActionListWidget(self))

        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.view.setItemDelegate(IndicatorMenuItemDelegate())
        self.view.setObjectName('comboListWidget')
        self.setItemHeight(33)


class AcrylicComboBox(ComboBox):
    """ Acrylic combo box """

    def _createComboMenu(self):
        return AcrylicComboBoxMenu(self)


class AcrylicEditableComboBox(AcrylicLineEditBase, EditableComboBox):
    """ Acrylic combo box """

    def _createComboMenu(self):
        return AcrylicComboBoxMenu(self)


class AcrylicComboBoxSettingCard(SettingCard):
    """ Setting card with a combo box """

    def __init__(self, configItem: OptionsConfigItem, icon, title, content=None, texts=None, parent=None):
        """
        Parameters
        ----------
        configItem: OptionsConfigItem
            configuration item operated by the card

        icon: str | QIcon | FluentIconBase
            the icon to be drawn

        title: str
            the title of card

        content: str
            the content of card

        texts: List[str]
            the text of items

        parent: QWidget
            parent widget
        """
        super().__init__(icon, title, content, parent)
        self.configItem = configItem
        self.comboBox = AcrylicComboBox(self)
        self.hBoxLayout.addWidget(self.comboBox, 0, Qt.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.optionToText = {o: t for o, t in zip(configItem.options, texts)}
        for text, option in zip(texts, configItem.options):
            self.comboBox.addItem(text, userData=option)

        self.comboBox.setCurrentText(self.optionToText[qconfig.get(configItem)])
        self.comboBox.currentIndexChanged.connect(self._onCurrentIndexChanged)
        configItem.valueChanged.connect(self.setValue)

    def _onCurrentIndexChanged(self, index: int):
        qconfig.set(self.configItem, self.comboBox.itemData(index))

    def setValue(self, value):
        if value not in self.optionToText:
            return

        self.comboBox.setCurrentText(self.optionToText[value])
        qconfig.set(self.configItem, value)