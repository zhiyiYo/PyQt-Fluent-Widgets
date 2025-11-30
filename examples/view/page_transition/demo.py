# coding:utf-8
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QFrame, QGridLayout
from qfluentwidgets import (TransitionStackedWidget, TransitionType, RadioButton, PushButton,
                            BodyLabel, SubtitleLabel, TitleLabel, isDarkTheme, themeColor)
from qframelesswindow import FramelessWindow, StandardTitleBar

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

        title = TitleLabel('Lorem ipsum dolor sit amet, consectetur adipiscing elit', self)
        title.setWordWrap(True)
        vbox.addWidget(title)

        body = BodyLabel(LOREM, self)
        body.setWordWrap(True)
        vbox.addWidget(body)
        vbox.addStretch(1)

        layout.addLayout(vbox, 1)


class Window(FramelessWindow):

    def __init__(self):
        super().__init__()
        self.setTitleBar(StandardTitleBar(self))
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), 'resource/logo.png')))
        self._backStack = []

        container = QWidget(self)
        container.setStyleSheet(f'background: {"#202020" if isDarkTheme() else "#f3f3f3"};')
        layout = QHBoxLayout(container)
        layout.setContentsMargins(24, 24, 24, 24), layout.setSpacing(24)

        # TransitionStackedWidget: WinUI 3 style page transitions
        # API:
        #   setCurrentIndex(index, transition=None, duration=None, isBack=False)
        #   setCurrentWidget(widget, transition=None, duration=None, isBack=False)
        #   setDefaultTransition(TransitionType)  - set default transition type
        #   setAnimationEnabled(bool)             - enable/disable animation
        self.stack = TransitionStackedWidget(self)
        self.stack.setMinimumHeight(500)
        self.stack.addWidget(SamplePage1(self))
        self.stack.addWidget(SamplePage2(self))
        layout.addWidget(self.stack, 1)

        # control panel
        self.ctrl = QWidget(self)
        self.ctrl.setFixedWidth(260)
        ctrlLayout = QVBoxLayout(self.ctrl)
        ctrlLayout.setContentsMargins(16, 16, 16, 16), ctrlLayout.setSpacing(8)
        ctrlLayout.addWidget(SubtitleLabel('Transition modes', self.ctrl))

        # transition type selection
        # Available types: DEFAULT, ENTRANCE, DRILL_IN, SUPPRESS, SLIDE_RIGHT, SLIDE_LEFT
        self.modes = [
            ('Default', TransitionType.DEFAULT),
            ('Entrance', TransitionType.ENTRANCE),
            ('DrillIn', TransitionType.DRILL_IN),
            ('Suppress', TransitionType.SUPPRESS),
            ('Slide from Right', TransitionType.SLIDE_RIGHT),
            ('Slide from Left', TransitionType.SLIDE_LEFT),
        ]
        self.radios = []
        for i, (name, _) in enumerate(self.modes):
            r = RadioButton(name, self.ctrl)
            self.radios.append(r)
            ctrlLayout.addWidget(r)
            if i == 0:
                r.setChecked(True)

        ctrlLayout.addSpacing(16)
        ctrlLayout.addWidget(SubtitleLabel('Navigate', self.ctrl))

        # navigation buttons
        self.fwdBtn = PushButton('Navigate Forward', self.ctrl)
        self.bwdBtn = PushButton('Navigate Backward', self.ctrl)
        ctrlLayout.addWidget(self.fwdBtn)
        ctrlLayout.addWidget(self.bwdBtn)
        ctrlLayout.addStretch(1)

        layout.addWidget(self.ctrl, 0, Qt.AlignTop)

        self.fwdBtn.clicked.connect(self._onForward)
        self.bwdBtn.clicked.connect(self._onBackward)

        self.setLayout(QVBoxLayout(self))
        self.layout().setContentsMargins(0, self.titleBar.height(), 0, 0)
        self.layout().addWidget(container)
        self.resize(1000, 700)
        self.setWindowTitle('Page Transitions')
        d = QApplication.desktop().availableGeometry()
        self.move((d.width()-self.width())//2, (d.height()-self.height())//2)

    def _getTransitionType(self):
        return next((t for r, (_, t) in zip(self.radios, self.modes) if r.isChecked()), TransitionType.DEFAULT)

    def _onForward(self):
        self._backStack.append(self.stack.currentIndex())

        # forward navigation: pass transition type (or None to use default)
        self.stack.setCurrentIndex(
            (self.stack.currentIndex() + 1) % self.stack.count(),
            self._getTransitionType()
        )

    def _onBackward(self):
        if not self._backStack:
            return

        # back navigation: set isBack=True to reverse animation direction
        self.stack.setCurrentIndex(
            self._backStack.pop(),
            self._getTransitionType(),
            isBack=True
        )


if __name__ == '__main__':
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    Window().show()
    app.exec_()
