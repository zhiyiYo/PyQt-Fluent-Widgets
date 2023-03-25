# coding:utf-8
from PyQt6.QtCore import Qt, pyqtSignal, QPoint, QRegularExpression, QSize
from PyQt6.QtGui import (QBrush, QColor, QPixmap, QPainter, QPen, QIntValidator,
                         QIcon, QRegularExpressionValidator)
from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QPushButton, QFrame, QVBoxLayout

from ...common.style_sheet import setStyleSheet, getStyleSheet
from ..widgets import Slider, ScrollArea, PushButton, PrimaryPushButton
from ..widgets.line_edit import LineEdit
from .mask_dialog_base import MaskDialogBase


class HuePanel(QWidget):
    """ Hue panel """

    colorChanged = pyqtSignal(QColor)

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
        painter.setRenderHints(QPainter.RenderHint.Antialiasing |
                               QPainter.RenderHint.SmoothPixmapTransform)

        # draw hue panel
        painter.setBrush(QBrush(self.huePixmap))
        painter.setPen(QPen(QColor(0, 0, 0, 15), 2.4))
        painter.drawRoundedRect(self.rect(), 5.6, 5.6)

        # draw picker
        if self.saturation > 153 or 40 < self.hue < 180:
            color = Qt.GlobalColor.black
        else:
            color = QColor(255, 253, 254)

        painter.setPen(QPen(color, 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(self.pickerPos.x() - 8,
                            self.pickerPos.y() - 8, 16, 16)


class BrightnessSlider(Slider):
    """ Brightness slider """

    colorChanged = pyqtSignal(QColor)

    def __init__(self, color, parent=None):
        super().__init__(Qt.Orientation.Horizontal, parent)
        self.setRange(0, 255)
        self.setSingleStep(1)
        self.setColor(color)
        self.valueChanged.connect(self.__onValueChanged)

    def setColor(self, color):
        """ set color """
        self.color = QColor(color)
        self.setValue(self.color.value())
        qss = getStyleSheet('color_dialog')
        qss = qss.replace('--slider-hue', str(self.color.hue()))
        qss = qss.replace('--slider-saturation', str(self.color.saturation()))
        self.setStyleSheet(qss)

    def __onValueChanged(self, value):
        """ slider value changed slot """
        self.color.setHsv(self.color.hue(), self.color.saturation(), value)
        self.setColor(self.color)
        self.colorChanged.emit(self.color)


class ColorCard(QWidget):
    """ Color card """

    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.setFixedSize(44, 128)
        self.setColor(color)

    def setColor(self, color):
        """ set the color of card """
        self.color = QColor(color)
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)

        painter.setBrush(self.color)
        painter.setPen(QColor(0, 0, 0, 13))
        painter.drawRoundedRect(self.rect(), 4, 4)


class ColorLineEdit(LineEdit):
    """ Color line edit """

    valueChanged = pyqtSignal(str)

    def __init__(self, value, parent=None):
        super().__init__(str(value), parent)
        self.setFixedSize(136, 33)
        self.setClearButtonEnabled(True)
        self.setValidator(QIntValidator(0, 255, self))

        self.textEdited.connect(self._onTextEdited)

    def _onTextEdited(self, text):
        """ text edited slot """
        state = self.validator().validate(text, 0)[0]
        if state == QIntValidator.State.Acceptable:
            self.valueChanged.emit(text)


class HexColorLineEdit(ColorLineEdit):
    """ Hex color line edit """

    def __init__(self, color, parent=None):
        super().__init__(QColor(color).name()[1:], parent)
        self.setValidator(QRegularExpressionValidator(QRegularExpression(r'[A-Fa-f0-9]{6}')))
        self.setTextMargins(4, 0, 33, 0)
        self.prefixLabel = QLabel('#', self)
        self.prefixLabel.move(10, 7)
        self.prefixLabel.setObjectName('prefixLabel')

    def setColor(self, color):
        """ set color """
        self.setText(color.name()[1:])


class ColorDialog(MaskDialogBase):
    """ Color dialog """

    colorChanged = pyqtSignal(QColor)

    def __init__(self, color, title: str, parent=None):
        """
        Parameters
        ----------
        color: `QColor` | `GlobalColor` | str
            initial color

        title: str
            the title of dialog

        parent: QWidget
            parent widget
        """
        super().__init__(parent)
        self.oldColor = QColor(color)
        self.color = QColor(color)

        self.scrollArea = ScrollArea(self.widget)
        self.scrollWidget = QWidget(self.scrollArea)

        self.buttonGroup = QFrame(self.widget)
        self.yesButton = PrimaryPushButton(self.tr('OK'), self.buttonGroup)
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
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scrollArea.setViewportMargins(48, 24, 0, 24)
        self.scrollArea.setWidget(self.scrollWidget)

        self.widget.setMaximumSize(488, 696)
        self.widget.resize(488, 696)
        self.scrollWidget.resize(440, 560)
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

        self.editLabel.move(0, 381)
        self.redLineEdit.move(0, 426)
        self.greenLineEdit.move(0, 470)
        self.blueLineEdit.move(0, 515)
        self.redLabel.move(144, 434)
        self.greenLabel.move(144, 478)
        self.blueLabel.move(144, 524)
        self.hexLineEdit.move(196, 381)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addWidget(self.scrollArea, 1)
        self.vBoxLayout.addWidget(self.buttonGroup, 0, Qt.AlignmentFlag.AlignBottom)

        self.yesButton.move(24, 25)
        self.cancelButton.move(250, 25)

    def __setQss(self):
        self.editLabel.setObjectName('editLabel')
        self.titleLabel.setObjectName('titleLabel')
        self.yesButton.setObjectName('yesButton')
        self.cancelButton.setObjectName('cancelButton')
        self.buttonGroup.setObjectName('buttonGroup')
        setStyleSheet(self, 'color_dialog')
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
        self.color.setHsv(color.hue(), color.saturation(), self.color.value())
        self.setColor(self.color)

    def __onBrightnessChanged(self, color):
        """ brightness changed slot """
        self.color.setHsv(self.color.hue(),
                          self.color.saturation(), color.value())
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

    def __onHexColorChanged(self, color):
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
