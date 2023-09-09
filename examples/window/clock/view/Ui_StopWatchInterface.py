# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'StopWatchInterface.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, PillToolButton, TitleLabel, ToggleToolButton,
    ToolButton)

class Ui_StopWatchInterface(object):
    def setupUi(self, StopWatchInterface):
        if not StopWatchInterface.objectName():
            StopWatchInterface.setObjectName(u"StopWatchInterface")
        StopWatchInterface.resize(867, 781)
        self.verticalLayout_2 = QVBoxLayout(StopWatchInterface)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.timeLabel = BodyLabel(StopWatchInterface)
        self.timeLabel.setObjectName(u"timeLabel")
        self.timeLabel.setProperty("lightColor", QColor(96, 96, 96))
        self.timeLabel.setProperty("darkColor", QColor(206, 206, 206))
        self.timeLabel.setProperty("pixelFontSize", 100)

        self.verticalLayout.addWidget(self.timeLabel, 0, Qt.AlignHCenter)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_4)

        self.hourLabel = TitleLabel(StopWatchInterface)
        self.hourLabel.setObjectName(u"hourLabel")
        self.hourLabel.setProperty("lightColor", QColor(96, 96, 96))
        self.hourLabel.setProperty("darkColor", QColor(206, 206, 206))

        self.horizontalLayout_3.addWidget(self.hourLabel)

        self.horizontalSpacer_6 = QSpacerItem(60, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_6)

        self.minuteLabel = TitleLabel(StopWatchInterface)
        self.minuteLabel.setObjectName(u"minuteLabel")
        self.minuteLabel.setProperty("lightColor", QColor(96, 96, 96))
        self.minuteLabel.setProperty("darkColor", QColor(206, 206, 206))

        self.horizontalLayout_3.addWidget(self.minuteLabel)

        self.horizontalSpacer_7 = QSpacerItem(90, 17, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_7)

        self.secondLabel = TitleLabel(StopWatchInterface)
        self.secondLabel.setObjectName(u"secondLabel")
        self.secondLabel.setProperty("lightColor", QColor(96, 96, 96))
        self.secondLabel.setProperty("darkColor", QColor(206, 206, 206))

        self.horizontalLayout_3.addWidget(self.secondLabel)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer_5)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.verticalSpacer_3 = QSpacerItem(20, 50, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(24)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.startButton = PillToolButton(StopWatchInterface)
        self.startButton.setObjectName(u"startButton")
        self.startButton.setMinimumSize(QSize(68, 68))
        self.startButton.setIconSize(QSize(21, 21))
        self.startButton.setChecked(True)

        self.horizontalLayout_2.addWidget(self.startButton)

        self.flagButton = PillToolButton(StopWatchInterface)
        self.flagButton.setObjectName(u"flagButton")
        self.flagButton.setEnabled(False)
        self.flagButton.setMinimumSize(QSize(68, 68))
        self.flagButton.setIconSize(QSize(21, 21))

        self.horizontalLayout_2.addWidget(self.flagButton)

        self.restartButton = PillToolButton(StopWatchInterface)
        self.restartButton.setObjectName(u"restartButton")
        self.restartButton.setEnabled(False)
        self.restartButton.setMinimumSize(QSize(68, 68))
        self.restartButton.setIconSize(QSize(21, 21))

        self.horizontalLayout_2.addWidget(self.restartButton)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_2)


        self.verticalLayout_2.addLayout(self.verticalLayout)


        self.retranslateUi(StopWatchInterface)

        QMetaObject.connectSlotsByName(StopWatchInterface)
    # setupUi

    def retranslateUi(self, StopWatchInterface):
        StopWatchInterface.setWindowTitle(QCoreApplication.translate("StopWatchInterface", u"Form", None))
        self.timeLabel.setText(QCoreApplication.translate("StopWatchInterface", u"00:00:00", None))
        self.hourLabel.setText(QCoreApplication.translate("StopWatchInterface", u"\u5c0f\u65f6", None))
        self.minuteLabel.setText(QCoreApplication.translate("StopWatchInterface", u"\u5206\u949f", None))
        self.secondLabel.setText(QCoreApplication.translate("StopWatchInterface", u"\u79d2", None))
    # retranslateUi

