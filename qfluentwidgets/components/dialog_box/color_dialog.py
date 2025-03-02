# coding:utf-8
from PySide6.QtCore import Qt, Signal, QPoint, QRegularExpression, QSize
from PySide6.QtGui import (QBrush, QColor, QPixmap, QPainter,
                           QPen, QIntValidator, QRegularExpressionValidator, QIcon)
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QPushButton, QFrame, QVBoxLayout

from ...common.style_sheet import FluentStyleSheet, isDarkTheme
from ..widgets import ClickableSlider, SingleDirectionScrollArea, PushButton, PrimaryPushButton
from ..widgets.line_edit import LineEdit
from .mask_dialog_base import MaskDialogBase


class HuePanel(QWidget):
    """ Hue panel """

    colorChanged = Signal(QColor)

    def __init__(self, color=QColor(255, 0, 0), parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(256, 256)
        self.huePixmap = QPixmap(":/qfluentwidgets/images/color_dialog/HuePanel.png")
        self.setColor(color)

    def mousePressEvent(self, e):
        self.setPickerPosition(e.pos())

    def mouseMoveEvent(self, e):
        self.setPickerPosition(e.pos())

    def setPickerPosition(self, pos):
        """ set the position of  """
        self.pickerPos = pos
        self.color.setHsv(
            int(max(0, min(1, pos.x() / self.width())) * 360),
            int(max(0, min(1, (self.height() - pos.y()) / self.height())) * 255),
            255
        )
        self.update()
        self.colorChanged.emit(self.color)

    def setColor(self, color):
        """ set color """
        self.color = QColor(color)
        self.color.setHsv(self.color.hue(), self.color.saturation(), 255)
        self.pickerPos = QPoint(
            int(self.hue/360*self.width()),
            int((255 - self.saturation)/255*self.height())
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
        painter.setPen(QPen(QColor(0, 0, 0, 15), 2.4))
        painter.drawRoundedRect(self.rect(), 5.6, 5.6)

        # draw picker
        if self.saturation > 153 or 40 < self.hue < 180:
            color = Qt.black
        else:
            color = QColor(255, 253, 254)

        painter.setPen(QPen(color, 3))
        painter.setBrush(Qt.NoBrush)
        painter.drawEllipse(self.pickerPos.x() - 8,
                            self.pickerPos.y() - 8, 16, 16)


class BrightnessSlider(ClickableSlider):
    """ Brightness slider """

    colorChanged = Signal(QColor)

    def __init__(self, color, parent=None):
        super().__init__(Qt.Horizontal, parent)
        self.setRange(0, 255)
        self.setSingleStep(1)
        self.setColor(color)
        self.valueChanged.connect(self.__onValueChanged)

    def setColor(self, color):
        """ set color """
        self.color = QColor(color)
        self.setValue(self.color.value())
        qss = FluentStyleSheet.COLOR_DIALOG.content()
        qss = qss.replace('--slider-hue', str(self.color.hue()))
        qss = qss.replace('--slider-saturation', str(self.color.saturation()))
        self.setStyleSheet(qss)

    def __onValueChanged(self, value):
        """ slider value changed slot """
        self.color.setHsv(self.color.hue(), self.color.saturation(), value, self.color.alpha())
        self.setColor(self.color)
        self.colorChanged.emit(self.color)


class ColorCard(QWidget):
    """ Color card """

    def __init__(self, color, parent=None, enableAlpha=False):
        super().__init__(parent)
        self.setFixedSize(44, 128)
        self.setColor(color)
        self.enableAlpha = enableAlpha
        self.titledPixmap = self._createTitledBackground()

    def _createTitledBackground(self):
        pixmap = QPixmap(8, 8)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)

        c = 255 if isDarkTheme() else 0
        color = QColor(c, c, c, 26)
        painter.fillRect(4, 0, 4, 4, color)
        painter.fillRect(0, 4, 4, 4, color)
        painter.end()
        return pixmap

    def setColor(self, color):
        """ set the color of card """
        self.color = QColor(color)
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)

        # draw tiled background
        if self.enableAlpha:
            painter.setBrush(QBrush(self.titledPixmap))
            painter.setPen(QColor(0, 0, 0, 13))
            painter.drawRoundedRect(self.rect(), 4, 4)

        # draw color
        painter.setBrush(self.color)
        painter.setPen(QColor(0, 0, 0, 13))
        painter.drawRoundedRect(self.rect(), 4, 4)


class ColorLineEdit(LineEdit):
    """ Color line edit """

    valueChanged = Signal(str)

    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setText(str(value))
        self.setFixedSize(136, 33)
        self.setClearButtonEnabled(True)
        self.setValidator(QIntValidator(0, 255, self))

        self.textEdited.connect(self._onTextEdited)

    def _onTextEdited(self, text):
        """ text edited slot """
        state = self.validator().validate(text, 0)[0]
        if state == QIntValidator.Acceptable:
            self.valueChanged.emit(text)


class HexColorLineEdit(ColorLineEdit):
    """ Hex color line edit """

    def __init__(self, color, parent=None, enableAlpha=False):
        self.colorFormat = QColor.HexArgb if enableAlpha else QColor.HexRgb
        super().__init__(QColor(color).name(self.colorFormat)[1:], parent)

        if enableAlpha:
            self.setValidator(QRegularExpressionValidator(QRegularExpression(r'[A-Fa-f0-9]{8}')))
        else:
            self.setValidator(QRegularExpressionValidator(QRegularExpression(r'[A-Fa-f0-9]{6}')))

        self.setTextMargins(4, 0, 33, 0)
        self.prefixLabel = QLabel('#', self)
        self.prefixLabel.move(7, 2)
        self.prefixLabel.setObjectName('prefixLabel')

    def setColor(self, color):
        """ set color """
        self.setText(color.name(self.colorFormat)[1:])


class OpacityLineEdit(ColorLineEdit):
    """ Opacity line edit """

    def __init__(self, value, parent=None, enableAlpha=False):
        super().__init__(int(value/255*100), parent)
        self.setValidator(QRegularExpressionValidator(QRegularExpression(r'[0-9][0-9]{0,1}|100')))
        self.setTextMargins(4, 0, 33, 0)
        self.suffixLabel = QLabel('%', self)
        self.suffixLabel.setObjectName('suffixLabel')
        self.textChanged.connect(self._adjustSuffixPos)

    def showEvent(self, e):
        super().showEvent(e)
        self._adjustSuffixPos()

    def _adjustSuffixPos(self):
        x = self.fontMetrics().boundingRect(self.text()).width() + 18
        self.suffixLabel.move(x, 2)


class ColorDialog(MaskDialogBase):
    """ Color dialog """

    colorChanged = Signal(QColor)

    def __init__(self, color, title: str, parent=None, enableAlpha=False):
        """
        Parameters
        ----------
        color: `QColor` | `GlobalColor` | str
            initial color

        title: str
            the title of dialog

        parent: QWidget
            parent widget

        enableAlpha: bool
            whether to enable the alpha channel
        """
        super().__init__(parent)
        self.enableAlpha = enableAlpha
        if not enableAlpha:
            color = QColor(color)
            color.setAlpha(255)

        self.oldColor = QColor(color)
        self.color = QColor(color)

        self.scrollArea = SingleDirectionScrollArea(self.widget)
        self.scrollWidget = QWidget(self.scrollArea)

        self.buttonGroup = QFrame(self.widget)
        self.yesButton = PrimaryPushButton(self.tr('OK'), self.buttonGroup)
        self.cancelButton = QPushButton(self.tr('Cancel'), self.buttonGroup)

        self.titleLabel = QLabel(title, self.scrollWidget)
        self.huePanel = HuePanel(color, self.scrollWidget)
        self.newColorCard = ColorCard(color, self.scrollWidget, enableAlpha)
        self.oldColorCard = ColorCard(color, self.scrollWidget, enableAlpha)
        self.brightSlider = BrightnessSlider(color, self.scrollWidget)

        self.editLabel = QLabel(self.tr('Edit Color'), self.scrollWidget)
        self.redLabel = QLabel(self.tr('Red'), self.scrollWidget)
        self.blueLabel = QLabel(self.tr('Blue'), self.scrollWidget)
        self.greenLabel = QLabel(self.tr('Green'), self.scrollWidget)
        self.opacityLabel = QLabel(self.tr('Opacity'), self.scrollWidget)
        self.hexLineEdit = HexColorLineEdit(color, self.scrollWidget, enableAlpha)
        self.redLineEdit = ColorLineEdit(self.color.red(), self.scrollWidget)
        self.greenLineEdit = ColorLineEdit(self.color.green(), self.scrollWidget)
        self.blueLineEdit = ColorLineEdit(self.color.blue(), self.scrollWidget)
        self.opacityLineEdit = OpacityLineEdit(self.color.alpha(), self.scrollWidget)

        self.vBoxLayout = QVBoxLayout(self.widget)

        self.__initWidget()

    def __initWidget(self):
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setViewportMargins(48, 24, 0, 24)
        self.scrollArea.setWidget(self.scrollWidget)

        self.widget.setMaximumSize(488, 696+40*self.enableAlpha)
        self.widget.resize(488, 696+40*self.enableAlpha)
        self.scrollWidget.resize(440, 560+40*self.enableAlpha)
        self.buttonGroup.setFixedSize(486, 81)
        self.yesButton.setFixedWidth(216)
        self.cancelButton.setFixedWidth(216)

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 80))
        self.setMaskColor(QColor(0, 0, 0, 76))

        self.__setQss()
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.huePanel.move(0, 46)
        self.newColorCard.move(288, 46)
        self.oldColorCard.move(288, self.newColorCard.geometry().bottom()+1)
        self.brightSlider.move(0, 324)

        self.editLabel.move(0, 385)
        self.redLineEdit.move(0, 426)
        self.greenLineEdit.move(0, 470)
        self.blueLineEdit.move(0, 515)
        self.redLabel.move(144, 434)
        self.greenLabel.move(144, 478)
        self.blueLabel.move(144, 524)
        self.hexLineEdit.move(196, 381)

        if self.enableAlpha:
            self.opacityLineEdit.move(0, 560)
            self.opacityLabel.move(144, 567)
        else:
            self.opacityLineEdit.hide()
            self.opacityLabel.hide()

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.scrollArea, 1)
        self.vBoxLayout.addWidget(self.buttonGroup, 0, Qt.AlignBottom)

        self.yesButton.move(24, 25)
        self.cancelButton.move(250, 25)

    def __setQss(self):
        self.editLabel.setObjectName('editLabel')
        self.titleLabel.setObjectName('titleLabel')
        self.yesButton.setObjectName('yesButton')
        self.cancelButton.setObjectName('cancelButton')
        self.buttonGroup.setObjectName('buttonGroup')
        FluentStyleSheet.COLOR_DIALOG.apply(self)
        self.titleLabel.adjustSize()
        self.editLabel.adjustSize()

    def setColor(self, color, movePicker=True):
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

    def __onHueChanged(self, color):
        """ hue changed slot """
        self.color.setHsv(
            color.hue(), color.saturation(), self.color.value(), self.color.alpha())
        self.setColor(self.color)

    def __onBrightnessChanged(self, color):
        """ brightness changed slot """
        self.color.setHsv(
            self.color.hue(), self.color.saturation(), color.value(), color.alpha())
        self.setColor(self.color, False)

    def __onRedChanged(self, red):
        """ red channel changed slot """
        self.color.setRed(int(red))
        self.setColor(self.color)

    def __onBlueChanged(self, blue):
        """ blue channel changed slot """
        self.color.setBlue(int(blue))
        self.setColor(self.color)

    def __onGreenChanged(self, green):
        """ green channel changed slot """
        self.color.setGreen(int(green))
        self.setColor(self.color)

    def __onOpacityChanged(self, opacity):
        """ opacity channel changed slot """
        self.color.setAlpha(int(int(opacity)/100*255))
        self.setColor(self.color)

    def __onHexColorChanged(self, color):
        """ hex color changed slot """
        self.color.setNamedColor("#" + color)
        self.setColor(self.color)

    def __onYesButtonClicked(self):
        """ yes button clicked slot """
        self.accept()
        if self.color != self.oldColor:
            self.colorChanged.emit(self.color)

    def updateStyle(self):
        """ update style sheet """
        self.setStyle(QApplication.style())
        self.titleLabel.adjustSize()
        self.editLabel.adjustSize()
        self.redLabel.adjustSize()
        self.greenLabel.adjustSize()
        self.blueLabel.adjustSize()
        self.opacityLabel.adjustSize()

    def showEvent(self, e):
        self.updateStyle()
        super().showEvent(e)

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        self.cancelButton.clicked.connect(self.reject)
        self.yesButton.clicked.connect(self.__onYesButtonClicked)

        self.huePanel.colorChanged.connect(self.__onHueChanged)
        self.brightSlider.colorChanged.connect(self.__onBrightnessChanged)

        self.redLineEdit.valueChanged.connect(self.__onRedChanged)
        self.blueLineEdit.valueChanged.connect(self.__onBlueChanged)
        self.greenLineEdit.valueChanged.connect(self.__onGreenChanged)
        self.hexLineEdit.valueChanged.connect(self.__onHexColorChanged)
        self.opacityLineEdit.valueChanged.connect(self.__onOpacityChanged)
