# coding:utf-8
from PyQt5.QtCore import Qt, pyqtSignal, QRegExp, QRectF
from PyQt5.QtGui import (QBrush, QColor, QLinearGradient, QPainter, QPainterPath,
                         QPen, QPixmap, QIntValidator, QRegExpValidator)
from PyQt5.QtWidgets import (QLabel, QWidget, QPushButton, QFrame, QVBoxLayout,
                             QHBoxLayout, QSizePolicy)

from ...common.style_sheet import FluentStyleSheet, isDarkTheme
from ..widgets import PrimaryPushButton, SpinBox, CompactSpinBox
from ..widgets.line_edit import LineEdit
from .mask_dialog_base import MaskDialogBase


class HuePanel(QWidget):
    """ Hue panel """

    colorChanged = pyqtSignal(QColor)

    def __init__(self, color=QColor(255, 0, 0), parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(256, 256)
        self.setCursor(Qt.CrossCursor)
        self.hue = 0
        self.saturation = 255
        self.setColor(color)

    def mousePressEvent(self, e):
        self.setPickerPosition(e.pos())

    def mouseMoveEvent(self, e):
        self.setPickerPosition(e.pos())

    def setPickerPosition(self, pos):
        """ set the position of color picker """
        self.hue = max(0, min(1, pos.x() / self.width())) * 359
        self.saturation = max(0, min(1, (self.height() - pos.y()) / self.height())) * 255
        self.update()
        self.colorChanged.emit(
            QColor.fromHsv(int(self.hue), int(self.saturation), 255))

    def setColor(self, color):
        """ set color """
        color = QColor(color)
        if color.hue() >= 0:
            self.hue = color.hue()
        self.saturation = color.saturation()
        self.update()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        rect = QRectF(self.rect().adjusted(1, 1, -1, -1))

        # draw hue panel
        path = QPainterPath()
        path.addRoundedRect(rect, 8, 8)
        painter.save()
        painter.setClipPath(path)

        gradient = QLinearGradient(rect.topLeft(), rect.topRight())
        for i in range(7):
            gradient.setColorAt(i / 6, QColor.fromHsvF(i / 6, 1, 1))
        painter.fillRect(rect, QBrush(gradient))

        white = QLinearGradient(rect.topLeft(), rect.bottomLeft())
        white.setColorAt(0, QColor(255, 255, 255, 0))
        white.setColorAt(1, QColor(255, 255, 255, 255))
        painter.fillRect(rect, QBrush(white))

        black = QLinearGradient(rect.topLeft(), rect.bottomLeft())
        black.setColorAt(0, QColor(0, 0, 0, 0))
        black.setColorAt(1, QColor(0, 0, 0, 255))
        painter.fillRect(rect, QBrush(black))
        painter.restore()

        painter.setPen(QPen(QColor(0, 0, 0, 32), 1))
        painter.setBrush(Qt.NoBrush)
        painter.drawRoundedRect(rect, 8, 8)

        # draw color picker
        x = rect.left() + self.hue / 359 * rect.width()
        y = rect.top() + (255 - self.saturation) / 255 * rect.height()
        painter.setPen(QPen(QColor(0, 0, 0, 140), 1))
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(int(x) - 7, int(y) - 7, 14, 14)


class BrightnessSlider(QWidget):
    """ Brightness slider """

    colorChanged = pyqtSignal(QColor)

    def __init__(self, color, parent=None):
        super().__init__(parent=parent)
        self.color = QColor(color)
        self.setFixedHeight(28)
        self.setCursor(Qt.SizeHorCursor)
        self.setFocusPolicy(Qt.StrongFocus)
        self._wheelDelta = 0

    def mousePressEvent(self, e):
        self.__setValue(e.pos().x())

    def mouseMoveEvent(self, e):
        self.__setValue(e.pos().x())

    def keyPressEvent(self, e):
        value = self.color.value()
        if e.key() in (Qt.Key_Left, Qt.Key_Down):
            value -= 1
        elif e.key() in (Qt.Key_Right, Qt.Key_Up):
            value += 1
        elif e.key() == Qt.Key_PageDown:
            value -= 10
        elif e.key() == Qt.Key_PageUp:
            value += 10
        elif e.key() == Qt.Key_Home:
            value = 0
        elif e.key() == Qt.Key_End:
            value = 255
        else:
            super().keyPressEvent(e)
            return
        self._setValue(value)

    def wheelEvent(self, e):
        e.accept()
        self._wheelDelta += e.angleDelta().y()
        steps = int(self._wheelDelta / 120)
        self._wheelDelta -= steps * 120
        if steps:
            self._setValue(self.color.value() + steps)

    def setColor(self, color):
        """ set color """
        self.color = QColor(color)
        self.update()

    def __setValue(self, x):
        rect = self.rect().adjusted(7, 8, -7, -8)
        value = max(0, min(255, round((x - rect.left()) / max(1, rect.width()) * 255)))
        self._setValue(value)

    def _setValue(self, value):
        value = max(0, min(255, value))
        if value == self.color.value():
            return

        self.color.setHsv(self.color.hue(), self.color.saturation(),
                          value, self.color.alpha())
        self.update()
        self.colorChanged.emit(self.color)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        rect = self.rect().adjusted(7, 8, -7, -8)

        # draw brightness gradient
        gradient = QLinearGradient(rect.topLeft(), rect.topRight())
        gradient.setColorAt(0, Qt.black)
        gradient.setColorAt(1, QColor.fromHsv(self.color.hue(), self.color.saturation(), 255))
        painter.setPen(QPen(QColor(0, 0, 0, 32), 1))
        painter.setBrush(QBrush(gradient))
        painter.drawRoundedRect(rect, 5, 5)

        # draw color picker
        x = rect.left() + self.color.value() / 255 * rect.width()
        y = rect.center().y()
        painter.setPen(QPen(QColor(0, 0, 0, 110), 1))
        painter.setBrush(QColor(255, 255, 255, 236))
        painter.drawEllipse(int(x) - 7, int(y) - 7, 14, 14)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.color)
        painter.drawEllipse(int(x) - 3, int(y) - 3, 6, 6)


class ColorCard(QWidget):
    """ Color card """

    def __init__(self, color, parent=None, enableAlpha=False):
        super().__init__(parent)
        self.setFixedHeight(36)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
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
        rect = self.rect().adjusted(1, 1, -1, -1)

        # draw tiled background
        if self.enableAlpha:
            painter.setBrush(QBrush(self.titledPixmap))
            painter.setPen(QColor(0, 0, 0, 13))
            painter.drawRoundedRect(rect, 6, 6)

        # draw color
        painter.setBrush(self.color)
        painter.setPen(QColor(0, 0, 0, 13))
        painter.drawRoundedRect(rect, 6, 6)


class ColorLineEdit(LineEdit):
    """ Color line edit """

    valueChanged = pyqtSignal(str)

    def __init__(self, value, parent=None):
        super().__init__(parent)
        self.setText(str(value))
        self.setMinimumWidth(136)
        self.setFixedHeight(33)
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
            self.setValidator(QRegExpValidator(QRegExp(r'[A-Fa-f0-9]{8}')))
        else:
            self.setValidator(QRegExpValidator(QRegExp(r'[A-Fa-f0-9]{6}')))

        self.setTextMargins(4, 0, 33, 0)
        self.prefixLabel = QLabel('#', self)
        self.prefixLabel.move(7, 2)
        self.prefixLabel.setObjectName('prefixLabel')

    def setColor(self, color):
        """ set color """
        self.setText(color.name(self.colorFormat)[1:])


class ColorDialog(MaskDialogBase):
    """ Color dialog """

    colorChanged = pyqtSignal(QColor)

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

        self.buttonGroup = QFrame(self.widget)
        self.yesButton = PrimaryPushButton(self.tr('OK'), self.buttonGroup)
        self.cancelButton = QPushButton(self.tr('Cancel'), self.buttonGroup)

        self.titleLabel = QLabel(title, self.widget)
        self.oldColorLabel = QLabel(self.tr('Original'), self.widget)
        self.newColorLabel = QLabel(self.tr('Current'), self.widget)
        self.huePanel = HuePanel(color, self.widget)
        self.newColorCard = ColorCard(color, self.widget, enableAlpha)
        self.oldColorCard = ColorCard(color, self.widget, enableAlpha)
        self.brightSlider = BrightnessSlider(color, self.widget)
        self.brightLabel = QLabel(self.tr('Brightness'), self.widget)
        self.hexLabel = QLabel(self.tr('Hex'), self.widget)
        self.opacityLabel = QLabel(self.tr('Opacity'), self.widget)
        self.hexLineEdit = HexColorLineEdit(color, self.widget, enableAlpha)
        self.redLabel = QLabel(self.tr('Red'), self.widget)
        self.greenLabel = QLabel(self.tr('Green'), self.widget)
        self.blueLabel = QLabel(self.tr('Blue'), self.widget)
        self.redSpinBox = CompactSpinBox(self.widget)
        self.greenSpinBox = CompactSpinBox(self.widget)
        self.blueSpinBox = CompactSpinBox(self.widget)
        for spin in (self.redSpinBox, self.greenSpinBox, self.blueSpinBox):
            spin.setRange(0, 255)
        self.redSpinBox.setValue(self.color.red())
        self.greenSpinBox.setValue(self.color.green())
        self.blueSpinBox.setValue(self.color.blue())
        self.opacitySpinBox = SpinBox(self.widget)
        self.opacitySpinBox.setRange(0, 100)
        self.opacitySpinBox.setSuffix('%')
        self.opacitySpinBox.setValue(int(self.color.alpha() / 255 * 100))

        self.vBoxLayout = QVBoxLayout(self.widget)

        self.__initWidget()

    def __initWidget(self):
        self.widget.setFixedWidth(488)
        self.buttonGroup.setFixedHeight(81)

        self.setShadowEffect(60, (0, 10), QColor(0, 0, 0, 80))
        self.setMaskColor(QColor(0, 0, 0, 76))

        # fixes https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/19
        self.yesButton.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        self.cancelButton.setAttribute(Qt.WA_LayoutUsesWidgetRect)
        self.yesButton.setAttribute(Qt.WA_MacShowFocusRect, False)
        self.yesButton.setFocus()

        self.__setQss()
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self._hBoxLayout.removeWidget(self.widget)
        self._hBoxLayout.addWidget(self.widget, 1, Qt.AlignCenter)

        # picker area
        pickerLayout = QHBoxLayout()
        pickerLayout.setSpacing(16)
        pickerLayout.addWidget(self.huePanel, 0, Qt.AlignTop)

        previewLayout = QVBoxLayout()
        previewLayout.setSpacing(8)
        previewLayout.addWidget(self.oldColorLabel)
        previewLayout.addWidget(self.oldColorCard)
        previewLayout.addSpacing(8)
        previewLayout.addWidget(self.newColorLabel)
        previewLayout.addWidget(self.newColorCard)
        previewLayout.addStretch(1)
        pickerLayout.addLayout(previewLayout, 1)

        # edit area
        editLayout = QHBoxLayout()
        editLayout.setSpacing(12)
        editLayout.addWidget(self.hexLabel, 0, Qt.AlignVCenter)
        editLayout.addWidget(self.hexLineEdit, 1)

        if self.enableAlpha:
            editLayout.addWidget(self.opacityLabel, 0, Qt.AlignVCenter)
            editLayout.addWidget(self.opacitySpinBox, 1)
        else:
            self.opacityLabel.hide()
            self.opacitySpinBox.hide()

        rgbLayout = QHBoxLayout()
        rgbLayout.setSpacing(12)
        rgbLayout.addWidget(self.redLabel, 0, Qt.AlignVCenter)
        rgbLayout.addWidget(self.redSpinBox, 1)
        rgbLayout.addWidget(self.greenLabel, 0, Qt.AlignVCenter)
        rgbLayout.addWidget(self.greenSpinBox, 1)
        rgbLayout.addWidget(self.blueLabel, 0, Qt.AlignVCenter)
        rgbLayout.addWidget(self.blueSpinBox, 1)

        self.viewLayout = QVBoxLayout()
        self.viewLayout.setSpacing(12)
        self.viewLayout.setContentsMargins(24, 24, 24, 24)
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addLayout(pickerLayout)
        self.viewLayout.addWidget(self.brightLabel)
        self.viewLayout.addWidget(self.brightSlider)
        self.viewLayout.addLayout(editLayout)
        self.viewLayout.addLayout(rgbLayout)

        buttonLayout = QHBoxLayout(self.buttonGroup)
        buttonLayout.setSpacing(12)
        buttonLayout.setContentsMargins(24, 24, 24, 24)
        buttonLayout.addWidget(self.yesButton, 1, Qt.AlignVCenter)
        buttonLayout.addWidget(self.cancelButton, 1, Qt.AlignVCenter)

        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.viewLayout, 1)
        self.vBoxLayout.addWidget(self.buttonGroup, 0, Qt.AlignBottom)

        self.widget.adjustSize()

    def __setQss(self):
        self.titleLabel.setObjectName('titleLabel')
        self.yesButton.setObjectName('yesButton')
        self.cancelButton.setObjectName('cancelButton')
        self.buttonGroup.setObjectName('buttonGroup')
        FluentStyleSheet.COLOR_DIALOG.apply(self)

    def setColor(self, color, movePicker=True):
        """ set color """
        self.color = QColor(color)
        self.__syncWidgets(movePicker)

    def __syncWidgets(self, movePicker=True, updateOpacity=True):
        self.brightSlider.setColor(self.color)
        self.newColorCard.setColor(self.color)
        self.hexLineEdit.setColor(self.color)

        channels = zip((self.redSpinBox, self.greenSpinBox, self.blueSpinBox),
                       (self.color.red(), self.color.green(), self.color.blue()))
        for spin, value in channels:
            spin.blockSignals(True)
            spin.setValue(value)
            spin.blockSignals(False)

        if updateOpacity:
            self.opacitySpinBox.blockSignals(True)
            self.opacitySpinBox.setValue(int(self.color.alpha() / 255 * 100))
            self.opacitySpinBox.blockSignals(False)
        if movePicker:
            self.huePanel.setColor(self.color)

    def __onHueChanged(self, color):
        """ hue changed slot """
        self.color.setHsv(
            color.hue(), color.saturation(), self.color.value(), self.color.alpha())
        self.__syncWidgets()

    def __onBrightnessChanged(self, color):
        """ brightness changed slot """
        self.color.setHsv(
            self.color.hue(), self.color.saturation(), color.value(), self.color.alpha())
        self.__syncWidgets(movePicker=False)

    def __onOpacityChanged(self, opacity):
        """ opacity changed slot """
        self.color.setAlpha(int(opacity / 100 * 255))
        self.__syncWidgets(updateOpacity=False)

    def __onRedChanged(self, red):
        """ red channel changed slot """
        self.color.setRed(red)
        self.__syncWidgets()

    def __onGreenChanged(self, green):
        """ green channel changed slot """
        self.color.setGreen(green)
        self.__syncWidgets()

    def __onBlueChanged(self, blue):
        """ blue channel changed slot """
        self.color.setBlue(blue)
        self.__syncWidgets()

    def __onHexColorChanged(self, color):
        """ hex color changed slot """
        self.color.setNamedColor("#" + color)
        self.__syncWidgets()

    def __onYesButtonClicked(self):
        """ yes button clicked slot """
        self.accept()
        if self.color != self.oldColor:
            self.colorChanged.emit(self.color)

    def updateStyle(self):
        """ update style sheet """
        FluentStyleSheet.COLOR_DIALOG.apply(self)

    def showEvent(self, e):
        self.updateStyle()
        super().showEvent(e)

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        self.cancelButton.clicked.connect(self.reject)
        self.yesButton.clicked.connect(self.__onYesButtonClicked)

        self.huePanel.colorChanged.connect(self.__onHueChanged)
        self.brightSlider.colorChanged.connect(self.__onBrightnessChanged)
        self.hexLineEdit.valueChanged.connect(self.__onHexColorChanged)
        self.opacitySpinBox.valueChanged.connect(self.__onOpacityChanged)
        self.redSpinBox.valueChanged.connect(self.__onRedChanged)
        self.greenSpinBox.valueChanged.connect(self.__onGreenChanged)
        self.blueSpinBox.valueChanged.connect(self.__onBlueChanged)
