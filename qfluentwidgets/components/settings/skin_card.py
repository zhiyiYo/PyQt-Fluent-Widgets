# coding: utf-8
""" the widgets that preview and pick a `FluentSkin` """
from typing import Dict, List, Optional

from PyQt5.QtCore import Qt, QSize, QPointF, QRectF, pyqtSignal
from PyQt5.QtGui import QColor, QFontMetrics, QPainter, QPainterPath, QPen
from PyQt5.QtWidgets import QWidget, QHBoxLayout

from ...common.config import Theme
from ...common.font import setFont
from ...common.skin import FluentSkin, FluentSkinSet
from ...common.style_sheet import themeColor
from ..layout.flow_layout import FlowLayout
from ..dialog_box.message_box_base import MessageBoxBase
from ..widgets.button import RadioButton
from ..widgets.check_box import CheckBox
from ..widgets.label import BodyLabel, CaptionLabel, SubtitleLabel
from ..widgets.slider import Slider
from .setting_card import ColorPickerButton


class SkinCard(QWidget):
    """ A clickable preview of a skin

    The skin is painted as a miniature window: the tinted window background,
    a tinted card, the accent color and a couple of content lines. It makes the
    difference between the skins visible at a glance, which a plain button
    cannot do.

    Examples
    --------
    >>> card = SkinCard(FluentSkinSet.DEEP_OCEAN)
    >>> card.clicked.connect(lambda skin: skin.apply(window))
    """

    clicked = pyqtSignal(object)

    #: size of the preview card
    CARD_SIZE = QSize(128, 76)

    def __init__(self, skin: FluentSkin, parent=None):
        super().__init__(parent)
        self.skin = skin
        self.isSelected = False
        self._isHover = False

        self.setFixedSize(self.CARD_SIZE)
        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_Hover, True)

        setFont(self, 10)

    def setSelected(self, isSelected: bool):
        """ set whether the card is selected """
        if self.isSelected == isSelected:
            return

        self.isSelected = isSelected
        self.update()

    def isDarkPreview(self) -> bool:
        """ whether the preview is painted with a dark window background """
        return self.skin.windowBackgroundColor().lightness() < 128

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        rect = QRectF(self.rect()).adjusted(1.5, 1.5, -1.5, -1.5)
        path = QPainterPath()
        path.addRoundedRect(rect, 6, 6)

        painter.save()
        painter.setClipPath(path)
        painter.fillRect(self.rect(), self.skin.windowBackgroundColor())
        self.__drawPreview(painter)
        painter.restore()

        self.__drawBorder(painter, rect)

        if self.isSelected:
            self.__drawCheckMark(painter)

    def __drawPreview(self, painter: QPainter):
        """ draw the miniature window inside the card """
        dark = self.isDarkPreview()
        lineColor = QColor(255, 255, 255, 90) if dark else QColor(0, 0, 0, 55)

        # the name of the skin sits on the window background
        font = self.font()
        painter.setFont(font)
        painter.setPen(QColor(240, 240, 240) if dark else QColor(32, 32, 32))
        title = QFontMetrics(font).elidedText(self.skin.name, Qt.ElideRight, 112)
        painter.drawText(QRectF(10, 5, 112, 17), Qt.AlignLeft | Qt.AlignVCenter, title)

        # the tinted card
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.skin.surfaceColor())
        painter.drawRoundedRect(QRectF(10, 30, 108, 36), 4, 4)

        # the accent color and the content lines
        painter.setBrush(self.skin.accentColor)
        painter.drawRoundedRect(QRectF(18, 38, 26, 6), 3, 3)

        painter.setBrush(lineColor)
        painter.drawRoundedRect(QRectF(18, 50, 62, 5), 2.5, 2.5)
        painter.drawRoundedRect(QRectF(18, 58, 42, 5), 2.5, 2.5)

    def __drawBorder(self, painter: QPainter, rect: QRectF):
        if self.isSelected:
            pen = QPen(themeColor(), 2)
        elif self._isHover:
            pen = QPen(QColor(0, 0, 0, 45) if not self.isDarkPreview()
                       else QColor(255, 255, 255, 45), 1.5)
        else:
            return

        painter.setPen(pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, 6, 6)

    @staticmethod
    def __relativeLuminance(color: QColor) -> float:
        """ WCAG relative luminance, it decides whether the check mark should
        be dark or light """
        def linearize(value: int) -> float:
            value /= 255
            return value / 12.92 if value <= 0.03928 else ((value + 0.055) / 1.055) ** 2.4

        return (0.2126 * linearize(color.red()) +
                0.7152 * linearize(color.green()) +
                0.0722 * linearize(color.blue()))

    def __drawCheckMark(self, painter: QPainter):
        """ draw a filled circle with a check mark at the top right corner """
        color = themeColor()
        center = QPointF(self.width() - 14, 14)

        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        painter.drawEllipse(center, 7.5, 7.5)

        # a white mark is invisible on a light accent color, so pick the one
        # that contrasts with the accent color
        markColor = Qt.black if self.__relativeLuminance(color) > 0.35 else Qt.white
        painter.setPen(QPen(markColor, 1.6, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        painter.setBrush(Qt.NoBrush)

        check = QPainterPath()
        check.moveTo(center.x() - 3.2, center.y() + 0.2)
        check.lineTo(center.x() - 1.0, center.y() + 2.6)
        check.lineTo(center.x() + 3.4, center.y() - 2.4)
        painter.drawPath(check)

    def enterEvent(self, e):
        self._isHover = True
        self.update()
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._isHover = False
        self.update()
        super().leaveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.rect().contains(e.pos()):
            self.clicked.emit(self.skin)

        super().mouseReleaseEvent(e)


class CustomSkinCard(QWidget):
    """ The card that opens the custom skin dialog """

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._isHover = False

        self.setFixedSize(SkinCard.CARD_SIZE)
        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_Hover, True)

        setFont(self, 10)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)

        rect = QRectF(self.rect()).adjusted(1.5, 1.5, -1.5, -1.5)
        alpha = 160 if self._isHover else 110

        painter.setPen(QPen(QColor(128, 128, 128, alpha), 1.2, Qt.DashLine))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, 6, 6)

        # plus icon
        center = QPointF(rect.center().x(), rect.center().y() - 7)
        painter.setPen(QPen(themeColor(), 2, Qt.SolidLine, Qt.RoundCap))
        painter.drawLine(QPointF(center.x() - 7, center.y()),
                         QPointF(center.x() + 7, center.y()))
        painter.drawLine(QPointF(center.x(), center.y() - 7),
                         QPointF(center.x(), center.y() + 7))

        # label
        painter.setFont(self.font())
        painter.setPen(QColor(140, 140, 140))
        painter.drawText(QRectF(rect.left(), center.y() + 8, rect.width(), 20),
                         Qt.AlignCenter, self.tr('Custom…'))

    def enterEvent(self, e):
        self._isHover = True
        self.update()
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._isHover = False
        self.update()
        super().leaveEvent(e)

    def mouseReleaseEvent(self, e):
        if e.button() == Qt.LeftButton and self.rect().contains(e.pos()):
            self.clicked.emit()

        super().mouseReleaseEvent(e)


class CustomSkinDialog(MessageBoxBase):
    """ A dialog that derives a new skin from an existing one

    A skin is just a bundle of theme settings, so the dialog edits the fields
    of the given skin and returns a copy of it in `customSkin()`.
    """

    def __init__(self, skin: FluentSkin, parent=None):
        super().__init__(parent)
        self.skin = skin
        self.titleLabel = SubtitleLabel(self.tr('Custom skin'), self)

        # base theme
        self.lightRadioButton = RadioButton(self.tr('Light'), self)
        self.darkRadioButton = RadioButton(self.tr('Dark'), self)
        if skin.theme == Theme.DARK:
            self.darkRadioButton.setChecked(True)
        else:
            self.lightRadioButton.setChecked(True)

        # accent color
        self.accentButton = ColorPickerButton(skin.accentColor, self.tr('Accent color'), self)

        # surface tint
        self.tintEnabledBox = CheckBox(self.tr('Enable surface tint'), self)
        self.tintEnabledBox.setChecked(skin.isTintEnabled)
        tint = skin.surfaceTint if skin.surfaceTint.isValid() else QColor('#3A2D12')
        self.tintButton = ColorPickerButton(tint, self.tr('Surface tint'), self)
        self.tintButton.setEnabled(skin.isTintEnabled)
        self.tintEnabledBox.toggled.connect(self.tintButton.setEnabled)

        # tint strength
        self.strengthSlider = Slider(Qt.Horizontal, self)
        self.strengthSlider.setRange(0, 100)
        self.strengthSlider.setValue(int(skin.surfaceTintStrength * 100))
        self.strengthLabel = CaptionLabel(f'{skin.surfaceTintStrength:.2f}', self)
        self.strengthSlider.valueChanged.connect(
            lambda value: self.strengthLabel.setText(f'{value / 100:.2f}'))

        # assemble the form
        self.viewLayout.addWidget(self.titleLabel)
        themeRow = QHBoxLayout()
        themeRow.addStretch(1)
        themeRow.addWidget(self.lightRadioButton)
        themeRow.addWidget(self.darkRadioButton)
        self.__addRow(self.tr('Base theme'), themeRow)
        self.__addRow(self.tr('Accent color'), self.accentButton)
        self.__addRow(self.tr('Surface tint'), self.tintButton)
        self.__addRow(self.tr('Enable tint'), self.tintEnabledBox)

        strengthRow = QHBoxLayout()
        strengthRow.addWidget(self.strengthSlider, 1)
        strengthRow.addWidget(self.strengthLabel)
        self.__addRow(self.tr('Strength'), strengthRow)

        self.yesButton.setText(self.tr('Apply'))
        self.cancelButton.setText(self.tr('Cancel'))
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

    def customSkin(self) -> FluentSkin:
        """ return the skin assembled from the current form state """
        return self.skin.copy(
            name='Custom',
            theme=Theme.DARK if self.darkRadioButton.isChecked() else Theme.LIGHT,
            accentColor=self.accentButton.color,
            surfaceTint=self.tintButton.color if self.tintEnabledBox.isChecked() else None,
            surfaceTintStrength=self.strengthSlider.value() / 100,
        )


class SkinCardView(QWidget):
    """ A single choice view that lays the skin previews out in a flow

    Examples
    --------
    >>> view = SkinCardView(parent=self)
    >>> view.skinChanged.connect(skin.apply)
    >>> view.setCurrentSkin(FluentSkinSet.DEEP_OCEAN)
    """

    skinChanged = pyqtSignal(object)
    customRequested = pyqtSignal()

    def __init__(self, skins: Optional[List[FluentSkin]] = None, parent=None):
        """
        Parameters
        ----------
        skins: List[FluentSkin]
            the skins to show, the presets of `FluentSkinSet` are used when
            it's `None`

        parent: QWidget
            parent widget
        """
        super().__init__(parent)
        self.currentSkin = None
        self.cards = {}   # type: Dict[str, SkinCard]

        self.flowLayout = FlowLayout(self, needAni=False)
        self.flowLayout.setContentsMargins(0, 0, 0, 0)
        self.flowLayout.setHorizontalSpacing(10)
        self.flowLayout.setVerticalSpacing(10)

        for skin in (FluentSkinSet.skins() if skins is None else skins):
            self.addSkin(skin)

        self.customCard = CustomSkinCard(self)
        self.customCard.clicked.connect(self.customRequested)
        self.flowLayout.addWidget(self.customCard)

    def addSkin(self, skin: FluentSkin):
        """ add a preview card of the given skin """
        card = SkinCard(skin, self)
        card.clicked.connect(self.setCurrentSkin)
        self.flowLayout.addWidget(card)
        self.cards[skin.name] = card

    def setCurrentSkin(self, skin: FluentSkin):
        """ select the card of the given skin, no card is selected when the
        skin is not one of the cards """
        if skin is self.currentSkin:
            return

        for name, card in self.cards.items():
            card.setSelected(skin is not None and name == skin.name)

        self.currentSkin = skin
        self.skinChanged.emit(skin)
