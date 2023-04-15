# coding:utf-8
from enum import Enum

from PySide6.QtXml import QDomDocument
from PySide6.QtCore import QPoint, QRect, QRectF, Qt, QFile
from PySide6.QtGui import QIcon, QIconEngine, QImage, QPainter, QPixmap, QColor
from PySide6.QtSvg import QSvgRenderer

from .config import isDarkTheme, Theme


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


def drawSvgIcon(icon, painter, rect):
    """ draw svg icon

    Parameters
    ----------
    icon: str | bytes | QByteArray
        the path or code of svg icon

    painter: QPainter
        painter

    rect: QRect | QRectF
        the rect to render icon
    """
    renderer = QSvgRenderer(icon)
    renderer.render(painter, QRectF(rect))


def writeSvg(iconPath: str, indexes=None, **attributes):
    """ write svg with specified attributes

    Parameters
    ----------
    iconPath: str
        svg icon path

    indexes: List[int]
        the path to be filled

    **attributes:
        the attributes of path

    Returns
    -------
    svg: str
        svg code
    """
    if not iconPath.lower().endswith('.svg'):
        return ""

    f = QFile(iconPath)
    f.open(QFile.ReadOnly)

    dom = QDomDocument()
    dom.setContent(f.readAll())

    f.close()

    # change the color of each path
    pathNodes = dom.elementsByTagName('path')
    indexes = range(pathNodes.length()) if not indexes else indexes
    for i in indexes:
        element = pathNodes.at(i).toElement()

        for k, v in attributes.items():
            element.setAttribute(k, v)

    return dom.toString()


def drawIcon(icon, painter, rect, **attributes):
    """ draw icon

    Parameters
    ----------
    icon: str | QIcon | FluentIconBaseBase
        the icon to be drawn

    painter: QPainter
        painter

    rect: QRect | QRectF
        the rect to render icon

    **attribute:
        the attribute of svg icon
    """
    if isinstance(icon, FluentIconBase):
        icon.render(painter, rect, **attributes)
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

    def render(self, painter, rect, theme=Theme.AUTO, indexes=None, **attributes):
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

        indexes: List[int]
            the svg path to be modified

        **attributes:
            the attributes of modified path
        """
        if attributes:
            svg = writeSvg(self.path(theme), indexes, **attributes).encode()
        else:
            svg = self.path(theme)

        drawSvgIcon(svg, painter, rect)


class FluentIcon(FluentIconBase, Enum):
    """ Fluent icon """

    ADD = "Add"
    CUT = "Cut"
    PIN = "Pin"
    TAG = "Tag"
    CHAT = "Chat"
    COPY = "Copy"
    CODE = "Code"
    EDIT = "Edit"
    FONT = "Font"
    HELP = "Help"
    HIDE = "Hide"
    HOME = "Home"
    INFO = "Info"
    LINK = "Link"
    MAIL = "Mail"
    MENU = "Menu"
    MORE = "More"
    SAVE = "Save"
    SEND = "Send"
    SYNC = "Sync"
    VIEW = "View"
    ZOOM = "Zoom"
    ALBUM = "Album"
    BRUSH = "Brush"
    CLOSE = "Close"
    EMBED = "Embed"
    GLOBE = "Globe"
    HEART = "Heart"
    MEDIA = "Media"
    MOVIE = "Movie"
    MUSIC = "Music"
    PASTE = "Paste"
    PHOTO = "Photo"
    PHONE = "Phone"
    PRINT = "Print"
    SHARE = "Share"
    UNPIN = "Unpin"
    VIDEO = "Video"
    ACCEPT = "Accept"
    CAMERA = "Camera"
    CANCEL = "Cancel"
    DELETE = "Delete"
    FOLDER = "Folder"
    SCROLL = "Scroll"
    LAYOUT = "Layout"
    GITHUB = "GitHub"
    UPDATE = "Update"
    RETURN = "Return"
    RINGER = "Ringer"
    SEARCH = "Search"
    SAVE_AS = "SaveAs"
    ZOOM_IN = "ZoomIn"
    HISTORY = "History"
    SETTING = "Setting"
    PALETTE = "Palette"
    MESSAGE = "Message"
    ZOOM_OUT = "ZoomOut"
    FEEDBACK = "Feedback"
    MINIMIZE = "Minimize"
    CHECKBOX = "CheckBox"
    DOCUMENT = "Document"
    LANGUAGE = "Language"
    DOWNLOAD = "Download"
    QUESTION = "Question"
    SEND_FILL = "SendFill"
    COMPLETED = "Completed"
    CONSTRACT = "Constract"
    ALIGNMENT = "Alignment"
    BOOK_SHELF = "BookShelf"
    HIGHTLIGHT = "Highlight"
    FOLDER_ADD = "FolderAdd"
    PENCIL_INK = "PencilInk"
    ZIP_FOLDER = "ZipFolder"
    MICROPHONE = "Microphone"
    ARROW_DOWN = "ChevronDown"
    TRANSPARENT = "Transparent"
    MUSIC_FOLDER = "MusicFolder"
    CHEVRON_RIGHT = "ChevronRight"
    BACKGROUND_FILL = "BackgroundColor"

    def path(self, theme=Theme.AUTO):
        if theme == Theme.AUTO:
            c = getIconColor()
        else:
            c = "white" if theme == Theme.DARK else "black"

        return f':/qfluentwidgets/images/icons/{self.value}_{c}.svg'
