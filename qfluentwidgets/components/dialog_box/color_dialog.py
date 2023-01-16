# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRegExp
from PyQt5.QtGui import (QIcon, QBrush, QColor, QMouseEvent, QPixmap,
                         QPainter, QPen, QIntValidator, QRegExpValidator)
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QWidget,
                             QToolButton, QPushButton, QFrame, QVBoxLayout)

from ...common.icon import getIconColor
from ...common.style_sheet import setStyleSheet, getStyleSheet
from ..widgets import LineEditMenu, Slider, ScrollArea
from .mask_dialog_base import MaskDialogBase


class HuePanel(QWidget):
    """ Hue panel """

    colorChanged = pyqtSignal(QColor)

    def __init__(self, color=QColor(255, 0, 0), parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(320, 320)
        self.huePixmap = QPixmap(":/qfluentwidgets/images/color_dialog/HuePanel.png")
        self.setColor(color)

    def mousePressEvent(self, e: QMouseEvent):
        self.setPickerPosition(e.pos())

    def mouseMoveEvent(self, e: QMouseEvent):
        self.setPickerPosition(e.pos())

    def setPickerPosition(self, pos: QPoint):
        """ set the position of  """
        self.pickerPos = pos
        self.color.setHsv(
            min(1, pos.x() / self.width()) * 360,
            min(1, (self.height() - pos.y()) / self.height()) * 255,
            255
        )
        self.update()
        self.colorChanged.emit(self.color)

    def setColor(self, color: QColor):
        """ set color """
        self.color = QColor(color)
        self.color.setHsv(self.color.hue(), self.color.saturation(), 255)
        self.pickerPos = QPoint(
            self.hue/360*self.width(),
            (255 - self.saturation)/255*self.height()
        )
        self.update()

    @property
    def hue(self):
        return self.color.hue()

    @property
    def saturation(self):
        return self.color.saturation()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)

        # draw hue panel
        painter.setBrush(QBrush(self.huePixmap))
        painter.setPen(QPen(QColor(0, 0, 0, 15), 3))
        painter.drawRoundedRect(self.rect(), 7, 7)

        # draw picker
        if self.saturation > 153 or 40 < self.hue < 180:
            color = Qt.black
        else:
            color = QColor(255, 253, 254)

        painter.setPen(QPen(color, 3))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(self.pickerPos.x() - 10,
                            self.pickerPos.y() - 10, 20, 20)


class BrightnessSlider(Slider):
    """ Brightness slider """

    colorChanged = pyqtSignal(QColor)

    def __init__(self, color: QColor, parent=None):
        super().__init__(Qt.Horizontal, parent)
        self.setRange(0, 255)
        self.setSingleStep(1)
        self.setColor(color)
        self.valueChanged.connect(self.__onValueChanged)

    def setColor(self, color: QColor):
        """ set color """
        self.color = QColor(color)
        self.setValue(self.color.value())
        qss = getStyleSheet('color_dialog')
        qss = qss.replace('--slider-hue', str(self.color.hue()))
        qss = qss.replace('--slider-saturation', str(self.color.saturation()))
        self.setStyleSheet(qss)

    def __onValueChanged(self, value: int):
        """ slider value changed slot """
        self.color.setHsv(self.color.hue(), self.color.saturation(), value)
        self.setColor(self.color)
        self.colorChanged.emit(self.color)


class ColorCard(QWidget):
    """ Color card """

    def __init__(self, color: QColor, parent=None):
        super().__init__(parent)
        self.setFixedSize(55, 160)
        self.setColor(color)

    def setColor(self, color: QColor):
        """ set the color of card """
        self.color = QColor(color)
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        painter.setBrush(self.color)
        painter.setPen(QColor(0, 0, 0, 13))
        painter.drawRoundedRect(self.rect(), 5, 5)


class ColorLineEdit(QLineEdit):
    """ Color line edit """

    valueChanged = pyqtSignal(str)

    def __init__(self, value: int, parent=None):
        super().__init__(str(value), parent)
        self.setFixedSize(170, 41)
        self.clearButton = QToolButton(self)

        self.clearButton.move(self.width() - 41, 5)
        self.clearButton.setFixedSize(36, 31)
        self.clearButton.setObjectName('clearButton')
        self.clearButton.setIcon(
            QIcon(f":/qfluentwidgets/images/color_dialog/Clear_{getIconColor()}.png"))
        self.clearButton.setIconSize(self.size())
        self.clearButton.setCursor(Qt.PointingHandCursor)
        self.clearButton.hide()

        self.setValidator(QIntValidator(0, 255, self))
        self.setTextMargins(0, 0, 41, 0)
        self.clearButton.clicked.connect(self.clear)
        self.textEdited.connect(self._onTextEdited)
        self.textChanged.connect(self._onTextChanged)

    def focusOutEvent(self, e):
        super().focusOutEvent(e)
        self.clearButton.hide()

    def focusInEvent(self, e):
        super().focusInEvent(e)
        self.clearButton.setVisible(bool(self.text()))

    def _onTextEdited(self, text: str):
        """ text edited slot """
        state = self.validator().validate(text, 0)[0]
        if state == QIntValidator.Acceptable:
            self.valueChanged.emit(text)

    def _onTextChanged(self, text: str):
        """ text changed slot """
        self.clearButton.setVisible(bool(text) and self.hasFocus())

    def contextMenuEvent(self, e):
        menu = LineEditMenu(self)
        menu.exec_(e.globalPos())


class HexColorLineEdit(ColorLineEdit):
    """ Hex color line edit """

    def __init__(self, color: QColor, parent=None):
        super().__init__(QColor(color).name()[1:], parent)
        self.setValidator(QRegExpValidator(QRegExp(r'[A-Fa-f0-9]{6}')))
        self.setTextMargins(11, 0, 41, 0)
        self.prefixLabel = QLabel('#', self)
        self.prefixLabel.move(13, 9)
        self.prefixLabel.setObjectName('prefixLabel')

    def setColor(self, color: QColor):
        """ set color """
        self.setText(color.name()[1:])


class ColorDialog(MaskDialogBase):
    """ Color dialog """

    colorChanged = pyqtSignal(QColor)

    def __init__(self, color: QColor, title: str, parent=None):
        super().__init__(parent)
        self.oldColor = QColor(color)
        self.color = QColor(color)

        self.scrollArea = ScrollArea(self.widget)
        self.scrollWidget = QWidget(self.scrollArea)

        self.buttonGroup = QFrame(self.widget)
        self.yesButton = QPushButton(self.tr('OK'), self.buttonGroup)
        self.cancelButton = QPushButton(self.tr('Cancel'), self.buttonGroup)

        self.titleLabel = QLabel(title, self.scrollWidget)
        self.huePanel = HuePanel(color, self.scrollWidget)
        self.newColorCard = ColorCard(color, self.scrollWidget)
        self.oldColorCard = ColorCard(color, self.scrollWidget)
        self.brightSlider = BrightnessSlider(color, self.scrollWidget)

        self.editLabel = QLabel(self.tr('Edit Color'), self.scrollWidget)
        self.redLabel = QLabel(self.tr('Red'), self.scrollWidget)
        self.blueLabel = QLabel(self.tr('Blue'), self.scrollWidget)
        self.greenLabel = QLabel(self.tr('Green'), self.scrollWidget)
        self.hexLineEdit = HexColorLineEdit(color, self.scrollWidget)
        self.redLineEdit = ColorLineEdit(self.color.red(), self.scrollWidget)
        self.greenLineEdit = ColorLineEdit(self.color.green(), self.scrollWidget)
        self.blueLineEdit = ColorLineEdit(self.color.blue(), self.scrollWidget)

        self.vBoxLayout = QVBoxLayout(self.widget)

        self.__initWidget()

    def __initWidget(self):
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setViewportMargins(60, 30, 0, 30)
        self.scrollArea.setWidget(self.scrollWidget)

        self.widget.setMaximumSize(610, 870)
        self.widget.resize(610, 870)
        self.scrollWidget.resize(550, 700)
        self.buttonGroup.setFixedSize(608, 101)
        self.yesButton.setFixedWidth(270)
        self.cancelButton.setFixedWidth(270)

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 80))
        self.setMaskColor(QColor(0, 0, 0, 76))

        self.__setQss()
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.huePanel.move(0, 57)
        self.newColorCard.move(360, 57)
        self.oldColorCard.move(360, self.newColorCard.geometry().bottom()+1)
        self.brightSlider.move(0, 405)

        self.editLabel.move(0, 476)
        self.redLineEdit.move(0, 532)
        self.greenLineEdit.move(0, 588)
        self.blueLineEdit.move(0, 644)
        self.redLabel.move(180, 543)
        self.greenLabel.move(180, 598)
        self.blueLabel.move(180, 655)
        self.hexLineEdit.move(245, 476)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.scrollArea, 1)
        self.vBoxLayout.addWidget(self.buttonGroup, 0, Qt.AlignBottom)

        self.yesButton.move(30, 31)
        self.cancelButton.move(310, 31)

    def __setQss(self):
        self.editLabel.setObjectName('editLabel')
        self.titleLabel.setObjectName('titleLabel')
        self.yesButton.setObjectName('yesButton')
        self.cancelButton.setObjectName('cancelButton')
        self.buttonGroup.setObjectName('buttonGroup')
        setStyleSheet(self, 'color_dialog')
        self.titleLabel.adjustSize()
        self.editLabel.adjustSize()

    def setColor(self, color: QColor, movePicker=True):
        """ set color """
        self.color = QColor(color)
        self.brightSlider.setColor(color)
        self.newColorCard.setColor(color)
        self.hexLineEdit.setColor(color)
        self.redLineEdit.setText(str(color.red()))
        self.blueLineEdit.setText(str(color.blue()))
        self.greenLineEdit.setText(str(color.green()))
        if movePicker:
            self.huePanel.setColor(color)

    def __onHueChanged(self, color: QColor):
        """ hue changed slot """
        self.color.setHsv(color.hue(), color.saturation(), self.color.value())
        self.setColor(self.color)

    def __onBrightnessChanged(self, color: QColor):
        """ brightness changed slot """
        self.color.setHsv(self.color.hue(),
                          self.color.saturation(), color.value())
        self.setColor(self.color, False)

    def __onRedChanged(self, red: str):
        """ red channel changed slot """
        self.color.setRed(int(red))
        self.setColor(self.color)

    def __onBlueChanged(self, blue: str):
        """ blue channel changed slot """
        self.color.setBlue(int(blue))
        self.setColor(self.color)

    def __onGreenChanged(self, green: str):
        """ green channel changed slot """
        self.color.setGreen(int(green))
        self.setColor(self.color)

    def __onHexColorChanged(self, color: str):
        """ hex color changed slot """
        self.color.setNamedColor("#" + color)
        self.setColor(self.color)

    def __onYesButtonClicked(self):
        """ yes button clicked slot """
        if self.color != self.oldColor:
            self.colorChanged.emit(self.color)

        self.close()

    def updateStyle(self):
        """ update style sheet """
        self.setStyle(QApplication.style())
        self.titleLabel.adjustSize()
        self.editLabel.adjustSize()

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        self.cancelButton.clicked.connect(self.close)
        self.yesButton.clicked.connect(self.__onYesButtonClicked)

        self.huePanel.colorChanged.connect(self.__onHueChanged)
        self.brightSlider.colorChanged.connect(self.__onBrightnessChanged)

        self.redLineEdit.valueChanged.connect(self.__onRedChanged)
        self.blueLineEdit.valueChanged.connect(self.__onBlueChanged)
        self.greenLineEdit.valueChanged.connect(self.__onGreenChanged)
        self.hexLineEdit.valueChanged.connect(self.__onHexColorChanged)
