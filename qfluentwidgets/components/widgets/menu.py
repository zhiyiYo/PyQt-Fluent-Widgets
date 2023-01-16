# coding:utf-8
from qframelesswindow import WindowEffect
from PyQt5.QtCore import QEasingCurve, QEvent, QPropertyAnimation, QPoint, QRect, Qt
from PyQt5.QtWidgets import QAction, QApplication, QMenu, QWidget

from ...common.icon import Icon, getIconColor
from ...common.style_sheet import setStyleSheet


class MenuIconFactory:
    """ Menu icon factory """

    ADD = "Add"
    ALBUM = "Album"
    CANCEL = "Cancel"
    CHEVRON_RIGHT = "ChevronRight"
    CLEAR = "Clear"
    CONTACT = "Contact"
    COPY = "Copy"
    CUT = "Cut"
    FULL_SCREEN = "FullScreen"
    PASTE = "Paste"
    PLAYING = "Playing"
    PLAYLIST = "Playlist"
    LYRIC = "Lyric"
    MOVIE = "Movie"
    BULLSEYE = "Bullseye"
    LOCK = "Lock"
    UNLOCK = "Unlock"
    CLOSE = "Close"
    SETTINGS = "Settings"
    RELOAD = "Reload"
    HIDE = "Hide"
    VIEW = "View"
    FOLDER_SEARCH = "FolderSearch"
    FILE_COMMENT = "FileComment"
    SPEED = "Speed"
    SPEED_UP = "SpeedUp"
    SPEED_DOWN = "SpeedDown"
    SPEED_RESET = "SpeedReset"
    INSERT = "Insert"
    FOLDER = "Folder"
    MUSIC_NOTE = "MusicNote"

    @classmethod
    def create(cls, iconType: str):
        """ create icon """
        path = f":/images/menu/{iconType}_{getIconColor()}.png"
        return Icon(path)


MIF = MenuIconFactory


class DWMMenu(QMenu):
    """ A menu with DWM shadow """

    def __init__(self, title="", parent=None):
        super().__init__(title, parent)
        self.windowEffect = WindowEffect()
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.Popup | Qt.NoDropShadowWindowHint)
        self.setAttribute(Qt.WA_StyledBackground)
        setStyleSheet(self, 'menu')

    def event(self, e: QEvent):
        if e.type() == QEvent.WinIdChange:
            self.windowEffect.addMenuShadowEffect(self.winId())
        return QMenu.event(self, e)

    def getPopupPos(self, widget: QWidget):
        """ get suitable popup position

        Parameters
        ----------
        widget: QWidget
            the widget that triggers the pop-up menu
        """
        pos = widget.mapToGlobal(QPoint())
        x = pos.x() + widget.width() + 5
        y = pos.y() + int(widget.height() / 2 - (13 + 38 * len(self.actions())) / 2)
        return QPoint(x, y)



class LineEditMenu(DWMMenu):
    """ Line edit menu """

    def __init__(self, parent):
        super().__init__("", parent)
        self.setObjectName("lineEditMenu")
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        setStyleSheet(self, 'menu')

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

    def exec_(self, pos):
        self.clear()
        self.createActions()
        self.setProperty("hasCancelAct", "false")

        if QApplication.clipboard().mimeData().hasText():
            if self.parent().text():
                self.setProperty("hasCancelAct", "true")
                if self.parent().selectedText():
                    self.addActions(self.action_list)
                else:
                    self.addActions(self.action_list[2:])
            else:
                self.addAction(self.pasteAct)
        else:
            if self.parent().text():
                self.setProperty("hasCancelAct", "true")
                if self.parent().selectedText():
                    self.addActions(
                        self.action_list[:2] + self.action_list[3:])
                else:
                    self.addActions(self.action_list[3:])
            else:
                return

        w = 130+max(self.fontMetrics().width(i.text()) for i in self.actions())
        h = len(self.actions()) * 40 + 10

        self.animation.setStartValue(QRect(pos.x(), pos.y(), 1, 1))
        self.animation.setEndValue(QRect(pos.x(), pos.y(), w, h))
        self.setStyle(QApplication.style())

        self.animation.start()
        super().exec_(pos)

