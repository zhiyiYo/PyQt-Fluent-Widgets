# coding:utf-8
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout

from qfluentwidgets import InfoBadge, InfoLevel, setTheme, Theme


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        # setTheme(Theme.DARK)

        self.hBoxLayout = QHBoxLayout(self)
        self.infoBadge = InfoBadge.info(1, self)
        self.successBadge = InfoBadge.success(10, self)
        self.attensionBadge = InfoBadge.attension(100, self)
        self.warningBadge = InfoBadge.warning(1000, self)
        self.errorBadge = InfoBadge.error(10000, self)
        self.customBadge = InfoBadge.custom('1w+', '#005fb8', '#60cdff', self)

        self.hBoxLayout.setSizeConstraint(QHBoxLayout.SizeConstraint.SetMinimumSize)
        self.hBoxLayout.addStretch(1)

        for w in self.findChildren(InfoBadge):
            self.hBoxLayout.addWidget(w, 0, Qt.AlignmentFlag.AlignHCenter)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.setSpacing(20)
        self.resize(450, 400)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()