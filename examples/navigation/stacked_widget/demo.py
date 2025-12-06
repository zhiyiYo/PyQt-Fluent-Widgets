# coding:utf-8
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout, QStackedWidget, QButtonGroup
from qfluentwidgets import (DrillInTransitionStackedWidget, EntranceTransitionStackedWidget, RadioButton, PushButton,
                            BodyLabel, SubtitleLabel, TitleLabel, isDarkTheme, themeColor)

LOREM = ('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et '
         'dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip '
         'ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu '
         'fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt '
         'mollit anim id est laborum.')


class ColorBlock(QFrame):
    def __init__(self, color, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f'background: {color.name()};')


class SamplePage1(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QGridLayout(self)
        layout.setContentsMargins(6, 6, 6, 6), layout.setSpacing(6)

        # blue accent block (left, spans 2 rows)
        accent = ColorBlock(themeColor(), self)
        accent.setMinimumWidth(200)
        layout.addWidget(accent, 0, 0, 2, 1)

        # gray blocks (right side 2x2 grid)
        darkGray = ColorBlock(QColor(128, 128, 128), self)
        lightGray1 = ColorBlock(QColor(192, 192, 192), self)
        lightGray2 = ColorBlock(QColor(192, 192, 192), self)
        darkGray2 = ColorBlock(QColor(160, 160, 160), self)

        for blk in [darkGray, lightGray1, lightGray2, darkGray2]:
            blk.setMinimumHeight(120)

        layout.addWidget(darkGray, 0, 1)
        layout.addWidget(lightGray1, 0, 2)
        layout.addWidget(lightGray2, 1, 1)
        layout.addWidget(darkGray2, 1, 2)

        # text at bottom
        lbl = BodyLabel(LOREM, self)
        lbl.setWordWrap(True)
        layout.addWidget(lbl, 2, 0, 1, 3)

        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 1)


class SamplePage2(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(6, 6, 6, 6), layout.setSpacing(16)
        layout.setAlignment(Qt.AlignTop)

        # blue accent block (left)
        accent = ColorBlock(themeColor(), self)
        accent.setFixedSize(140, 180)
        layout.addWidget(accent, 0, Qt.AlignTop)

        # text content (right)
        vbox = QVBoxLayout()
        vbox.setSpacing(8)
        vbox.setContentsMargins(0, 0, 0, 0)

        title = TitleLabel(
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit', self)
        title.setWordWrap(True)
        vbox.addWidget(title)

        body = BodyLabel(LOREM, self)
        body.setWordWrap(True)
        vbox.addWidget(body)
        vbox.addStretch(1)

        layout.addLayout(vbox, 1)


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self._backStack = []

        self.stackedWidget = QStackedWidget(self)
        self.hBoxLayout = QHBoxLayout(self)

        # entrance
        self.entranceStackedWidget = EntranceTransitionStackedWidget()
        self.entranceStackedWidget.setMinimumHeight(500)
        self.entranceStackedWidget.addWidget(SamplePage1())
        self.entranceStackedWidget.addWidget(SamplePage2())
        self.stackedWidget.addWidget(self.entranceStackedWidget)

        # drill in
        self.drillInStackedWidget = DrillInTransitionStackedWidget()
        self.drillInStackedWidget.setMinimumHeight(500)
        self.drillInStackedWidget.addWidget(SamplePage1())
        self.drillInStackedWidget.addWidget(SamplePage2())
        self.stackedWidget.addWidget(self.drillInStackedWidget)

        # control panel
        self.createControlPanel()

        self.hBoxLayout.addWidget(self.stackedWidget, 1)
        self.hBoxLayout.addWidget(self.ctrlPanel, 0)

        self.fwdBtn.clicked.connect(self._onForward)
        self.bwdBtn.clicked.connect(self._onBackward)
        self.buttonGroup.idClicked.connect(lambda : self.stackedWidget.setCurrentIndex(self.buttonGroup.checkedButton().property('index')))

        self.resize(800, 700)

    def createControlPanel(self):
        self.ctrlPanel = QWidget(self)
        self.buttonGroup = QButtonGroup(self)

        self.ctrlPanel.setFixedWidth(260)

        layout = QVBoxLayout(self.ctrlPanel)
        layout.addWidget(SubtitleLabel('Transition modes', self.ctrlPanel))

        # transition type selection
        self.modes = [
            ('Entrance', self.entranceStackedWidget),
            ('DrillIn', self.drillInStackedWidget),
        ]

        for i, (name, widget) in enumerate(self.modes):
            button = RadioButton(name, self.ctrlPanel)
            button.setProperty("index", i)
            self.buttonGroup.addButton(button)

            layout.addWidget(button)
            if i == 0:
                button.setChecked(True)

        layout.addSpacing(16)
        layout.addWidget(SubtitleLabel('Navigate', self.ctrlPanel))
        layout.setContentsMargins(16, 16, 16, 16), layout.setSpacing(8)

        # navigation buttons
        self.fwdBtn = PushButton('Navigate Forward', self.ctrlPanel)
        self.bwdBtn = PushButton('Navigate Backward', self.ctrlPanel)
        layout.addWidget(self.fwdBtn)
        layout.addWidget(self.bwdBtn)
        layout.addStretch(1)

    def _onForward(self):
        stack = self.stackedWidget.currentWidget()
        self._backStack.append(stack.currentIndex())

        stack.setCurrentIndex((stack.currentIndex() + 1) % stack.count())

    def _onBackward(self):
        if not self._backStack:
            return

        stack = self.stackedWidget.currentWidget()
        stack.setCurrentIndex(self._backStack.pop(), isBack=True)


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec_()
