# coding: utf-8
from PyQt5.QtCore import Qt, QTimer, pyqtProperty, pyqtSignal
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QToolButton, QWidget


class Indicator(QToolButton):
    """ 指示器 """

    checkedChanged = pyqtSignal(bool)

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.setCheckable(True)
        super().setChecked(False)
        self.resize(50, 26)
        self.__sliderOnColor = QColor(Qt.white)
        self.__sliderOffColor = QColor(Qt.black)
        self.__sliderDisabledColor = QColor(QColor(155, 154, 153))
        self.timer = QTimer(self)
        self.padding = self.height()//4
        self.sliderX = self.padding
        self.sliderRadius = (self.height()-2*self.padding)//2
        self.sliderEndX = self.width()-2*self.sliderRadius
        self.sliderStep = self.width()/50
        self.timer.timeout.connect(self.__updateSliderPos)

    def __updateSliderPos(self):
        """ 更新滑块位置 """
        if self.isChecked():
            if self.sliderX+self.sliderStep < self.sliderEndX:
                self.sliderX += self.sliderStep
            else:
                self.sliderX = self.sliderEndX
                self.timer.stop()
        else:
            if self.sliderX-self.sliderStep > self.sliderEndX:
                self.sliderX -= self.sliderStep
            else:
                self.sliderX = self.sliderEndX
                self.timer.stop()

        self.style().polish(self)

    def setChecked(self, isChecked: bool):
        """ 设置选中状态 """
        if isChecked == self.isChecked():
            return
        super().setChecked(isChecked)
        self.sliderEndX = self.width()-2*self.sliderRadius - \
            self.padding if self.isChecked() else self.padding
        self.timer.start(5)

    def mouseReleaseEvent(self, e):
        """ 鼠标点击更新选中状态 """
        super().mouseReleaseEvent(e)
        self.sliderEndX = self.width()-2*self.sliderRadius - \
            self.padding if self.isChecked() else self.padding
        self.timer.start(5)
        self.checkedChanged.emit(self.isChecked())

    def resizeEvent(self, e):
        self.padding = self.height()//4
        self.sliderRadius = (self.height()-2*self.padding)//2
        self.sliderStep = self.width()/50
        self.sliderEndX = self.width()-2*self.sliderRadius - \
            self.padding if self.isChecked() else self.padding
        self.update()

    def paintEvent(self, e):
        """ 绘制指示器 """
        super().paintEvent(e)  # 背景和边框由 qss 指定
        painter = QPainter(self)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(Qt.NoPen)
        if self.isEnabled():
            color = self.sliderOnColor if self.isChecked() else self.sliderOffColor
        else:
            color = self.sliderDisabledColor
        painter.setBrush(color)
        painter.drawEllipse(self.sliderX, self.padding,
                            self.sliderRadius*2, self.sliderRadius*2)

    def getSliderOnColor(self):
        return self.__sliderOnColor

    def setSliderOnColor(self, color: QColor):
        self.__sliderOnColor = color
        self.update()

    def getSliderOffColor(self):
        return self.__sliderOffColor

    def setSliderOffColor(self, color: QColor):
        self.__sliderOffColor = color
        self.update()

    def getSliderDisabledColor(self):
        return self.__sliderDisabledColor

    def setSliderDisabledColor(self, color: QColor):
        self.__sliderDisabledColor = color
        self.update()

    sliderOnColor = pyqtProperty(QColor, getSliderOnColor, setSliderOnColor)
    sliderOffColor = pyqtProperty(QColor, getSliderOffColor, setSliderOffColor)
    sliderDisabledColor = pyqtProperty(
        QColor, getSliderDisabledColor, setSliderDisabledColor)


class SwitchButton(QWidget):

    checkedChanged = pyqtSignal(bool)

    def __init__(self, text='关', parent=None):
        super().__init__(parent=parent)
        self.text = text
        self.__spacing = 15
        self.hBox = QHBoxLayout(self)
        self.indicator = Indicator(self)
        self.label = QLabel(text, self)
        self.__initWidget()

    def __initWidget(self):
        """ 初始化小部件 """
        # 设置布局
        self.hBox.addWidget(self.indicator)
        self.hBox.addWidget(self.label)
        self.hBox.setSpacing(self.__spacing)
        self.hBox.setAlignment(Qt.AlignLeft)
        self.setAttribute(Qt.WA_StyledBackground)
        self.hBox.setContentsMargins(0, 0, 0, 0)
        # 设置默认样式
        with open('resource/switch_button.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())
        # 信号连接到槽
        self.indicator.checkedChanged.connect(self.checkedChanged)

    def isChecked(self):
        return self.indicator.isChecked()

    def setChecked(self, isChecked: bool):
        """ 设置选中状态 """
        self.indicator.setChecked(isChecked)

    def toggleChecked(self):
        """ 切换选中状态 """
        self.indicator.setChecked(not self.indicator.isChecked())

    def setText(self, text: str):
        self.text = text
        self.label.setText(text)
        self.adjustSize()

    def getSpacing(self):
        return self.__spacing

    def setSpacing(self, spacing: int):
        self.__spacing = spacing
        self.hBox.setSpacing(spacing)
        self.update()

    spacing = pyqtProperty(int, getSpacing, setSpacing)
