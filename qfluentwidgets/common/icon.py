# coding:utf-8
from PyQt5.QtCore import QPoint, QRect, QRectF, Qt
from PyQt5.QtGui import QIcon, QIconEngine, QImage, QPainter, QPixmap
from PyQt5.QtSvg import QSvgRenderer

from .config import isDarkTheme


class IconEngine(QIconEngine):
    """ Icon engine """

    def __init__(self, iconPath):
        self.iconPath = iconPath
        super().__init__()

    def paint(self, painter, rect, mode, state):
        painter.setRenderHints(QPainter.Antialiasing |
                               QPainter.SmoothPixmapTransform)
        if not self.iconPath.lower().endswith('svg'):
            painter.drawImage(rect, QImage(self.iconPath))
        else:
            drawSvgIcon(self.iconPath, painter, rect)

    def pixmap(self, size, mode, state):
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)
        self.paint(QPainter(pixmap), QRect(QPoint(0, 0), size), mode, state)
        return pixmap


class Icon(QIcon):

    def __init__(self, iconPath):
        self.iconPath = iconPath
        super().__init__(IconEngine(iconPath))


class MenuIconEngine(QIconEngine):

    def __init__(self, icon):
        super().__init__()
        self.icon = icon

    def paint(self, painter, rect, mode, state):
        self.icon.paint(painter, rect, Qt.AlignHCenter, QIcon.Normal, state)


def getIconColor():
    """ get the color of icon based on theme """
    return "white" if isDarkTheme() else 'black'


def drawSvgIcon(iconPath, painter, rect):
    """ draw svg icon

    Parameters
    ----------
    iconPath: str
        the path of svg icon

    painter: QPainter
        painter

    rect: QRect | QRectF
        the rect to render icon
    """
    renderer = QSvgRenderer(iconPath)
    renderer.render(painter, QRectF(rect))


class FluentIconFactory:
    """ Fluent icon factory """

    WEB = "Web"
    CUT = "Cut"
    ADD = "Add"
    COPY = "Copy"
    LINK = "Link"
    HELP = "Help"
    FONT = "Font"
    INFO = "Info"
    ZOOM = "Zoom"
    CLOSE = "Close"
    MOVIE = "Movie"
    BRUSH = "Brush"
    MUSIC = "Music"
    VIDEO = "Video"
    EMBED = "Embed"
    PASTE = "Paste"
    CANCEL = "Cancel"
    FOLDER = "Folder"
    SEARCH = "Search"
    UPDATE = "Update"
    SETTING = "Setting"
    PALETTE = "Palette"
    FEEDBACK = "Feedback"
    MINIMIZE = "Minimize"
    LANGUAGE = "Language"
    DOWNLOAD = "Download"
    QUESTION = "Question"
    ALIGNMENT = "Alignment"
    PENCIL_INK = "PencilInk"
    FOLDER_ADD = "FolderAdd"
    ARROW_DOWN = "ChevronDown"
    TRANSPARENT = "Transparent"
    MUSIC_FOLDER = "MusicFolder"
    CHEVRON_RIGHT = "ChevronRight"
    BACKGROUND_FILL = "BackgroundColor"
    FLUORESCENT_PEN = "FluorescentPen"

    @staticmethod
    def path(iconType):
        """ get the path of icon """
        return f':/qfluentwidgets/images/icons/{iconType}_{getIconColor()}.svg'

    @classmethod
    def icon(cls, iconType):
        """ create an fluent icon """
        return QIcon(cls.path(iconType))

    @classmethod
    def render(cls, iconType, painter, rect):
        """ draw svg icon

        Parameters
        ----------
        iconType: str
            fluent icon type

        painter: QPainter
            painter

        rect: QRect | QRectF
            the rect to render icon
        """
        drawSvgIcon(cls.path(iconType), painter, rect)