# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FocusInterface.ui'
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QLayout,
    QProgressBar, QSizePolicy, QSpacerItem, QVBoxLayout,
    QWidget)

from qfluentwidgets import (BodyLabel, CardWidget, CheckBox, IconWidget,
    LargeTitleLabel, PrimaryPushButton, ProgressBar, ProgressRing,
    PushButton, StrongBodyLabel, SubtitleLabel, TimePicker,
    ToolButton, TransparentToolButton)
import resource_rc

class Ui_FocusInterface(object):
    def setupUi(self, FocusInterface):
        if not FocusInterface.objectName():
            FocusInterface.setObjectName(u"FocusInterface")
        FocusInterface.resize(911, 807)
        self.horizontalLayout_3 = QHBoxLayout(FocusInterface)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(12)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.gridLayout.setContentsMargins(20, 40, 20, 20)
        self.progressCard = CardWidget(FocusInterface)
        self.progressCard.setObjectName(u"progressCard")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressCard.sizePolicy().hasHeightForWidth())
        self.progressCard.setSizePolicy(sizePolicy)
        self.progressCard.setMinimumSize(QSize(380, 410))
        self.progressCard.setMaximumSize(QSize(600, 410))
        self.verticalLayout_4 = QVBoxLayout(self.progressCard)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(5, -1, -1, -1)
        self.progressIcon = IconWidget(self.progressCard)
        self.progressIcon.setObjectName(u"progressIcon")
        self.progressIcon.setMinimumSize(QSize(18, 18))
        self.progressIcon.setMaximumSize(QSize(18, 18))
        icon = QIcon()
        icon.addFile(u":/images/tips.png", QSize(), QIcon.Normal, QIcon.Off)
        self.progressIcon.setIcon(icon)

        self.horizontalLayout_4.addWidget(self.progressIcon)

        self.horizontalSpacer_8 = QSpacerItem(2, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_8)

        self.dailyProgressLabel = StrongBodyLabel(self.progressCard)
        self.dailyProgressLabel.setObjectName(u"dailyProgressLabel")

        self.horizontalLayout_4.addWidget(self.dailyProgressLabel)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer_9)

        self.editButton = TransparentToolButton(self.progressCard)
        self.editButton.setObjectName(u"editButton")

        self.horizontalLayout_4.addWidget(self.editButton, 0, Qt.AlignRight)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setSizeConstraint(QLayout.SetMinAndMaxSize)
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_5)

        self.yesterdayLabel = BodyLabel(self.progressCard)
        self.yesterdayLabel.setObjectName(u"yesterdayLabel")

        self.verticalLayout_5.addWidget(self.yesterdayLabel, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.yesterdayTimeLabel = LargeTitleLabel(self.progressCard)
        self.yesterdayTimeLabel.setObjectName(u"yesterdayTimeLabel")

        self.verticalLayout_5.addWidget(self.yesterdayTimeLabel, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.minuteLabel1 = BodyLabel(self.progressCard)
        self.minuteLabel1.setObjectName(u"minuteLabel1")

        self.verticalLayout_5.addWidget(self.minuteLabel1, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_6)


        self.horizontalLayout_5.addLayout(self.verticalLayout_5)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalSpacer_15 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_15)

        self.targetLabel = SubtitleLabel(self.progressCard)
        self.targetLabel.setObjectName(u"targetLabel")
        self.targetLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout_10.addWidget(self.targetLabel)

        self.progressRing = ProgressRing(self.progressCard)
        self.progressRing.setObjectName(u"progressRing")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.progressRing.sizePolicy().hasHeightForWidth())
        self.progressRing.setSizePolicy(sizePolicy1)
        self.progressRing.setMinimumSize(QSize(150, 150))
        self.progressRing.setMaximumSize(QSize(220, 220))
        font = QFont()
        font.setFamilies([u"Microsoft YaHei UI"])
        font.setPointSize(10)
        font.setBold(False)
        self.progressRing.setFont(font)
        self.progressRing.setMaximum(24)
        self.progressRing.setValue(10)
        self.progressRing.setAlignment(Qt.AlignCenter)
        self.progressRing.setTextVisible(True)
        self.progressRing.setOrientation(Qt.Horizontal)
        self.progressRing.setTextDirection(QProgressBar.TopToBottom)
        self.progressRing.setUseAni(False)
        self.progressRing.setVal(10.000000000000000)
        self.progressRing.setStrokeWidth(15)

        self.verticalLayout_10.addWidget(self.progressRing)

        self.verticalSpacer_16 = QSpacerItem(20, 3, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_10.addItem(self.verticalSpacer_16)

        self.finishTimeLabel = BodyLabel(self.progressCard)
        self.finishTimeLabel.setObjectName(u"finishTimeLabel")

        self.verticalLayout_10.addWidget(self.finishTimeLabel, 0, Qt.AlignHCenter)

        self.verticalSpacer_13 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer_13)

        self.verticalLayout_10.setStretch(2, 1)

        self.horizontalLayout_5.addLayout(self.verticalLayout_10)

        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalSpacer_9 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_9)

        self.continousComplianceDayLabel = BodyLabel(self.progressCard)
        self.continousComplianceDayLabel.setObjectName(u"continousComplianceDayLabel")

        self.verticalLayout_6.addWidget(self.continousComplianceDayLabel, 0, Qt.AlignHCenter|Qt.AlignVCenter)

        self.compianceDayLabel = LargeTitleLabel(self.progressCard)
        self.compianceDayLabel.setObjectName(u"compianceDayLabel")

        self.verticalLayout_6.addWidget(self.compianceDayLabel, 0, Qt.AlignHCenter)

        self.dayLabel = BodyLabel(self.progressCard)
        self.dayLabel.setObjectName(u"dayLabel")

        self.verticalLayout_6.addWidget(self.dayLabel, 0, Qt.AlignHCenter)

        self.verticalSpacer_10 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_6.addItem(self.verticalSpacer_10)


        self.horizontalLayout_5.addLayout(self.verticalLayout_6)

        self.horizontalLayout_5.setStretch(0, 1)
        self.horizontalLayout_5.setStretch(1, 2)
        self.horizontalLayout_5.setStretch(2, 1)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)


        self.gridLayout.addWidget(self.progressCard, 0, 1, 1, 1)

        self.focusCard = CardWidget(FocusInterface)
        self.focusCard.setObjectName(u"focusCard")
        sizePolicy.setHeightForWidth(self.focusCard.sizePolicy().hasHeightForWidth())
        self.focusCard.setSizePolicy(sizePolicy)
        self.focusCard.setMinimumSize(QSize(380, 410))
        self.focusCard.setMaximumSize(QSize(600, 410))
        self.focusCard.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(self.focusCard)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, -1, -1, -1)
        self.focusCardIcon = IconWidget(self.focusCard)
        self.focusCardIcon.setObjectName(u"focusCardIcon")
        self.focusCardIcon.setMinimumSize(QSize(20, 20))
        self.focusCardIcon.setMaximumSize(QSize(20, 20))
        icon1 = QIcon()
        icon1.addFile(u":/images/alarms.png", QSize(), QIcon.Normal, QIcon.Off)
        self.focusCardIcon.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.focusCardIcon)

        self.focusPeriodLabel = StrongBodyLabel(self.focusCard)
        self.focusPeriodLabel.setObjectName(u"focusPeriodLabel")

        self.horizontalLayout_2.addWidget(self.focusPeriodLabel)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pinButton = TransparentToolButton(self.focusCard)
        self.pinButton.setObjectName(u"pinButton")

        self.horizontalLayout_2.addWidget(self.pinButton)

        self.moreButton = TransparentToolButton(self.focusCard)
        self.moreButton.setObjectName(u"moreButton")

        self.horizontalLayout_2.addWidget(self.moreButton)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.verticalSpacer_12 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_12)

        self.prepareFocusLabel = SubtitleLabel(self.focusCard)
        self.prepareFocusLabel.setObjectName(u"prepareFocusLabel")
        self.prepareFocusLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.prepareFocusLabel)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(15, 10, 15, -1)
        self.hintLabel = BodyLabel(self.focusCard)
        self.hintLabel.setObjectName(u"hintLabel")
        self.hintLabel.setAlignment(Qt.AlignCenter)
        self.hintLabel.setWordWrap(True)
        self.hintLabel.setMargin(0)
        self.hintLabel.setProperty("lightColor", QColor(96, 96, 96))
        self.hintLabel.setProperty("darkColor", QColor(206, 206, 206))

        self.horizontalLayout_6.addWidget(self.hintLabel)


        self.verticalLayout.addLayout(self.horizontalLayout_6)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.timePicker = TimePicker(self.focusCard)
        self.timePicker.setObjectName(u"timePicker")
        self.timePicker.setSecondVisible(True)

        self.verticalLayout.addWidget(self.timePicker, 0, Qt.AlignHCenter)

        self.verticalSpacer_3 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_3)

        self.bottomHintLabel = BodyLabel(self.focusCard)
        self.bottomHintLabel.setObjectName(u"bottomHintLabel")
        self.bottomHintLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.bottomHintLabel, 0, Qt.AlignHCenter)

        self.verticalSpacer_11 = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_11)

        self.skipRelaxCheckBox = CheckBox(self.focusCard)
        self.skipRelaxCheckBox.setObjectName(u"skipRelaxCheckBox")
        self.skipRelaxCheckBox.setEnabled(True)

        self.verticalLayout.addWidget(self.skipRelaxCheckBox, 0, Qt.AlignHCenter)

        self.verticalSpacer_4 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_4)

        self.startFocusButton = PrimaryPushButton(self.focusCard)
        self.startFocusButton.setObjectName(u"startFocusButton")
        self.startFocusButton.setAutoDefault(True)

        self.verticalLayout.addWidget(self.startFocusButton, 0, Qt.AlignHCenter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.verticalLayout_3.addLayout(self.verticalLayout)


        self.gridLayout.addWidget(self.focusCard, 0, 0, 1, 1)

        self.taskCard = CardWidget(FocusInterface)
        self.taskCard.setObjectName(u"taskCard")
        self.taskCard.setMinimumSize(QSize(370, 0))
        self.taskCard.setMaximumSize(QSize(600, 395))
        self.verticalLayout_8 = QVBoxLayout(self.taskCard)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(8, -1, -1, -1)
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.taskCardIcon = IconWidget(self.taskCard)
        self.taskCardIcon.setObjectName(u"taskCardIcon")
        self.taskCardIcon.setMinimumSize(QSize(18, 18))
        self.taskCardIcon.setMaximumSize(QSize(18, 18))
        icon2 = QIcon()
        icon2.addFile(u":/images/todo.png", QSize(), QIcon.Normal, QIcon.Off)
        self.taskCardIcon.setIcon(icon2)

        self.horizontalLayout_7.addWidget(self.taskCardIcon)

        self.horizontalSpacer_7 = QSpacerItem(2, 2, QSizePolicy.Fixed, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_7)

        self.taskLabel = StrongBodyLabel(self.taskCard)
        self.taskLabel.setObjectName(u"taskLabel")

        self.horizontalLayout_7.addWidget(self.taskLabel)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_7.addItem(self.horizontalSpacer_3)

        self.addTaskButton = TransparentToolButton(self.taskCard)
        self.addTaskButton.setObjectName(u"addTaskButton")

        self.horizontalLayout_7.addWidget(self.addTaskButton)

        self.moreTaskButton = TransparentToolButton(self.taskCard)
        self.moreTaskButton.setObjectName(u"moreTaskButton")

        self.horizontalLayout_7.addWidget(self.moreTaskButton)


        self.verticalLayout_7.addLayout(self.horizontalLayout_7)

        self.verticalSpacer_8 = QSpacerItem(20, 3, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout_7.addItem(self.verticalSpacer_8)

        self.hintLabel_2 = BodyLabel(self.taskCard)
        self.hintLabel_2.setObjectName(u"hintLabel_2")
        self.hintLabel_2.setProperty("lightColor", QColor(96, 96, 96))
        self.hintLabel_2.setProperty("darkColor", QColor(206, 206, 206))

        self.verticalLayout_7.addWidget(self.hintLabel_2)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(-1, -1, 7, -1)
        self.taskCard1 = CardWidget(self.taskCard)
        self.taskCard1.setObjectName(u"taskCard1")
        self.taskCard1.setMinimumSize(QSize(0, 44))
        self.taskCard1.setMaximumSize(QSize(16777215, 44))
        self.horizontalLayout_9 = QHBoxLayout(self.taskCard1)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(15, -1, -1, -1)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.taskIcon1 = IconWidget(self.taskCard1)
        self.taskIcon1.setObjectName(u"taskIcon1")
        sizePolicy2 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(16)
        sizePolicy2.setVerticalStretch(16)
        sizePolicy2.setHeightForWidth(self.taskIcon1.sizePolicy().hasHeightForWidth())
        self.taskIcon1.setSizePolicy(sizePolicy2)
        self.taskIcon1.setMinimumSize(QSize(16, 16))
        self.taskIcon1.setMaximumSize(QSize(16, 16))

        self.horizontalLayout_8.addWidget(self.taskIcon1)


        self.horizontalLayout_9.addLayout(self.horizontalLayout_8)

        self.taskLabel1 = BodyLabel(self.taskCard1)
        self.taskLabel1.setObjectName(u"taskLabel1")
        self.taskLabel1.setProperty("pixelFontSize", 14)
        self.taskLabel1.setProperty("strikeOut", True)

        self.horizontalLayout_9.addWidget(self.taskLabel1)

        self.horizontalSpacer_4 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_9.addItem(self.horizontalSpacer_4)


        self.verticalLayout_9.addWidget(self.taskCard1)

        self.taskCard2 = CardWidget(self.taskCard)
        self.taskCard2.setObjectName(u"taskCard2")
        self.taskCard2.setMinimumSize(QSize(0, 44))
        self.taskCard2.setMaximumSize(QSize(16777215, 44))
        self.horizontalLayout_12 = QHBoxLayout(self.taskCard2)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(15, -1, -1, -1)
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.taskIcon2 = IconWidget(self.taskCard2)
        self.taskIcon2.setObjectName(u"taskIcon2")
        sizePolicy2.setHeightForWidth(self.taskIcon2.sizePolicy().hasHeightForWidth())
        self.taskIcon2.setSizePolicy(sizePolicy2)
        self.taskIcon2.setMinimumSize(QSize(16, 16))
        self.taskIcon2.setMaximumSize(QSize(16, 16))

        self.horizontalLayout_13.addWidget(self.taskIcon2)


        self.horizontalLayout_12.addLayout(self.horizontalLayout_13)

        self.taskLabel2 = BodyLabel(self.taskCard2)
        self.taskLabel2.setObjectName(u"taskLabel2")

        self.horizontalLayout_12.addWidget(self.taskLabel2)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_12.addItem(self.horizontalSpacer_6)


        self.verticalLayout_9.addWidget(self.taskCard2)

        self.taskCard3 = CardWidget(self.taskCard)
        self.taskCard3.setObjectName(u"taskCard3")
        self.taskCard3.setMinimumSize(QSize(0, 44))
        self.taskCard3.setMaximumSize(QSize(16777215, 44))
        self.horizontalLayout_10 = QHBoxLayout(self.taskCard3)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(15, -1, -1, -1)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.taskIcon3 = IconWidget(self.taskCard3)
        self.taskIcon3.setObjectName(u"taskIcon3")
        sizePolicy2.setHeightForWidth(self.taskIcon3.sizePolicy().hasHeightForWidth())
        self.taskIcon3.setSizePolicy(sizePolicy2)
        self.taskIcon3.setMinimumSize(QSize(16, 16))
        self.taskIcon3.setMaximumSize(QSize(16, 16))

        self.horizontalLayout_11.addWidget(self.taskIcon3)


        self.horizontalLayout_10.addLayout(self.horizontalLayout_11)

        self.taskLabel3 = BodyLabel(self.taskCard3)
        self.taskLabel3.setObjectName(u"taskLabel3")

        self.horizontalLayout_10.addWidget(self.taskLabel3)

        self.horizontalSpacer_5 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout_10.addItem(self.horizontalSpacer_5)


        self.verticalLayout_9.addWidget(self.taskCard3)


        self.verticalLayout_7.addLayout(self.verticalLayout_9)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_7)


        self.verticalLayout_8.addLayout(self.verticalLayout_7)


        self.gridLayout.addWidget(self.taskCard, 1, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 2, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)

        self.horizontalLayout_3.addLayout(self.gridLayout)


        self.retranslateUi(FocusInterface)

        QMetaObject.connectSlotsByName(FocusInterface)
    # setupUi

    def retranslateUi(self, FocusInterface):
        FocusInterface.setWindowTitle(QCoreApplication.translate("FocusInterface", u"Form", None))
        self.dailyProgressLabel.setText(QCoreApplication.translate("FocusInterface", u"\u6bcf\u65e5\u8fdb\u5ea6", None))
        self.yesterdayLabel.setText(QCoreApplication.translate("FocusInterface", u"\u6628\u5929", None))
        self.yesterdayTimeLabel.setText(QCoreApplication.translate("FocusInterface", u"3", None))
        self.minuteLabel1.setText(QCoreApplication.translate("FocusInterface", u"\u5206\u949f", None))
        self.targetLabel.setText(QCoreApplication.translate("FocusInterface", u"\u4eca\u65e5\u8ba1\u5212", None))
        self.progressRing.setFormat(QCoreApplication.translate("FocusInterface", u"\u76ee\u6807 %v \u5c0f\u65f6", None))
        self.finishTimeLabel.setText(QCoreApplication.translate("FocusInterface", u"\u5df2\u5b8c\u6210\uff1a0 \u5206\u949f", None))
        self.continousComplianceDayLabel.setText(QCoreApplication.translate("FocusInterface", u"\u8fde\u7eed\u8fbe\u6807\u65e5", None))
        self.compianceDayLabel.setText(QCoreApplication.translate("FocusInterface", u"5", None))
        self.dayLabel.setText(QCoreApplication.translate("FocusInterface", u"\u5929", None))
        self.focusPeriodLabel.setText(QCoreApplication.translate("FocusInterface", u"\u4e13\u6ce8\u65f6\u6bb5", None))
        self.prepareFocusLabel.setText(QCoreApplication.translate("FocusInterface", u"\u51c6\u5907\u4e13\u6ce8", None))
        self.hintLabel.setText(QCoreApplication.translate("FocusInterface", u"\u6211\u4eec\u5c06\u5728\u6bcf\u4e2a\u4f1a\u8bdd\u671f\u95f4\u5173\u95ed\u901a\u77e5\u548c\u5e94\u7528\u8b66\u62a5\u3002\u5bf9\u4e8e\u8f83\u957f\u7684\u4f1a\u8bdd\uff0c\u6211\u4eec\u5c06\u6dfb\u52a0\u7b80\u77ed\u7684\u4f11\u606f\u65f6\u95f4\uff0c\u4ee5\u4fbf\u4f60\u53ef\u4ee5\u6062\u590d\u7cbe\u529b\u3002", None))
        self.bottomHintLabel.setText(QCoreApplication.translate("FocusInterface", u"\u4f60\u5c06\u6ca1\u6709\u4f11\u606f\u65f6\u95f4\u3002", None))
        self.skipRelaxCheckBox.setText(QCoreApplication.translate("FocusInterface", u"\u8df3\u8fc7\u4f11\u606f", None))
        self.startFocusButton.setText(QCoreApplication.translate("FocusInterface", u"\u542f\u52a8\u4e13\u6ce8\u65f6\u6bb5", None))
        self.taskLabel.setText(QCoreApplication.translate("FocusInterface", u"\u4efb\u52a1", None))
        self.hintLabel_2.setText(QCoreApplication.translate("FocusInterface", u"\u4e3a\u4f1a\u8bdd\u9009\u62e9\u4efb\u52a1", None))
        self.taskLabel1.setText(QCoreApplication.translate("FocusInterface", u"\u5168\u519b\u51fa\u9e21\uff0c\u8a93\u6b7b\u4fdd\u536b\u9e3d\u9e3d\uff01\uff01", None))
        self.taskLabel2.setText(QCoreApplication.translate("FocusInterface", u"\u4e0a\u4f20\u6211\u5bb6 aiko \u7684 MV\u300e\u30b7\u30a2\u30ef\u30bb\u300f", None))
        self.taskLabel3.setText(QCoreApplication.translate("FocusInterface", u"\u4e0b\u8f7d\u6211\u5bb6 aiko \u7684\u65b0\u6b4c\u300e\u8352\u308c\u305f\u5507\u306f\u604b\u3092\u5931\u304f\u3059\u300f", None))
    # retranslateUi

