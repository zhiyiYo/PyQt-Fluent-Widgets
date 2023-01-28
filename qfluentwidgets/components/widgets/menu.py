# coding:utf-8
from qframelesswindow import WindowEffect
from PyQt6.QtCore import QEasingCurve, QEvent, QPropertyAnimation, QRect, Qt
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QApplication, QMenu, QProxyStyle, QStyle

from ...common.icon import Icon, getIconColor
from ...common.style_sheet import setStyleSheet


class MenuIconFactory:
    """ Menu icon factory """

    CUT = "Cut"
    COPY = "Copy"
    PASTE = "Paste"
    CANCEL = "Cancel"
    CHEVRON_RIGHT = "ChevronRight"

    @classmethod
    def create(cls, iconType: str):
        """ create icon """
        path = f":/qfluentwidgets/images/menu/{iconType}_{getIconColor()}.svg"
        return QIcon(path)


MIF = MenuIconFactory


class CustomMenuStyle(QProxyStyle):
    """ Custom menu style """

    def __init__(self, iconSize=14):
        """
        Parameters
        ----------
        iconSizeL int
            the size of icon
        """
        super().__init__()
        self.iconSize = iconSize

    def pixelMetric(self, metric, option, widget):
        if metric == QStyle.PixelMetric.PM_SmallIconSize:
            return self.iconSize

        return super().pixelMetric(metric, option, widget)


class DWMMenu(QMenu):
    """ A menu with DWM shadow """

    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.windowEffect = WindowEffect(self)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup | Qt.WindowType.NoDropShadowWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyle(CustomMenuStyle())
        setStyleSheet(self, 'menu')

    def event(self, e: QEvent):
        if e.type() == QEvent.Type.WinIdChange:
            self.windowEffect.addMenuShadowEffect(self.winId())
        return QMenu.event(self, e)



class LineEditMenu(DWMMenu):
    """ Line edit menu """

    def __init__(self, parent):
        super().__init__("", parent)
        self.setObjectName("lineEditMenu")
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.setProperty("selectAll", bool(self.parent().text()))

    def createActions(self):
        self.cutAct = QAction(
            MIF.create(MIF.CUT),
            self.tr("Cut"),
            self,
            shortcut="Ctrl+X",
            triggered=self.parent().cut,
        )
        self.copyAct = QAction(
            MIF.create(MIF.COPY),
            self.tr("Copy"),
            self,
            shortcut="Ctrl+C",
            triggered=self.parent().copy,
        )
        self.pasteAct = QAction(
            MIF.create(MIF.PASTE),
            self.tr("Paste"),
            self,
            shortcut="Ctrl+V",
            triggered=self.parent().paste,
        )
        self.cancelAct = QAction(
            MIF.create(MIF.CANCEL),
            self.tr("Cancel"),
            self,
            shortcut="Ctrl+Z",
            triggered=self.parent().undo,
        )
        self.selectAllAct = QAction(
            self.tr("Select all"),
            self,
            shortcut="Ctrl+A",
            triggered=self.parent().selectAll
        )
        self.action_list = [self.cutAct, self.copyAct,
                            self.pasteAct, self.cancelAct, self.selectAllAct]

    def exec(self, pos):
        self.clear()
        self.createActions()

        if QApplication.clipboard().mimeData().hasText():
            if self.parent().text():
                if self.parent().selectedText():
                    self.addActions(self.action_list)
                else:
                    self.addActions(self.action_list[2:])
            else:
                self.addAction(self.pasteAct)
        else:
            if self.parent().text():
                if self.parent().selectedText():
                    self.addActions(
                        self.action_list[:2] + self.action_list[3:])
                else:
                    self.addActions(self.action_list[3:])
            else:
                return

        w = 109+max(self.fontMetrics().boundingRect(i.text()).width() for i in self.actions())
        h = len(self.actions()) * 32 + 8

        self.animation.setStartValue(QRect(pos.x(), pos.y(), 1, 1))
        self.animation.setEndValue(QRect(pos.x(), pos.y(), w, h))
        self.setStyle(CustomMenuStyle())

        self.animation.start()
        super().exec(pos)

