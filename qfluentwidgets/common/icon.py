# coding:utf-8
from enum import Enum

from PyQt6.QtCore import QPoint, QRect, QRectF, Qt
from PyQt6.QtGui import QIcon, QIconEngine, QImage, QPainter, QPixmap
from PyQt6.QtSvg import QSvgRenderer

from .config import isDarkTheme, Theme


class IconEngine(QIconEngine):
    """ Icon engine """

    def __init__(self, iconPath):
        self.iconPath = iconPath
        super().__init__()

    def paint(self, painter, rect, mode, state):
        painter.setRenderHints(QPainter.RenderHint.Antialiasing |
                               QPainter.RenderHint.SmoothPixmapTransform)
        if not self.iconPath.lower().endswith('svg'):
            painter.drawImage(rect, QImage(self.iconPath))
        else:
            drawSvgIcon(self.iconPath, painter, rect)

    def pixmap(self, size, mode, state):
        pixmap = QPixmap(size)
        pixmap.fill(Qt.GlobalColor.transparent)
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
        self.icon.paint(painter, rect, Qt.AlignmentFlag.AlignHCenter, QIcon.Mode.Normal, state)


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


def drawIcon(icon, painter, rect):
    """ draw icon

    Parameters
    ----------
    icon: str | QIcon | FluentIconBaseBase
        the icon to be drawn

    painter: QPainter
        painter

    rect: QRect | QRectF
        the rect to render icon
    """
    if isinstance(icon, FluentIconBase):
        icon.render(painter, rect)
    else:
        icon = QIcon(icon)
        rect = QRectF(rect).toRect()
        image = icon.pixmap(rect.width(), rect.height())
        painter.drawPixmap(rect, image)


class FluentIconBase:
    """ Fluent icon base class """

    def path(self, theme=Theme.AUTO):
        """ get the path of icon

        Parameters
        ----------
        theme: Theme
            the theme of icon
            * `Theme.Light`: black icon
            * `Theme.DARK`: white icon
            * `Theme.AUTO`: icon color depends on `config.theme`
        """
        raise NotImplementedError

    def icon(self, theme=Theme.AUTO):
        """ create an fluent icon

        Parameters
        ----------
        theme: Theme
            the theme of icon
            * `Theme.Light`: black icon
            * `Theme.DARK`: white icon
            * `Theme.AUTO`: icon color depends on `config.theme`
        """
        return QIcon(self.path(theme))

    def render(self, painter, rect, theme=Theme.AUTO):
        """ draw svg icon

        Parameters
        ----------
        painter: QPainter
            painter

        rect: QRect | QRectF
            the rect to render icon

        theme: Theme
            the theme of icon
            * `Theme.Light`: black icon
            * `Theme.DARK`: white icon
            * `Theme.AUTO`: icon color depends on `config.theme`
        """
        drawSvgIcon(self.path(theme), painter, rect)



class FluentIcon(FluentIconBase, Enum):
    """ Fluent icon """

    WEB = "Web"
    CUT = "Cut"
    ADD = "Add"
    COPY = "Copy"
    LINK = "Link"
    HELP = "Help"
    FONT = "Font"
    INFO = "Info"
    ZOOM = "Zoom"
    MENU = "Menu"
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
    RETURN = "Return"
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

    def path(self, theme=Theme.AUTO):
        if theme == Theme.AUTO:
            c = getIconColor()
        else:
            c = "white" if theme == Theme.DARK else "black"

        return f':/qfluentwidgets/images/icons/{self.value}_{c}.svg'

