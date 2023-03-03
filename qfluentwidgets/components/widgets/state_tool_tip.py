# coding:utf-8
from PyQt6.QtCore import QEasingCurve, QPropertyAnimation, Qt, QTimer, pyqtSignal, QSize, QPoint, QRectF
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import QLabel, QWidget, QToolButton, QGraphicsOpacityEffect
from PyQt6.QtSvgWidgets import QSvgWidget

from ...common import setStyleSheet, drawSvgIcon
from ...components.widgets.three_state_button import ThreeStateButton, ButtonState


class StateToolTip(QWidget):
    """ State tooltip """

    closedSignal = pyqtSignal()

    def __init__(self, title, content, parent=None):
        """
        Parameters
        ----------
        title: str
            title of tooltip

        content: str
            content of tooltip

        parant:
            parent window
        """
        super().__init__(parent)
        self.title = title
        self.content = content

        self.titleLabel = QLabel(self.title, self)
        self.contentLabel = QLabel(self.content, self)
        self.rotateTimer = QTimer(self)
        self.closeTimer = QTimer(self)
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.busyIconPath = ":/qfluentwidgets/images/state_tool_tip/running.svg"
        self.doneIconPath = ":/qfluentwidgets/images/state_tool_tip/completed.svg"
        self.closeButton = ThreeStateButton(
            {
                ButtonState.NORMAL: ':/qfluentwidgets/images/state_tool_tip/close_normal.svg',
                ButtonState.HOVER: ':/qfluentwidgets/images/state_tool_tip/close_hover.svg',
                ButtonState.PRESSED: ':/qfluentwidgets/images/state_tool_tip/close_pressed.svg',
            },
            parent=self,
            buttonSize=(12, 12)
        )

        self.isDone = False
        self.rotateAngle = 0
        self.deltaAngle = 20

        self.__initWidget()

    def __initWidget(self):
        """ initialize widgets """
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.rotateTimer.setInterval(50)
        self.closeTimer.setInterval(1000)
        self.contentLabel.setMinimumWidth(200)

        # connect signal to slot
        self.closeButton.clicked.connect(self.__onCloseButtonClicked)
        self.rotateTimer.timeout.connect(self.__rotateTimerFlowSlot)
        self.closeTimer.timeout.connect(self.__slowlyClose)

        self.__setQss()
        self.__initLayout()

        self.rotateTimer.start()

    def __initLayout(self):
        """ initialize layout """
        self.setFixedSize(max(self.titleLabel.width(),
                          self.contentLabel.width()) + 56, 51)
        self.titleLabel.move(32, 9)
        self.contentLabel.move(12, 27)
        self.closeButton.move(self.width() - 24, 19)

    def __setQss(self):
        """ set style sheet """
        self.titleLabel.setObjectName("titleLabel")
        self.contentLabel.setObjectName("contentLabel")

        setStyleSheet(self, 'state_tool_tip')

        self.titleLabel.adjustSize()
        self.contentLabel.adjustSize()

    def setTitle(self, title: str):
        """ set the title of tooltip """
        self.title = title
        self.titleLabel.setText(title)
        self.titleLabel.adjustSize()

    def setContent(self, content: str):
        """ set the content of tooltip """
        self.content = content
        self.contentLabel.setText(content)

        # adjustSize() will mask spinner get stuck
        self.contentLabel.adjustSize()

    def setState(self, isDone=False):
        """ set the state of tooltip """
        self.isDone = isDone
        self.update()
        if self.isDone:
            self.closeTimer.start()

    def __onCloseButtonClicked(self):
        """ close button clicked slot """
        self.closedSignal.emit()
        self.hide()

    def __slowlyClose(self):
        """ fade out """
        self.rotateTimer.stop()
        self.animation.setEasingCurve(QEasingCurve.Type.Linear)
        self.animation.setDuration(500)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.finished.connect(self.deleteLater)
        self.animation.start()

    def __rotateTimerFlowSlot(self):
        """ rotate timer time out slot """
        self.rotateAngle = (self.rotateAngle + self.deltaAngle) % 360
        self.update()

    def paintEvent(self, e):
        """ paint state tooltip """
        super().paintEvent(e)
        painter = QPainter(self)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        if not self.isDone:
            painter.translate(19, 18)
            painter.rotate(self.rotateAngle)
            drawSvgIcon(self.busyIconPath, painter, QRectF(-8, -8, 16, 16))
        else:
            drawSvgIcon(self.doneIconPath, painter, QRectF(11, 10, 16, 16))


class ToastToolTip(QWidget):
    """ Toast tooltip """

    SUCCESS = "completed"
    WARNING = "info"

    def __init__(self, title, content, icon, parent=None):
        """
        Parameters
        ----------
        title: str
            title of tooltip

        content: str
            content of tooltip

        icon: str
            icon of toast, can be `completed` or `info`

        parant:
            parent window
        """
        super().__init__(parent)
        self.title = title
        self.content = content
        self.icon = f":/qfluentwidgets/images/state_tool_tip/{icon}.svg"

        self.titleLabel = QLabel(self.title, self)
        self.contentLabel = QLabel(self.content, self)
        self.iconLabel = QSvgWidget(self.icon, self)
        self.closeTimer = QTimer(self)
        self.opacityEffect = QGraphicsOpacityEffect(self)
        self.opacityAni = QPropertyAnimation(self.opacityEffect, b"opacity")
        self.slideAni = QPropertyAnimation(self, b'pos')
        self.closeButton = ThreeStateButton(
            {
                ButtonState.NORMAL: ':/qfluentwidgets/images/state_tool_tip/close_normal.svg',
                ButtonState.HOVER: ':/qfluentwidgets/images/state_tool_tip/close_hover.svg',
                ButtonState.PRESSED: ':/qfluentwidgets/images/state_tool_tip/close_pressed.svg',
            },
            parent=self,
            buttonSize=(12, 12)
        )

        self.__initWidget()

    def __initWidget(self):
        """ initialize widgets """
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.closeButton.setFixedSize(QSize(11, 11))
        self.closeButton.setIconSize(QSize(11, 11))
        self.closeTimer.setInterval(2000)
        self.contentLabel.setMinimumWidth(180)

        self.iconLabel.resize(16, 16)
        self.iconLabel.move(12, 10)

        self.setGraphicsEffect(self.opacityEffect)
        self.opacityEffect.setOpacity(1)

        # connect signal to slot
        self.closeButton.clicked.connect(self.hide)
        self.closeTimer.timeout.connect(self.__fadeOut)

        self.__setQss()
        self.__initLayout()

    def __initLayout(self):
        """ initialize layout """
        self.setFixedSize(max(self.titleLabel.width(),
                          self.contentLabel.width()) + 72, 51)
        self.titleLabel.move(32, 9)
        self.contentLabel.move(12, 27)
        self.closeButton.move(self.width() - 24, 19)

    def __setQss(self):
        """ set style sheet """
        self.titleLabel.setObjectName("titleLabel")
        self.contentLabel.setObjectName("contentLabel")
        setStyleSheet(self, 'state_tool_tip')
        self.titleLabel.adjustSize()
        self.contentLabel.adjustSize()

    def __fadeOut(self):
        """ fade out """
        self.opacityAni.setDuration(300)
        self.opacityAni.setStartValue(1)
        self.opacityAni.setEndValue(0)
        self.opacityAni.finished.connect(self.deleteLater)
        self.opacityAni.start()

    def getSuitablePos(self):
        """ get suitable position in main window """
        for i in range(10):
            dy = i*(self.height() + 16)
            pos = QPoint(self.window().width() - self.width() - 24, 50+dy)
            widget = self.window().childAt(pos + QPoint(2, 2))
            if isinstance(widget, (StateToolTip, ToastToolTip)):
                pos += QPoint(0, self.height() + 16)
            else:
                break

        return pos

    def showEvent(self, e):
        pos = self.getSuitablePos()
        self.slideAni.setDuration(200)
        self.slideAni.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.slideAni.setStartValue(QPoint(self.window().width(), pos.y()))
        self.slideAni.setEndValue(pos)
        self.slideAni.start()
        super().showEvent(e)
        self.closeTimer.start()

    @classmethod
    def success(cls, title: str, content: str, parent=None):
        """ show a success toast """
        cls(title, content, cls.SUCCESS, parent).show()

    @classmethod
    def warn(cls, title: str, content: str, parent=None):
        """ show a warning toast """
        cls(title, content, cls.WARNING, parent).show()