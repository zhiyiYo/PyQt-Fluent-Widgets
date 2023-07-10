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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLayout, QProgressBar,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, CardWidget, CheckBox, LargeTitleLabel,
    PrimaryPushButton, ProgressBar, ProgressRing, PushButton,
    StrongBodyLabel, SubtitleLabel, TimePicker, ToolButton,
    TransparentToolButton)

class Ui_FocusInterface(object):
    def setupUi(self, FocusInterface):
        if not FocusInterface.objectName():
            FocusInterface.setObjectName(u"FocusInterface")
        FocusInterface.resize(911, 807)
        self.horizontalLayout_3 = QHBoxLayout(FocusInterface)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(12)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetFixedSize)
        self.horizontalLayout.setContentsMargins(32, 40, 32, -1)
        self.focusCard = CardWidget(FocusInterface)
        self.focusCard.setObjectName(u"focusCard")
        self.focusCard.setMinimumSize(QSize(380, 424))
        self.focusCard.setMaximumSize(QSize(410, 424))
        self.focusCard.setStyleSheet(u"")
        self.verticalLayout_3 = QVBoxLayout(self.focusCard)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
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

        self.verticalSpacer_13 = QSpacerItem(20, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_13)

        self.hintLabel = BodyLabel(self.focusCard)
        self.hintLabel.setObjectName(u"hintLabel")
        self.hintLabel.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.hintLabel)

        self.verticalSpacer_2 = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.verticalLayout.addItem(self.verticalSpacer_2)

        self.timePicker = TimePicker(self.focusCard)
        self.timePicker.setObjectName(u"timePicker")

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


        self.horizontalLayout.addWidget(self.focusCard, 0, Qt.AlignLeft|Qt.AlignTop)

        self.progressCard = CardWidget(FocusInterface)
        self.progressCard.setObjectName(u"progressCard")
        self.progressCard.setMinimumSize(QSize(380, 424))
        self.progressCard.setMaximumSize(QSize(410, 424))
        self.verticalLayout_4 = QVBoxLayout(self.progressCard)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(5, -1, -1, -1)
        self.dailyProgressLabel = StrongBodyLabel(self.progressCard)
        self.dailyProgressLabel.setObjectName(u"dailyProgressLabel")

        self.horizontalLayout_4.addWidget(self.dailyProgressLabel)

        self.editButton = TransparentToolButton(self.progressCard)
        self.editButton.setObjectName(u"editButton")

        self.horizontalLayout_4.addWidget(self.editButton, 0, Qt.AlignRight)


        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.verticalSpacer_8 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_8)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
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

        self.progressRing = ProgressRing(self.progressCard)
        self.progressRing.setObjectName(u"progressRing")
        self.progressRing.setMinimumSize(QSize(150, 150))
        self.progressRing.setMaximumSize(QSize(150, 150))
        font = QFont()
        font.setFamilies([u"Microsoft YaHei UI"])
        font.setPointSize(10)
        font.setBold(False)
        self.progressRing.setFont(font)
        self.progressRing.setMaximum(24)
        self.progressRing.setValue(10)
        self.progressRing.setTextVisible(True)
        self.progressRing.setOrientation(Qt.Horizontal)
        self.progressRing.setTextDirection(QProgressBar.TopToBottom)
        self.progressRing.setUseAni(False)
        self.progressRing.setVal(10.000000000000000)
        self.progressRing.setStrokeWidth(15)

        self.horizontalLayout_5.addWidget(self.progressRing)

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


        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.finishTimeLabel = BodyLabel(self.progressCard)
        self.finishTimeLabel.setObjectName(u"finishTimeLabel")

        self.verticalLayout_2.addWidget(self.finishTimeLabel, 0, Qt.AlignHCenter)

        self.verticalSpacer_7 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_7)


        self.verticalLayout_4.addLayout(self.verticalLayout_2)


        self.horizontalLayout.addWidget(self.progressCard, 0, Qt.AlignLeft|Qt.AlignTop)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.horizontalLayout_3.addLayout(self.horizontalLayout)


        self.retranslateUi(FocusInterface)

        QMetaObject.connectSlotsByName(FocusInterface)
    # setupUi

    def retranslateUi(self, FocusInterface):
        FocusInterface.setWindowTitle(QCoreApplication.translate("FocusInterface", u"Form", None))
        self.prepareFocusLabel.setText(QCoreApplication.translate("FocusInterface", u"\u51c6\u5907\u4e13\u6ce8", None))
        self.hintLabel.setText(QCoreApplication.translate("FocusInterface", u"\u6211\u4eec\u5c06\u5728\u6bcf\u4e2a\u4f1a\u8bdd\u671f\u95f4\u5173\u95ed\u901a\u77e5\u548c\u5e94\u7528\u8b66\u62a5\u3002\u5bf9\u4e8e\n"
"\u8f83\u957f\u7684\u4f1a\u8bdd\uff0c\u6211\u4eec\u5c06\u6dfb\u52a0\u7b80\u77ed\u7684\u4f11\u606f\u65f6\u95f4\uff0c\u4ee5\u4fbf\u4f60\n"
"\u53ef\u4ee5\u6062\u590d\u7cbe\u529b\u3002", None))
        self.bottomHintLabel.setText(QCoreApplication.translate("FocusInterface", u"\u4f60\u5c06\u6ca1\u6709\u4f11\u606f\u65f6\u95f4\u3002", None))
        self.skipRelaxCheckBox.setText(QCoreApplication.translate("FocusInterface", u"\u8df3\u8fc7\u4f11\u606f", None))
        self.startFocusButton.setText(QCoreApplication.translate("FocusInterface", u"\u542f\u52a8\u4e13\u6ce8\u65f6\u6bb5", None))
        self.dailyProgressLabel.setText(QCoreApplication.translate("FocusInterface", u"\u6bcf\u65e5\u8fdb\u5ea6", None))
        self.yesterdayLabel.setText(QCoreApplication.translate("FocusInterface", u"\u6628\u5929", None))
        self.yesterdayTimeLabel.setText(QCoreApplication.translate("FocusInterface", u"0", None))
        self.minuteLabel1.setText(QCoreApplication.translate("FocusInterface", u"\u5206\u949f", None))
        self.progressRing.setFormat(QCoreApplication.translate("FocusInterface", u"\u76ee\u6807 %v \u5c0f\u65f6", None))
        self.continousComplianceDayLabel.setText(QCoreApplication.translate("FocusInterface", u"\u8fde\u7eed\u8fbe\u6807\u65e5", None))
        self.compianceDayLabel.setText(QCoreApplication.translate("FocusInterface", u"0", None))
        self.dayLabel.setText(QCoreApplication.translate("FocusInterface", u"\u5929", None))
        self.finishTimeLabel.setText(QCoreApplication.translate("FocusInterface", u"\u5df2\u5b8c\u6210\uff1a0 \u5206\u949f", None))
    # retranslateUi

