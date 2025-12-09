# coding:utf-8
from enum import Enum
from typing import Union
import json

from PyQt5.QtXml import QDomDocument
from PyQt5.QtCore import QRectF, Qt, QFile, QObject, QRect
from PyQt5.QtGui import QIcon, QIconEngine, QColor, QPixmap, QImage, QPainter, QFontDatabase, QFont, QPainterPath
from PyQt5.QtWidgets import QAction, qApp, QApplication
from PyQt5.QtSvg import QSvgRenderer

from .config import isDarkTheme, Theme
from .overload import singledispatchmethod


class FluentIconEngine(QIconEngine):
    """ Fluent icon engine """

    def __init__(self, icon, reverse=False):
        """
        Parameters
        ----------
        icon: QICon | Icon | FluentIconBase
            the icon to be drawn

        reverse: bool
            whether to reverse the theme of icon
        """
        super().__init__()
        self.icon = icon
        self.isThemeReversed = reverse

    def paint(self, painter, rect, mode, state):
        painter.save()

        if mode == QIcon.Disabled:
            painter.setOpacity(0.5)
        elif mode == QIcon.Selected:
            painter.setOpacity(0.7)

        # change icon color according to the theme
        icon = self.icon

        if not self.isThemeReversed:
            theme = Theme.AUTO
        else:
            theme = Theme.LIGHT if isDarkTheme() else Theme.DARK

        if isinstance(self.icon, Icon):
            icon = self.icon.fluentIcon.icon(theme)
        elif isinstance(self.icon, FluentIconBase):
            icon = self.icon.icon(theme)

        if rect.x() == 19:
            rect = rect.adjusted(-1, 0, 0, 0)

        icon.paint(painter, rect, Qt.AlignCenter, QIcon.Normal, state)
        painter.restore()

    def clone(self) -> QIconEngine:
        return FluentIconEngine(self.icon, self.isThemeReversed)

    def pixmap(self, size, mode, state):
        image = QImage(size, QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        pixmap = QPixmap.fromImage(image, Qt.NoFormatConversion)

        painter = QPainter(pixmap)
        rect = QRect(0, 0, size.width(), size.height())
        self.paint(painter, rect, mode, state)
        return pixmap


class SvgIconEngine(QIconEngine):
    """ Svg icon engine """

    def __init__(self, svg: str):
        super().__init__()
        self.svg = svg

    def paint(self, painter, rect, mode, state):
        drawSvgIcon(self.svg.encode(), painter, rect)

    def clone(self) -> QIconEngine:
        return SvgIconEngine(self.svg)

    def pixmap(self, size, mode, state):
        image = QImage(size, QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        pixmap = QPixmap.fromImage(image, Qt.NoFormatConversion)

        painter = QPainter(pixmap)
        rect = QRect(0, 0, size.width(), size.height())
        self.paint(painter, rect, mode, state)
        return pixmap


class FontIconEngine(QIconEngine):
    """ Font icon engine """

    def __init__(self, fontFamily: str, char: str, color, isBold):
        super().__init__()
        self.color = color
        self.char = char
        self.fontFamily = fontFamily
        self.isBold = isBold

    def paint(self, painter, rect, mode, state):
        font = QFont(self.fontFamily)
        font.setBold(self.isBold)
        font.setPixelSize(round(rect.height()))
        painter.setFont(font)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.color)
        painter.setRenderHints(
            QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)

        path = QPainterPath()
        path.addText(rect.x(), rect.y() + rect.height(), font, self.char)
        painter.drawPath(path)


    def clone(self) -> QIconEngine:
        return FontIconEngine(self.fontFamily, self.char, self.color, self.isBold)

    def pixmap(self, size, mode, state):
        image = QImage(size, QImage.Format_ARGB32)
        image.fill(Qt.transparent)
        pixmap = QPixmap.fromImage(image, Qt.NoFormatConversion)

        painter = QPainter(pixmap)
        rect = QRect(0, 0, size.width(), size.height())
        self.paint(painter, rect, mode, state)
        return pixmap


def getIconColor(theme=Theme.AUTO, reverse=False):
    """ get the color of icon based on theme """
    if not reverse:
        lc, dc = "black", "white"
    else:
        lc, dc = "white", "black"

    if theme == Theme.AUTO:
        color = dc if isDarkTheme() else lc
    else:
        color = dc if theme == Theme.DARK else lc

    return color


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


def drawIcon(icon, painter, rect, state=QIcon.Off, **attributes):
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
    elif isinstance(icon, Icon):
        icon.fluentIcon.render(painter, rect, **attributes)
    else:
        icon = QIcon(icon)
        icon.paint(painter, QRectF(rect).toRect(), Qt.AlignCenter, state=state)


class FluentIconBase:
    """ Fluent icon base class """

    def path(self, theme=Theme.AUTO) -> str:
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

    def icon(self, theme=Theme.AUTO, color: QColor = None) -> QIcon:
        """ create a fluent icon

        Parameters
        ----------
        theme: Theme
            the theme of icon
            * `Theme.Light`: black icon
            * `Theme.DARK`: white icon
            * `Theme.AUTO`: icon color depends on `qconfig.theme`

        color: QColor | Qt.GlobalColor | str
            icon color, only applicable to svg icon
        """
        path = self.path(theme)

        if not (path.endswith('.svg') and color):
            return QIcon(self.path(theme))

        color = QColor(color).name()
        return QIcon(SvgIconEngine(writeSvg(path, fill=color)))

    def colored(self, lightColor: QColor, darkColor: QColor) -> "ColoredFluentIcon":
        """ create a colored fluent icon

        Parameters
        ----------
        lightColor: str | QColor | Qt.GlobalColor
            icon color in light mode

        darkColor: str | QColor | Qt.GlobalColor
            icon color in dark mode
        """
        return ColoredFluentIcon(self, lightColor, darkColor)

    def qicon(self, reverse=False) -> QIcon:
        """ convert to QIcon, the theme of icon will be updated synchronously with app

        Parameters
        ----------
        reverse: bool
            whether to reverse the theme of icon
        """
        return QIcon(FluentIconEngine(self, reverse))

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
        icon = self.path(theme)

        if icon.endswith('.svg'):
            if attributes:
                icon = writeSvg(icon, indexes, **attributes).encode()

            drawSvgIcon(icon, painter, rect)
        else:
            icon = QIcon(icon)
            rect = QRectF(rect).toRect()
            painter.drawPixmap(rect, icon.pixmap(QRectF(rect).toRect().size()))


class FluentFontIconBase(FluentIconBase):
    """ Fluent font icon base class """

    _isFontLoaded = False
    fontId = None
    fontFamily = None
    _iconNames = {}

    def __init__(self, char: str):
        super().__init__()
        self.char = char
        self.lightColor = QColor(0, 0, 0)
        self.darkColor = QColor(255, 255, 255)
        self.isBold = False
        self.loadFont()

    @classmethod
    def fromName(cls, name: str):
        icon = cls("")
        icon.char = cls._iconNames.get(name, "")
        return icon

    def bold(self):
        self.isBold = True
        return self

    def icon(self, theme=Theme.AUTO, color: QColor = None) -> QIcon:
        if not color:
            color = self._getIconColor(theme)

        return QIcon(FontIconEngine(self.fontFamily, self.char, color, self.isBold))

    def colored(self, lightColor, darkColor):
        self.lightColor = QColor(lightColor)
        self.darkColor = QColor(darkColor)
        return self

    def render(self, painter: QPainter, rect, theme=Theme.AUTO, indexes=None, **attributes):
        color = self._getIconColor(theme)

        if "fill" in attributes:
            color = QColor(attributes["fill"])

        font = QFont(self.fontFamily)
        font.setBold(self.isBold)
        font.setPixelSize(round(rect.height()))
        painter.setFont(font)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(color)
        painter.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing)

        path = QPainterPath()
        path.addText(rect.x(), rect.y() + rect.height(), font, self.char)
        painter.drawPath(path)

    def iconNameMapPath(self) -> str:
        return None

    def loadFont(self):
        """ Load icon font """
        cls = self.__class__
        if cls._isFontLoaded or not QApplication.instance():
            return

        file = QFile(self.path())
        if not file.open(QFile.ReadOnly):
            raise FileNotFoundError(f"Cannot open font file: {self.path()}")

        data = file.readAll()
        file.close()

        cls.fontId = QFontDatabase.addApplicationFontFromData(data)
        cls.fontFamily = QFontDatabase.applicationFontFamilies(cls.fontId)[0]

        if self.iconNameMapPath():
            self.loadIconNames()

    def loadIconNames(self):
        """ Load icon name map """
        cls = self.__class__
        cls._iconNames.clear()

        file = QFile(self.iconNameMapPath())
        if not file.open(QFile.ReadOnly):
            raise FileNotFoundError(f"Cannot open font file: {self.iconNameMapPath()}")

        cls._iconNames = json.loads(str(file.readAll(), encoding='utf-8'))
        file.close()

    def _getIconColor(self, theme):
        if theme == Theme.AUTO:
            color = self.darkColor if isDarkTheme() else self.lightColor
        else:
            color = self.darkColor if theme == Theme.DARK else self.lightColor

        return color


class ColoredFluentIcon(FluentIconBase):
    """ Colored fluent icon """

    def __init__(self, icon: FluentIconBase, lightColor, darkColor):
        """
        Parameters
        ----------
        icon: FluentIconBase
            the icon to be colored

        lightColor: str | QColor | Qt.GlobalColor
            icon color in light mode

        darkColor: str | QColor | Qt.GlobalColor
            icon color in dark mode
        """
        super().__init__()
        self.fluentIcon = icon
        self.lightColor = QColor(lightColor)
        self.darkColor = QColor(darkColor)

    def path(self, theme=Theme.AUTO) -> str:
        return self.fluentIcon.path(theme)

    def render(self, painter, rect, theme=Theme.AUTO, indexes=None, **attributes):
        icon = self.path(theme)

        if not icon.endswith('.svg'):
            return self.fluentIcon.render(painter, rect, theme, indexes, attributes)

        if theme == Theme.AUTO:
            color = self.darkColor if isDarkTheme() else self.lightColor
        else:
            color = self.darkColor if theme == Theme.DARK else self.lightColor

        attributes.update(fill=color.name())
        icon = writeSvg(icon, indexes, **attributes).encode()
        drawSvgIcon(icon, painter, rect)



class FluentIcon(FluentIconBase, Enum):
    """ Fluent icon """

    UP = "Up"
    ADD = "Add"
    BUS = "Bus"
    CAR = "Car"
    CUT = "Cut"
    IOT = "IOT"
    PIN = "Pin"
    TAG = "Tag"
    VPN = "VPN"
    CAFE = "Cafe"
    CHAT = "Chat"
    COPY = "Copy"
    CODE = "Code"
    DOWN = "Down"
    EDIT = "Edit"
    FLAG = "Flag"
    FONT = "Font"
    GAME = "Game"
    HELP = "Help"
    HIDE = "Hide"
    HOME = "Home"
    INFO = "Info"
    LEAF = "Leaf"
    LINK = "Link"
    MAIL = "Mail"
    MENU = "Menu"
    MUTE = "Mute"
    MORE = "More"
    MOVE = "Move"
    PLAY = "Play"
    SAVE = "Save"
    SEND = "Send"
    SYNC = "Sync"
    UNIT = "Unit"
    VIEW = "View"
    WIFI = "Wifi"
    ZOOM = "Zoom"
    ALBUM = "Album"
    BRUSH = "Brush"
    BROOM = "Broom"
    CLOSE = "Close"
    CLOUD = "Cloud"
    EMBED = "Embed"
    GLOBE = "Globe"
    HEART = "Heart"
    LABEL = "Label"
    MEDIA = "Media"
    MOVIE = "Movie"
    MUSIC = "Music"
    ROBOT = "Robot"
    PAUSE = "Pause"
    PASTE = "Paste"
    PHOTO = "Photo"
    PHONE = "Phone"
    PRINT = "Print"
    SHARE = "Share"
    TILES = "Tiles"
    UNPIN = "Unpin"
    VIDEO = "Video"
    TRAIN = "Train"
    ADD_TO  ="AddTo"
    ACCEPT = "Accept"
    CAMERA = "Camera"
    CANCEL = "Cancel"
    DELETE = "Delete"
    FOLDER = "Folder"
    FILTER = "Filter"
    MARKET = "Market"
    SCROLL = "Scroll"
    LAYOUT = "Layout"
    GITHUB = "GitHub"
    UPDATE = "Update"
    REMOVE = "Remove"
    RETURN = "Return"
    PEOPLE = "People"
    QRCODE = "QRCode"
    RINGER = "Ringer"
    ROTATE = "Rotate"
    SEARCH = "Search"
    VOLUME = "Volume"
    FRIGID  = "Frigid"
    SAVE_AS = "SaveAs"
    ZOOM_IN = "ZoomIn"
    CONNECT  ="Connect"
    HISTORY = "History"
    SETTING = "Setting"
    PALETTE = "Palette"
    MESSAGE = "Message"
    FIT_PAGE = "FitPage"
    ZOOM_OUT = "ZoomOut"
    AIRPLANE = "Airplane"
    ASTERISK = "Asterisk"
    CALORIES = "Calories"
    CALENDAR = "Calendar"
    FEEDBACK = "Feedback"
    LIBRARY = "BookShelf"
    MINIMIZE = "Minimize"
    CHECKBOX = "CheckBox"
    DOCUMENT = "Document"
    LANGUAGE = "Language"
    DOWNLOAD = "Download"
    QUESTION = "Question"
    SPEAKERS = "Speakers"
    DATE_TIME = "DateTime"
    FONT_SIZE = "FontSize"
    HOME_FILL = "HomeFill"
    PAGE_LEFT = "PageLeft"
    SAVE_COPY = "SaveCopy"
    SEND_FILL = "SendFill"
    SKIP_BACK = "SkipBack"
    SPEED_OFF = "SpeedOff"
    ALIGNMENT = "Alignment"
    BLUETOOTH = "Bluetooth"
    COMPLETED = "Completed"
    CONSTRACT = "Constract"
    HEADPHONE = "Headphone"
    MEGAPHONE = "Megaphone"
    PROJECTOR = "Projector"
    EDUCATION = "Education"
    LEFT_ARROW = "LeftArrow"
    ERASE_TOOL = "EraseTool"
    PAGE_RIGHT = "PageRight"
    PLAY_SOLID = "PlaySolid"
    BOOK_SHELF = "BookShelf"
    HIGHTLIGHT = "Highlight"
    FOLDER_ADD = "FolderAdd"
    PAUSE_BOLD = "PauseBold"
    PENCIL_INK = "PencilInk"
    PIE_SINGLE = "PieSingle"
    QUICK_NOTE = "QuickNote"
    SPEED_HIGH = "SpeedHigh"
    STOP_WATCH = "StopWatch"
    ZIP_FOLDER = "ZipFolder"
    BASKETBALL = "Basketball"
    BRIGHTNESS = "Brightness"
    DICTIONARY = "Dictionary"
    MICROPHONE = "Microphone"
    ARROW_DOWN = "ChevronDown"
    FULL_SCREEN = "FullScreen"
    MIX_VOLUMES = "MixVolumes"
    REMOVE_FROM = "RemoveFrom"
    RIGHT_ARROW = "RightArrow"
    QUIET_HOURS  ="QuietHours"
    FINGERPRINT = "Fingerprint"
    APPLICATION = "Application"
    CERTIFICATE = "Certificate"
    TRANSPARENT = "Transparent"
    IMAGE_EXPORT = "ImageExport"
    SPEED_MEDIUM = "SpeedMedium"
    LIBRARY_FILL = "LibraryFill"
    MUSIC_FOLDER = "MusicFolder"
    POWER_BUTTON = "PowerButton"
    SKIP_FORWARD = "SkipForward"
    CARE_UP_SOLID = "CareUpSolid"
    ACCEPT_MEDIUM = "AcceptMedium"
    CANCEL_MEDIUM = "CancelMedium"
    CHEVRON_RIGHT = "ChevronRight"
    CLIPPING_TOOL = "ClippingTool"
    SEARCH_MIRROR = "SearchMirror"
    SHOPPING_CART = "ShoppingCart"
    FONT_INCREASE = "FontIncrease"
    BACK_TO_WINDOW = "BackToWindow"
    COMMAND_PROMPT = "CommandPrompt"
    CLOUD_DOWNLOAD = "CloudDownload"
    DICTIONARY_ADD = "DictionaryAdd"
    CARE_DOWN_SOLID = "CareDownSolid"
    CARE_LEFT_SOLID = "CareLeftSolid"
    CLEAR_SELECTION = "ClearSelection"
    DEVELOPER_TOOLS = "DeveloperTools"
    BACKGROUND_FILL = "BackgroundColor"
    CARE_RIGHT_SOLID = "CareRightSolid"
    CHEVRON_DOWN_MED = "ChevronDownMed"
    CHEVRON_RIGHT_MED = "ChevronRightMed"
    EMOJI_TAB_SYMBOLS = "EmojiTabSymbols"
    EXPRESSIVE_INPUT_ENTRY = "ExpressiveInputEntry"

    ACCIDENT = "Accident"
    ACCIDENT_SOLID = "AccidentSolid"
    ACCOUNTS = "Accounts"
    ACTION_CENTER = "ActionCenter"
    ACTION_CENTER_ASTERISK = "ActionCenterAsterisk"
    ACTION_CENTER_MIRRORED = "ActionCenterMirrored"
    ACTION_CENTER_NOTIFICATION = "ActionCenterNotification"
    ACTION_CENTER_NOTIFICATION_MIRRORED = "ActionCenterNotificationMirrored"
    ACTION_CENTER_QUIET = "ActionCenterQuiet"
    ACTION_CENTER_QUIET_NOTIFICATION = "ActionCenterQuietNotification"
    ADD_BOLD = "AddBold"
    ADD_FRIEND = "AddFriend"
    ADD_NEW_LINE = "AddNewLine"
    ADD_NEW_LINE_FILL = "AddNewLineFill"
    ADD_REMOTE_DEVICE = "AddRemoteDevice"
    ADD_SURFACE_HUB = "AddSurfaceHub"
    ADJUST_HOLOGRAM = "AdjustHologram"
    ADMIN = "Admin"
    AIRPLANE_SOLID = "AirplaneSolid"
    ALERT_URGENT = "AlertUrgent"
    ALIGN_CENTER = "AlignCenter"
    ALIGN_LEFT = "AlignLeft"
    ALIGN_RIGHT = "AlignRight"
    ALL_APPS = "AllApps"
    ALL_APPS_MIRRORED = "AllAppsMirrored"
    ANNOTATION = "Annotation"
    APPLICATION_GUARD = "ApplicationGuard"
    APPS = "Apps"
    APP_ICON_DEFAULT = "AppIconDefault"
    APP_ICON_DEFAULT_ADD = "AppIconDefaultAdd"
    AREA_CHART = "AreaChart"
    ARROW_DOWN8 = "ArrowDown8"
    ARROW_LEFT8 = "ArrowLeft8"
    ARROW_RIGHT8 = "ArrowRight8"
    ARROW_UP8 = "ArrowUp8"
    ASPECT_RATIO = "AspectRatio"
    ASTERISK_BADGE12 = "AsteriskBadge12"
    ATTACH = "Attach"
    ATTACH_CAMERA = "AttachCamera"
    AUDIO = "Audio"
    BACK = "Back"
    BACKGROUND_TOGGLE = "BackgroundToggle"
    BACK_MIRRORED = "BackMirrored"
    BACK_SOLID_BOLD = "BackSolidBold"
    BACK_SPACE_QWERTY = "BackSpaceQWERTY"
    BACK_SPACE_QWERTY_LG = "BackSpaceQWERTYLg"
    BACK_SPACE_QWERTY_MD = "BackSpaceQWERTYMd"
    BACK_SPACE_QWERTY_SM = "BackSpaceQWERTYSm"
    BADGE = "Badge"
    BAND_BATTERY0 = "BandBattery0"
    BAND_BATTERY1 = "BandBattery1"
    BAND_BATTERY2 = "BandBattery2"
    BAND_BATTERY3 = "BandBattery3"
    BAND_BATTERY4 = "BandBattery4"
    BAND_BATTERY5 = "BandBattery5"
    BAND_BATTERY6 = "BandBattery6"
    BANK = "Bank"
    BARCODE_SCANNER = "BarcodeScanner"
    BATTERY0 = "Battery0"
    BATTERY1 = "Battery1"
    BATTERY10 = "Battery10"
    BATTERY2 = "Battery2"
    BATTERY3 = "Battery3"
    BATTERY4 = "Battery4"
    BATTERY5 = "Battery5"
    BATTERY6 = "Battery6"
    BATTERY7 = "Battery7"
    BATTERY8 = "Battery8"
    BATTERY9 = "Battery9"
    BATTERY_CHARGING0 = "BatteryCharging0"
    BATTERY_CHARGING1 = "BatteryCharging1"
    BATTERY_CHARGING10 = "BatteryCharging10"
    BATTERY_CHARGING2 = "BatteryCharging2"
    BATTERY_CHARGING3 = "BatteryCharging3"
    BATTERY_CHARGING4 = "BatteryCharging4"
    BATTERY_CHARGING5 = "BatteryCharging5"
    BATTERY_CHARGING6 = "BatteryCharging6"
    BATTERY_CHARGING7 = "BatteryCharging7"
    BATTERY_CHARGING8 = "BatteryCharging8"
    BATTERY_CHARGING9 = "BatteryCharging9"
    BATTERY_SAVER = "BatterySaver"
    BATTERY_SAVER0 = "BatterySaver0"
    BATTERY_SAVER1 = "BatterySaver1"
    BATTERY_SAVER10 = "BatterySaver10"
    BATTERY_SAVER2 = "BatterySaver2"
    BATTERY_SAVER3 = "BatterySaver3"
    BATTERY_SAVER4 = "BatterySaver4"
    BATTERY_SAVER5 = "BatterySaver5"
    BATTERY_SAVER6 = "BatterySaver6"
    BATTERY_SAVER7 = "BatterySaver7"
    BATTERY_SAVER8 = "BatterySaver8"
    BATTERY_SAVER9 = "BatterySaver9"
    BATTERY_UNKNOWN = "BatteryUnknown"
    BEAKER = "Beaker"
    BETA = "Beta"
    BIDI_LTR = "BidiLtr"
    BIDI_RTL = "BidiRtl"
    BLOCKED = "Blocked"
    BLOCKED2 = "Blocked2"
    BLOCK_CONTACT = "BlockContact"
    BLUE_LIGHT = "BlueLight"
    BODY_CAM = "BodyCam"
    BOLD = "Bold"
    BOOKMARKS = "Bookmarks"
    BOOKMARKS_MIRRORED = "BookmarksMirrored"
    BROWSE_PHOTOS = "BrowsePhotos"
    BRUSH_SIZE = "BrushSize"
    BUG = "Bug"
    BUILDING_ENERGY = "BuildingEnergy"
    BULLETED_LIST = "BulletedList"
    BULLETED_LIST2 = "BulletedList2"
    BULLETED_LIST2_MIRRORED = "BulletedList2Mirrored"
    BULLETED_LIST_MIRRORED = "BulletedListMirrored"
    BULLSEYE = "Bullseye"
    BUMPER_LEFT = "BumperLeft"
    BUMPER_RIGHT = "BumperRight"
    BUS_SOLID = "BusSolid"
    BUTTON_A = "ButtonA"
    BUTTON_B = "ButtonB"
    BUTTON_MENU = "ButtonMenu"
    BUTTON_VIEW2 = "ButtonView2"
    BUTTON_X = "ButtonX"
    BUTTON_Y = "ButtonY"
    CALCULATOR = "Calculator"
    CALCULATOR_ADDITION = "CalculatorAddition"
    CALCULATOR_BACKSPACE = "CalculatorBackspace"
    CALCULATOR_DIVIDE = "CalculatorDivide"
    CALCULATOR_EQUAL_TO = "CalculatorEqualTo"
    CALCULATOR_MULTIPLY = "CalculatorMultiply"
    CALCULATOR_NEGATE = "CalculatorNegate"
    CALCULATOR_PERCENTAGE = "CalculatorPercentage"
    CALCULATOR_SQUAREROOT = "CalculatorSquareroot"
    CALCULATOR_SUBTRACT = "CalculatorSubtract"
    CALENDAR_DAY = "CalendarDay"
    CALENDAR_MIRRORED = "CalendarMirrored"
    CALENDAR_REPLY = "CalendarReply"
    CALENDAR_SOLID = "CalendarSolid"
    CALENDAR_WEEK = "CalendarWeek"
    CALLIGRAPHY_FILL = "CalligraphyFill"
    CALLIGRAPHY_PEN = "CalligraphyPen"
    CALL_CONTROL = "CallControl"
    CALL_FORWARDING = "CallForwarding"
    CALL_FORWARDING_MIRRORED = "CallForwardingMirrored"
    CALL_FORWARD_INTERNATIONAL = "CallForwardInternational"
    CALL_FORWARD_INTERNATIONAL_MIRRORED = "CallForwardInternationalMirrored"
    CALL_FORWARD_ROAMING = "CallForwardRoaming"
    CALL_FORWARD_ROAMING_MIRRORED = "CallForwardRoamingMirrored"
    CAPTION = "Caption"
    CARET_BOTTOM_RIGHT_SOLID_CENTER8 = "CaretBottomRightSolidCenter8"
    CARET_DOWN8 = "CaretDown8"
    CARET_DOWN_SOLID8 = "CaretDownSolid8"
    CARET_LEFT8 = "CaretLeft8"
    CARET_LEFT_SOLID8 = "CaretLeftSolid8"
    CARET_RIGHT8 = "CaretRight8"
    CARET_RIGHT_SOLID8 = "CaretRightSolid8"
    CARET_SOLID_DOWN = "CaretSolidDown"
    CARET_SOLID_LEFT = "CaretSolidLeft"
    CARET_SOLID_RIGHT = "CaretSolidRight"
    CARET_SOLID_UP = "CaretSolidUp"
    CARET_UP8 = "CaretUp8"
    CARET_UP_SOLID8 = "CaretUpSolid8"
    CASH_DRAWER = "CashDrawer"
    CC = "CC"
    CELL_PHONE = "CellPhone"
    CHARACTERS = "Characters"
    CHARACTER_APPEARANCE = "CharacterAppearance"
    CHAT_BUBBLES = "ChatBubbles"
    CHECKBOX14 = "Checkbox14"
    CHECKBOX_COMPOSITE = "CheckboxComposite"
    CHECKBOX_COMPOSITE14 = "CheckboxComposite14"
    CHECKBOX_COMPOSITE_REVERSED = "CheckboxCompositeReversed"
    CHECKBOX_FILL = "CheckboxFill"
    CHECKBOX_INDETERMINATE = "CheckboxIndeterminate"
    CHECKBOX_INDETERMINATE_COMBO = "CheckboxIndeterminateCombo"
    CHECKBOX_INDETERMINATE_COMBO14 = "CheckboxIndeterminateCombo14"
    CHECKLIST_MIRRORED = "ChecklistMirrored"
    CHECK_LIST = "CheckList"
    CHECK_MARK = "CheckMark"
    CHEVRON_DOWN_SMALL = "ChevronDownSmall"
    CHEVRON_LEFT = "ChevronLeft"
    CHEVRON_LEFT20 = "ChevronLeft20"
    CHEVRON_LEFT32 = "ChevronLeft32"
    CHEVRON_LEFT_MED = "ChevronLeftMed"
    CHEVRON_LEFT_SMALL = "ChevronLeftSmall"
    CHEVRON_RIGHT20 = "ChevronRight20"
    CHEVRON_RIGHT32 = "ChevronRight32"
    CHEVRON_RIGHT_SMALL = "ChevronRightSmall"
    CHEVRON_UP = "ChevronUp"
    CHEVRON_UP_MED = "ChevronUpMed"
    CHEVRON_UP_SMALL = "ChevronUpSmall"
    CHINESE_BO_PO_MO_FO = "ChineseBoPoMoFo"
    CHINESE_CHANGJIE = "ChineseChangjie"
    CHINESE_PINYIN = "ChinesePinyin"
    CHINESE_PUNCTUATION = "ChinesePunctuation"
    CHINESE_QUICK = "ChineseQuick"
    CHIP_CARD_CREDIT_CARD_READER = "ChipCardCreditCardReader"
    CHROME_ANNOTATE = "ChromeAnnotate"
    CHROME_ANNOTATE_CONTRAST = "ChromeAnnotateContrast"
    CHROME_BACK = "ChromeBack"
    CHROME_BACK_CONTRAST = "ChromeBackContrast"
    CHROME_BACK_CONTRAST_MIRRORED = "ChromeBackContrastMirrored"
    CHROME_BACK_MIRRORED = "ChromeBackMirrored"
    CHROME_BACK_TO_WINDOW = "ChromeBackToWindow"
    CHROME_BACK_TO_WINDOW_CONTRAST = "ChromeBackToWindowContrast"
    CHROME_CLOSE = "ChromeClose"
    CHROME_CLOSE_CONTRAST = "ChromeCloseContrast"
    CHROME_FULL_SCREEN = "ChromeFullScreen"
    CHROME_FULL_SCREEN_CONTRAST = "ChromeFullScreenContrast"
    CHROME_MAXIMIZE = "ChromeMaximize"
    CHROME_MAXIMIZE_CONTRAST = "ChromeMaximizeContrast"
    CHROME_MINIMIZE = "ChromeMinimize"
    CHROME_MINIMIZE_CONTRAST = "ChromeMinimizeContrast"
    CHROME_RESTORE = "ChromeRestore"
    CHROME_RESTORE_CONTRAST = "ChromeRestoreContrast"
    CHROME_SWITCH = "ChromeSwitch"
    CHROME_SWITCH_CONTAST = "ChromeSwitchContast"
    CHT_LANGUAGE_BAR = "CHTLanguageBar"
    CIRCLE_FILL = "CircleFill"
    CIRCLE_FILL_BADGE12 = "CircleFillBadge12"
    CIRCLE_PAUSE = "CirclePause"
    CIRCLE_RING = "CircleRing"
    CIRCLE_RING_BADGE12 = "CircleRingBadge12"
    CIRCLE_SHAPE_SOLID = "CircleShapeSolid"
    CITY_NEXT = "CityNext"
    CITY_NEXT2 = "CityNext2"
    CLEAR = "Clear"
    CLEAR_ALL_INK = "ClearAllInk"
    CLEAR_ALL_INK_MIRRORED = "ClearAllInkMirrored"
    CLEAR_SELECTION_MIRRORED = "ClearSelectionMirrored"
    CLICK = "Click"
    CLICKED_OUT_LOUD_SOLID_BOLD = "ClickedOutLoudSolidBold"
    CLICKTO_DO = "ClicktoDo"
    CLICKTO_DO_OFF = "ClicktoDoOff"
    CLICK_SOLID = "ClickSolid"
    CLIPBOARD_LIST = "ClipboardList"
    CLIPBOARD_LIST_MIRRORED = "ClipboardListMirrored"
    CLOSED_CAPTIONS_INTERNATIONAL = "ClosedCaptionsInternational"
    CLOSE_PANE = "ClosePane"
    CLOSE_PANE_MIRRORED = "ClosePaneMirrored"
    CLOUD_NOT_SYNCED = "CloudNotSynced"
    CLOUD_PRINTER = "CloudPrinter"
    CLOUD_SEARCH = "CloudSearch"
    COLLAPSE_CONTENT = "CollapseContent"
    COLLAPSE_CONTENT_SINGLE = "CollapseContentSingle"
    COLLATE_LANDSCAPE = "CollateLandscape"
    COLLATE_LANDSCAPE_SEPARATED = "CollateLandscapeSeparated"
    COLLATE_PORTRAIT = "CollatePortrait"
    COLLATE_PORTRAIT_SEPARATED = "CollatePortraitSeparated"
    COLOR = "Color"
    COLOR_OFF = "ColorOff"
    COLOR_SOLID = "ColorSolid"
    COMMA_KEY = "CommaKey"
    COMMENT = "Comment"
    COMMUNICATIONS = "Communications"
    COMPANION_APP = "CompanionApp"
    COMPANION_DEVICE_FRAMEWORK = "CompanionDeviceFramework"
    COMPLETED_SOLID = "CompletedSolid"
    COMPONENT = "Component"
    COMPOSE_MODE = "ComposeMode"
    CONNECTED = "Connected"
    CONNECT_APP = "ConnectApp"
    CONSTRUCTION = "Construction"
    CONSTRUCTION_CONE = "ConstructionCone"
    CONSTRUCTION_SOLID = "ConstructionSolid"
    CONTACT = "Contact"
    CONTACT2 = "Contact2"
    CONTACT_INFO = "ContactInfo"
    CONTACT_INFO_MIRRORED = "ContactInfoMirrored"
    CONTACT_PRESENCE = "ContactPresence"
    CONTACT_SOLID = "ContactSolid"
    CONTRAST = "Contrast"
    COPY_TO = "CopyTo"
    COURTHOUSE = "Courthouse"
    CPU = "CPU"
    CRM_SCHEDULE_REPORTS = "CRMScheduleReports"
    CROP = "Crop"
    CTRL_SPATIAL_LEFT = "CtrlSpatialLeft"
    CTRL_SPATIAL_RIGHT = "CtrlSpatialRight"
    DASH_KEY = "DashKey"
    DATA_SENSE = "DataSense"
    DATA_SENSE_BAR = "DataSenseBar"
    DATE_TIME_MIRRORED = "DateTimeMirrored"
    DECLINE_CALL = "DeclineCall"
    DEFAULT_APN = "DefaultAPN"
    DEFENDER_APP = "DefenderApp"
    DEFENDER_BADGE12 = "DefenderBadge12"
    DELETE_LINES = "DeleteLines"
    DELETE_LINES_FILL = "DeleteLinesFill"
    DELETE_WORD = "DeleteWord"
    DELETE_WORD_FILL = "DeleteWordFill"
    DELIVERY_OPTIMIZATION = "DeliveryOptimization"
    DESIGN = "Design"
    DESKTOP_LEAF_TWO = "DesktopLeafTwo"
    DETACHABLE_PC = "DetachablePC"
    DEVICES = "Devices"
    DEVICES2 = "Devices2"
    DEVICES3 = "Devices3"
    DEVICES4 = "Devices4"
    DEVICE_DISCOVERY = "DeviceDiscovery"
    DEVICE_LAPTOP_NO_PIC = "DeviceLaptopNoPic"
    DEVICE_LAPTOP_PIC = "DeviceLaptopPic"
    DEVICE_MONITOR_LEFT_PIC = "DeviceMonitorLeftPic"
    DEVICE_MONITOR_NO_PIC = "DeviceMonitorNoPic"
    DEVICE_MONITOR_RIGHT_PIC = "DeviceMonitorRightPic"
    DEV_UPDATE = "DevUpdate"
    DIAGNOSTIC = "Diagnostic"
    DIAL1 = "Dial1"
    DIAL10 = "Dial10"
    DIAL11 = "Dial11"
    DIAL12 = "Dial12"
    DIAL13 = "Dial13"
    DIAL14 = "Dial14"
    DIAL15 = "Dial15"
    DIAL16 = "Dial16"
    DIAL2 = "Dial2"
    DIAL3 = "Dial3"
    DIAL4 = "Dial4"
    DIAL5 = "Dial5"
    DIAL6 = "Dial6"
    DIAL7 = "Dial7"
    DIAL8 = "Dial8"
    DIAL9 = "Dial9"
    DIALPAD = "Dialpad"
    DIAL_SHAPE1 = "DialShape1"
    DIAL_SHAPE2 = "DialShape2"
    DIAL_SHAPE3 = "DialShape3"
    DIAL_SHAPE4 = "DialShape4"
    DIAL_UP = "DialUp"
    DICTIONARY_CLOUD = "DictionaryCloud"
    DIRECTIONS = "Directions"
    DIRECT_ACCESS = "DirectAccess"
    DISABLE_UPDATES = "DisableUpdates"
    DISCONNECT_DISPLAY = "DisconnectDisplay"
    DISCONNECT_DRIVE = "DisconnectDrive"
    DISLIKE = "Dislike"
    DMC = "DMC"
    DOCK = "Dock"
    DOCK_BOTTOM = "DockBottom"
    DOCK_LEFT = "DockLeft"
    DOCK_LEFT_MIRRORED = "DockLeftMirrored"
    DOCK_RIGHT = "DockRight"
    DOCK_RIGHT_MIRRORED = "DockRightMirrored"
    DOCUMENT_APPROVAL = "DocumentApproval"
    DOUBLE_PINYIN = "DoublePinyin"
    DOWNLOAD_MAP = "DownloadMap"
    DOWN_SHIFT_KEY = "DownShiftKey"
    DPAD = "Dpad"
    DRAW = "Draw"
    DRAW_SOLID = "DrawSolid"
    DRIVING_MODE = "DrivingMode"
    DROP = "Drop"
    DULL_SOUND = "DullSound"
    DULL_SOUND_KEY = "DullSoundKey"
    DUPLEX_LANDSCAPE_ONE_SIDED = "DuplexLandscapeOneSided"
    DUPLEX_LANDSCAPE_ONE_SIDED_MIRRORED = "DuplexLandscapeOneSidedMirrored"
    DUPLEX_LANDSCAPE_TWO_SIDED_LONG_EDGE = "DuplexLandscapeTwoSidedLongEdge"
    DUPLEX_LANDSCAPE_TWO_SIDED_LONG_EDGE_MIRRORED = "DuplexLandscapeTwoSidedLongEdgeMirrored"
    DUPLEX_LANDSCAPE_TWO_SIDED_SHORT_EDGE = "DuplexLandscapeTwoSidedShortEdge"
    DUPLEX_LANDSCAPE_TWO_SIDED_SHORT_EDGE_MIRRORED = "DuplexLandscapeTwoSidedShortEdgeMirrored"
    DUPLEX_PORTRAIT_ONE_SIDED = "DuplexPortraitOneSided"
    DUPLEX_PORTRAIT_ONE_SIDED_MIRRORED = "DuplexPortraitOneSidedMirrored"
    DUPLEX_PORTRAIT_TWO_SIDED_LONG_EDGE = "DuplexPortraitTwoSidedLongEdge"
    DUPLEX_PORTRAIT_TWO_SIDED_LONG_EDGE_MIRRORED = "DuplexPortraitTwoSidedLongEdgeMirrored"
    DUPLEX_PORTRAIT_TWO_SIDED_SHORT_EDGE = "DuplexPortraitTwoSidedShortEdge"
    DUPLEX_PORTRAIT_TWO_SIDED_SHORT_EDGE_MIRRORED = "DuplexPortraitTwoSidedShortEdgeMirrored"
    DYNAMIC_LOCK = "DynamicLock"
    EAR = "Ear"
    EARBUD = "Earbud"
    EARBUDSINGLE = "Earbudsingle"
    EASE_OF_ACCESS = "EaseOfAccess"
    EDIT_MIRRORED = "EditMirrored"
    EDUCATION_ICON = "EducationIcon"
    EFFECTS = "Effects"
    EJECT = "Eject"
    EMI = "EMI"
    EMOJI = "Emoji"
    EMOJI2 = "Emoji2"
    EMOJIPLAY = "Emojiplay"
    EMOJI_BRUSH = "EmojiBrush"
    EMOJI_SWATCH = "EmojiSwatch"
    EMOJI_TAB_CELEBRATION_OBJECTS = "EmojiTabCelebrationObjects"
    EMOJI_TAB_FAVORITES = "EmojiTabFavorites"
    EMOJI_TAB_FOOD_PLANTS = "EmojiTabFoodPlants"
    EMOJI_TAB_MORE_SYMBOLS = "EmojiTabMoreSymbols"
    EMOJI_TAB_PEOPLE = "EmojiTabPeople"
    EMOJI_TAB_SMILES_ANIMALS = "EmojiTabSmilesAnimals"
    EMOJI_TAB_TEXT_SMILES = "EmojiTabTextSmiles"
    EMOJI_TAB_TRANSIT_PLACES = "EmojiTabTransitPlaces"
    END_POINT = "EndPoint"
    END_POINT_SOLID = "EndPointSolid"
    ENGLISH_PUNCTUATION = "EnglishPunctuation"
    EQUALIZER = "Equalizer"
    ERASE_TOOL_FILL = "EraseToolFill"
    ERASE_TOOL_FILL2 = "EraseToolFill2"
    ERROR = "Error"
    ERROR_BADGE = "ErrorBadge"
    ERROR_BADGE12 = "ErrorBadge12"
    ETHERNET = "Ethernet"
    ETHERNET_ERROR = "EthernetError"
    ETHERNET_VPN = "EthernetVPN"
    ETHERNET_WARNING = "EthernetWarning"
    EVENT12 = "Event12"
    EXPAND_TILE = "ExpandTile"
    EXPAND_TILE_MIRRORED = "ExpandTileMirrored"
    EXPLOIT_PROTECTION = "ExploitProtection"
    EXPLOIT_PROTECTION_SETTINGS = "ExploitProtectionSettings"
    EXPLORE_CONTENT = "ExploreContent"
    EXPLORE_CONTENT_SINGLE = "ExploreContentSingle"
    EXPORT = "Export"
    EXPORT_MIRRORED = "ExportMirrored"
    EYEDROPPER = "Eyedropper"
    EYE_GAZE = "EyeGaze"
    EYE_TRACKING = "EyeTracking"
    EYE_TRACKING_TEXT = "EyeTrackingText"
    E_SIM = "eSIM"
    E_SIM_BUSY = "eSIMBusy"
    E_SIM_LOCKED = "eSIMLocked"
    E_SIM_NO_PROFILE = "eSIMNoProfile"
    FAMILY = "Family"
    FAST_FORWARD = "FastForward"
    FAVICON = "Favicon"
    FAVICON2 = "Favicon2"
    FAVORITE_LIST = "FavoriteList"
    FAVORITE_STAR = "FavoriteStar"
    FAVORITE_STAR_FILL = "FavoriteStarFill"
    FEEDBACK_APP = "FeedbackApp"
    FERRY = "Ferry"
    FERRY_SOLID = "FerrySolid"
    FIDO_PASSKEY = "FIDOPasskey"
    FILE_EXPLORER = "FileExplorer"
    FILE_EXPLORER_APP = "FileExplorerApp"
    FINGER_INKING = "FingerInking"
    FLASHLIGHT = "Flashlight"
    FLICK_DOWN = "FlickDown"
    FLICK_LEFT = "FlickLeft"
    FLICK_RIGHT = "FlickRight"
    FLICK_UP = "FlickUp"
    FLOW = "Flow"
    FOLDER_FILL = "FolderFill"
    FOLDER_HORIZONTAL = "FolderHorizontal"
    FOLDER_OPEN = "FolderOpen"
    FOLDER_SELECT = "FolderSelect"
    FONT_COLOR = "FontColor"
    FONT_DECREASE = "FontDecrease"
    FORMAT_TEXT = "FormatText"
    FORWARD = "Forward"
    FORWARD_CALL = "ForwardCall"
    FORWARD_MIRRORED = "ForwardMirrored"
    FORWARD_SM = "ForwardSm"
    FORWARD_SOLID_BOLD = "ForwardSolidBold"
    FOUR_BARS = "FourBars"
    FREE_FORM_CLIPPING = "FreeFormClipping"
    FULL20 = "Full20"
    FULL_ALPHA = "FullAlpha"
    FULL_ALPHA_PRIVATE_MODE = "FullAlphaPrivateMode"
    FULL_CIRCLE_MASK = "FullCircleMask"
    FULL_HIRAGANA = "FullHiragana"
    FULL_HIRAGANA_PRIVATE_MODE = "FullHiraganaPrivateMode"
    FULL_KATAKANA = "FullKatakana"
    FULL_KATAKANA_PRIVATE_MODE = "FullKatakanaPrivateMode"
    FUZZY_READING = "FuzzyReading"
    GAME_CONSOLE = "GameConsole"
    GATEWAY_ROUTER = "GatewayRouter"
    GENERIC_APP = "GenericApp"
    GENERIC_SCAN = "GenericScan"
    GIF = "GIF"
    GIFTBOX_OPEN = "GiftboxOpen"
    GLOBAL_NAV_BUTTON = "GlobalNavButton"
    GLOBE2 = "Globe2"
    GO = "Go"
    GOTO_TODAY = "GotoToday"
    GO_MIRRORED = "GoMirrored"
    GO_TO_MESSAGE = "GoToMessage"
    GO_TO_START = "GoToStart"
    GRID_VIEW = "GridView"
    GRID_VIEW_SMALL = "GridViewSmall"
    GRIPPER_BAR_HORIZONTAL = "GripperBarHorizontal"
    GRIPPER_BAR_VERTICAL = "GripperBarVertical"
    GRIPPER_RESIZE = "GripperResize"
    GRIPPER_RESIZE_MIRRORED = "GripperResizeMirrored"
    GRIPPER_TOOL = "GripperTool"
    GROCERIES = "Groceries"
    GROUP = "Group"
    GROUP_LIST = "GroupList"
    GUEST_USER = "GuestUser"
    HALF_ALPHA = "HalfAlpha"
    HALF_ALPHA_PRIVATE_MODE = "HalfAlphaPrivateMode"
    HALF_DULL_SOUND = "HalfDullSound"
    HALF_KATAKANA = "HalfKatakana"
    HALF_KATAKANA_PRIVATE_MODE = "HalfKatakanaPrivateMode"
    HALF_STAR_LEFT = "HalfStarLeft"
    HALF_STAR_RIGHT = "HalfStarRight"
    HANDWRITING = "Handwriting"
    HANDWRITING20 = "Handwriting20"
    HANG_UP = "HangUp"
    HARD_DRIVE = "HardDrive"
    HEADLESS_DEVICE = "HeadlessDevice"
    HEADPHONE0 = "Headphone0"
    HEADPHONE1 = "Headphone1"
    HEADPHONE2 = "Headphone2"
    HEADPHONE3 = "Headphone3"
    HEADSET = "Headset"
    HEALTH = "Health"
    HEARING_AID = "HearingAid"
    HEART_BROKEN = "HeartBroken"
    HEART_FILL = "HeartFill"
    HELP_MIRRORED = "HelpMirrored"
    HIDE_BCC = "HideBcc"
    HIGHLIGHT_FILL = "HighlightFill"
    HIGHLIGHT_FILL2 = "HighlightFill2"
    HMD = "HMD"
    HOLE_PUNCH_LANDSCAPE_BOTTOM = "HolePunchLandscapeBottom"
    HOLE_PUNCH_LANDSCAPE_LEFT = "HolePunchLandscapeLeft"
    HOLE_PUNCH_LANDSCAPE_RIGHT = "HolePunchLandscapeRight"
    HOLE_PUNCH_LANDSCAPE_TOP = "HolePunchLandscapeTop"
    HOLE_PUNCH_OFF = "HolePunchOff"
    HOLE_PUNCH_PORTRAIT_BOTTOM = "HolePunchPortraitBottom"
    HOLE_PUNCH_PORTRAIT_LEFT = "HolePunchPortraitLeft"
    HOLE_PUNCH_PORTRAIT_RIGHT = "HolePunchPortraitRight"
    HOLE_PUNCH_PORTRAIT_TOP = "HolePunchPortraitTop"
    HOLO_LENS = "HoloLens"
    HOLO_LENS_SELECTED = "HoloLensSelected"
    HOME_GROUP = "HomeGroup"
    HOME_SOLID = "HomeSolid"
    HORIZONTAL_TAB_KEY = "HorizontalTabKey"
    HWP_INSERT = "HWPInsert"
    HWP_JOIN = "HWPJoin"
    HWP_NEW_LINE = "HWPNewLine"
    HWP_OVERWRITE = "HWPOverwrite"
    HWP_SCRATCH_OUT = "HWPScratchOut"
    HWP_SPLIT = "HWPSplit"
    HWP_STRIKE_THROUGH = "HWPStrikeThrough"
    ID_BADGE = "IDBadge"
    IMPORT = "Import"
    IMPORTANT = "Important"
    IMPORTANT_BADGE12 = "ImportantBadge12"
    IMPORT_ALL = "ImportAll"
    IMPORT_ALL_MIRRORED = "ImportAllMirrored"
    IMPORT_MIRRORED = "ImportMirrored"
    INCIDENT_TRIANGLE = "IncidentTriangle"
    INCOMING_CALL = "IncomingCall"
    INFO2 = "Info2"
    INFO_SOLID = "InfoSolid"
    INKING_CARET = "InkingCaret"
    INKING_COLOR_FILL = "InkingColorFill"
    INKING_COLOR_OUTLINE = "InkingColorOutline"
    INKING_TOOL = "InkingTool"
    INKING_TOOL_FILL = "InkingToolFill"
    INKING_TOOL_FILL2 = "InkingToolFill2"
    INPUT = "Input"
    INSIDER_HUB_APP = "InsiderHubApp"
    INSTERT_WORDS = "InstertWords"
    INSTERT_WORDS_FILL = "InstertWordsFill"
    INTERACTIVE_DASHBOARD = "InteractiveDashboard"
    INTERNET_SHARING = "InternetSharing"
    IN_PRIVATE = "InPrivate"
    ITALIC = "Italic"
    I_BEAM = "IBeam"
    I_BEAM_OUTLINE = "IBeamOutline"
    JAPANESE = "Japanese"
    JOIN_WORDS = "JoinWords"
    JOIN_WORDS_FILL = "JoinWordsFill"
    JPN_ROMANJI = "JpnRomanji"
    JPN_ROMANJI_LOCK = "JpnRomanjiLock"
    JPN_ROMANJI_SHIFT = "JpnRomanjiShift"
    JPN_ROMANJI_SHIFT_LOCK = "JpnRomanjiShiftLock"
    KEY12_ON = "Key12On"
    KEYBOARD12_KEY = "Keyboard12Key"
    KEYBOARDSETTINGS20 = "Keyboardsettings20"
    KEYBOARD_BRIGHTNESS = "KeyboardBrightness"
    KEYBOARD_CLASSIC = "KeyboardClassic"
    KEYBOARD_DISMISS = "KeyboardDismiss"
    KEYBOARD_DOCK = "KeyboardDock"
    KEYBOARD_FULL = "KeyboardFull"
    KEYBOARD_LEFT_ALIGNED = "KeyboardLeftAligned"
    KEYBOARD_LEFT_DOCK = "KeyboardLeftDock"
    KEYBOARD_LEFT_HANDED = "KeyboardLeftHanded"
    KEYBOARD_LOWER_BRIGHTNESS = "KeyboardLowerBrightness"
    KEYBOARD_NARROW = "KeyboardNarrow"
    KEYBOARD_ONE_HANDED = "KeyboardOneHanded"
    KEYBOARD_RIGHT_ALIGNED = "KeyboardRightAligned"
    KEYBOARD_RIGHT_DOCK = "KeyboardRightDock"
    KEYBOARD_RIGHT_HANDED = "KeyboardRightHanded"
    KEYBOARD_SETTINGS = "KeyboardSettings"
    KEYBOARD_SHORTCUT = "KeyboardShortcut"
    KEYBOARD_SPLIT = "KeyboardSplit"
    KEYBOARD_STANDARD = "KeyboardStandard"
    KEYBOARD_UNDOCK = "KeyboardUndock"
    KIOSK = "Kiosk"
    KNOWLEDGE_ARTICLE = "KnowledgeArticle"
    KOREAN = "Korean"
    LANDSCAPE_ORIENTATION = "LandscapeOrientation"
    LANDSCAPE_ORIENTATION_MIRRORED = "LandscapeOrientationMirrored"
    LANGUAGE_CHS = "LanguageChs"
    LANGUAGE_CHT = "LanguageCht"
    LANGUAGE_JPN = "LanguageJpn"
    LANGUAGE_KOR = "LanguageKor"
    LANG_JPN = "LangJPN"
    LAPTOP_SECURE = "LaptopSecure"
    LAPTOP_SELECTED = "LaptopSelected"
    LARGE_ERASE = "LargeErase"
    LEAF_TWO = "LeafTwo"
    LEAVE_CHAT = "LeaveChat"
    LEAVE_CHAT_MIRRORED = "LeaveChatMirrored"
    LED_LIGHT = "LEDLight"
    LEFT_ARROW_KEY_TIME0 = "LeftArrowKeyTime0"
    LEFT_DOUBLE_QUOTE = "LeftDoubleQuote"
    LEFT_QUOTE = "LeftQuote"
    LEFT_STICK = "LeftStick"
    LEXICON = "Lexicon"
    LIGHT = "Light"
    LIGHTBULB = "Lightbulb"
    LIGHTNING_BOLT = "LightningBolt"
    LIKE = "Like"
    LIKE_DISLIKE = "LikeDislike"
    LINE_DISPLAY = "LineDisplay"
    LIST = "List"
    LIST_MIRRORED = "ListMirrored"
    LOCALE_LANGUAGE = "LocaleLanguage"
    LOCATION = "Location"
    LOCK = "Lock"
    LOCKSCREEN_DESKTOP = "LockscreenDesktop"
    LOCK_FEEDBACK = "LockFeedback"
    LOCK_SCREEN_GLANCE = "LockScreenGlance"
    LOWER_BRIGHTNESS = "LowerBrightness"
    MAG_STRIPE_READER = "MagStripeReader"
    MAIL_BADGE12 = "MailBadge12"
    MAIL_FILL = "MailFill"
    MAIL_FORWARD = "MailForward"
    MAIL_FORWARD_MIRRORED = "MailForwardMirrored"
    MAIL_REPLY = "MailReply"
    MAIL_REPLY_ALL = "MailReplyAll"
    MAIL_REPLY_ALL_MIRRORED = "MailReplyAllMirrored"
    MAIL_REPLY_MIRRORED = "MailReplyMirrored"
    MANAGE = "Manage"
    MAP_COMPASS_BOTTOM = "MapCompassBottom"
    MAP_COMPASS_TOP = "MapCompassTop"
    MAP_DIRECTIONS = "MapDirections"
    MAP_DRIVE = "MapDrive"
    MAP_LAYERS = "MapLayers"
    MAP_PIN = "MapPin"
    MAP_PIN2 = "MapPin2"
    MARKER = "Marker"
    MARKET_DOWN = "MarketDown"
    MARQUEE = "Marquee"
    MEDIA_STORAGE_TOWER = "MediaStorageTower"
    MEMO = "Memo"
    MERGE_CALL = "MergeCall"
    MICROPHONE_LISTENING = "MicrophoneListening"
    MICROPHONE_SOLID_BOLD = "MicrophoneSolidBold"
    MIC_CLIPPING = "MicClipping"
    MIC_ERROR = "MicError"
    MIC_LOCATION_COMBO = "MicLocationCombo"
    MIC_OFF = "MicOff"
    MIC_OFF2 = "MicOff2"
    MIC_ON = "MicOn"
    MIC_SLEEP = "MicSleep"
    MINI_CONTRACT2_MIRRORED = "MiniContract2Mirrored"
    MINI_EXPAND2_MIRRORED = "MiniExpand2Mirrored"
    MIRACAST_LOGO_LARGE = "MiracastLogoLarge"
    MIRACAST_LOGO_SMALL = "MiracastLogoSmall"
    MIXED_MEDIA_BADGE = "MixedMediaBadge"
    MOBE_SIM = "MobeSIM"
    MOBE_SIM_BUSY = "MobeSIMBusy"
    MOBE_SIM_LOCKED = "MobeSIMLocked"
    MOBE_SIM_NO_PROFILE = "MobeSIMNoProfile"
    MOBILE_LOCKED = "MobileLocked"
    MOBILE_SELECTED = "MobileSelected"
    MOBILE_TABLET = "MobileTablet"
    MOB_ACTION_CENTER = "MobActionCenter"
    MOB_AIRPLANE = "MobAirplane"
    MOB_BATTERY0 = "MobBattery0"
    MOB_BATTERY1 = "MobBattery1"
    MOB_BATTERY10 = "MobBattery10"
    MOB_BATTERY2 = "MobBattery2"
    MOB_BATTERY3 = "MobBattery3"
    MOB_BATTERY4 = "MobBattery4"
    MOB_BATTERY5 = "MobBattery5"
    MOB_BATTERY6 = "MobBattery6"
    MOB_BATTERY7 = "MobBattery7"
    MOB_BATTERY8 = "MobBattery8"
    MOB_BATTERY9 = "MobBattery9"
    MOB_BATTERY_CHARGING0 = "MobBatteryCharging0"
    MOB_BATTERY_CHARGING1 = "MobBatteryCharging1"
    MOB_BATTERY_CHARGING10 = "MobBatteryCharging10"
    MOB_BATTERY_CHARGING2 = "MobBatteryCharging2"
    MOB_BATTERY_CHARGING3 = "MobBatteryCharging3"
    MOB_BATTERY_CHARGING4 = "MobBatteryCharging4"
    MOB_BATTERY_CHARGING5 = "MobBatteryCharging5"
    MOB_BATTERY_CHARGING6 = "MobBatteryCharging6"
    MOB_BATTERY_CHARGING7 = "MobBatteryCharging7"
    MOB_BATTERY_CHARGING8 = "MobBatteryCharging8"
    MOB_BATTERY_CHARGING9 = "MobBatteryCharging9"
    MOB_BATTERY_SAVER0 = "MobBatterySaver0"
    MOB_BATTERY_SAVER1 = "MobBatterySaver1"
    MOB_BATTERY_SAVER10 = "MobBatterySaver10"
    MOB_BATTERY_SAVER2 = "MobBatterySaver2"
    MOB_BATTERY_SAVER3 = "MobBatterySaver3"
    MOB_BATTERY_SAVER4 = "MobBatterySaver4"
    MOB_BATTERY_SAVER5 = "MobBatterySaver5"
    MOB_BATTERY_SAVER6 = "MobBatterySaver6"
    MOB_BATTERY_SAVER7 = "MobBatterySaver7"
    MOB_BATTERY_SAVER8 = "MobBatterySaver8"
    MOB_BATTERY_SAVER9 = "MobBatterySaver9"
    MOB_BATTERY_UNKNOWN = "MobBatteryUnknown"
    MOB_BLUETOOTH = "MobBluetooth"
    MOB_CALL_FORWARDING = "MobCallForwarding"
    MOB_CALL_FORWARDING_MIRRORED = "MobCallForwardingMirrored"
    MOB_DRIVING_MODE = "MobDrivingMode"
    MOB_LOCATION = "MobLocation"
    MOB_NOTIFICATION_BELL = "MobNotificationBell"
    MOB_NOTIFICATION_BELL_FILLED = "MobNotificationBellFilled"
    MOB_QUIET_HOURS = "MobQuietHours"
    MOB_SIGNAL1 = "MobSignal1"
    MOB_SIGNAL2 = "MobSignal2"
    MOB_SIGNAL3 = "MobSignal3"
    MOB_SIGNAL4 = "MobSignal4"
    MOB_SIGNAL5 = "MobSignal5"
    MOB_SIM_ERROR = "MobSIMError"
    MOB_SIM_LOCK = "MobSIMLock"
    MOB_SIM_MISSING = "MobSIMMissing"
    MOB_SNOOZE = "MobSnooze"
    MOB_SNOOZE_FILLED = "MobSnoozeFilled"
    MOB_WIFI1 = "MobWifi1"
    MOB_WIFI2 = "MobWifi2"
    MOB_WIFI3 = "MobWifi3"
    MOB_WIFI4 = "MobWifi4"
    MOB_WIFI_CALL0 = "MobWifiCall0"
    MOB_WIFI_CALL1 = "MobWifiCall1"
    MOB_WIFI_CALL2 = "MobWifiCall2"
    MOB_WIFI_CALL3 = "MobWifiCall3"
    MOB_WIFI_CALL4 = "MobWifiCall4"
    MOB_WIFI_CALL_BARS = "MobWifiCallBars"
    MOB_WIFI_HOTSPOT = "MobWifiHotspot"
    MOB_WIFI_WARNING1 = "MobWifiWarning1"
    MOB_WIFI_WARNING2 = "MobWifiWarning2"
    MOB_WIFI_WARNING3 = "MobWifiWarning3"
    MOB_WIFI_WARNING4 = "MobWifiWarning4"
    MOUSE = "Mouse"
    MOVE_TO_FOLDER = "MoveToFolder"
    MOVIES = "Movies"
    MULTIMEDIA_DMP = "MultimediaDMP"
    MULTIMEDIA_DMS = "MultimediaDMS"
    MULTIMEDIA_DVR = "MultimediaDVR"
    MULTIMEDIA_PMP = "MultimediaPMP"
    MULTI_SELECT = "MultiSelect"
    MULTI_SELECT_MIRRORED = "MultiSelectMirrored"
    MUSIC_ALBUM = "MusicAlbum"
    MUSIC_INFO = "MusicInfo"
    MUSIC_NOTE = "MusicNote"
    MUSIC_SHARING = "MusicSharing"
    MUSIC_SHARING_OFF = "MusicSharingOff"
    MY_NETWORK = "MyNetwork"
    NARRATOR = "Narrator"
    NARRATOR_APP = "NarratorApp"
    NARRATOR_FORWARD = "NarratorForward"
    NARRATOR_FORWARD_MIRRORED = "NarratorForwardMirrored"
    NEARBY_SHARING = "NearbySharing"
    NETWORK = "Network"
    NETWORK_ADAPTER = "NetworkAdapter"
    NETWORK_CONNECTED = "NetworkConnected"
    NETWORK_CONNECTED_CHECKMARK = "NetworkConnectedCheckmark"
    NETWORK_OFFLINE = "NetworkOffline"
    NETWORK_PHYSICAL = "NetworkPhysical"
    NETWORK_PRINTER = "NetworkPrinter"
    NETWORK_SHARING = "NetworkSharing"
    NETWORK_TOWER = "NetworkTower"
    NEW_FOLDER = "NewFolder"
    NEW_WINDOW = "NewWindow"
    NEXT = "Next"
    NOISE_CANCELATION = "NoiseCancelation"
    NOISE_CANCELATION_OFF = "NoiseCancelationOff"
    NUIFP_CONTINUE_SLIDE_ACTION = "NUIFPContinueSlideAction"
    NUIFP_CONTINUE_SLIDE_HAND = "NUIFPContinueSlideHand"
    NUIFP_PRESS_ACTION = "NUIFPPressAction"
    NUIFP_PRESS_HAND = "NUIFPPressHand"
    NUIFP_PRESS_REPEAT_ACTION = "NUIFPPressRepeatAction"
    NUIFP_PRESS_REPEAT_HAND = "NUIFPPressRepeatHand"
    NUIFP_ROLL_LEFT_ACTION = "NUIFPRollLeftAction"
    NUIFP_ROLL_LEFT_HAND = "NUIFPRollLeftHand"
    NUIFP_ROLL_RIGHT_HAND = "NUIFPRollRightHand"
    NUIFP_ROLL_RIGHT_HAND_ACTION = "NUIFPRollRightHandAction"
    NUIFP_START_SLIDE_ACTION = "NUIFPStartSlideAction"
    NUIFP_START_SLIDE_HAND = "NUIFPStartSlideHand"
    NUI_FACE = "NUIFace"
    NUI_IRIS = "NUIIris"
    OEM = "OEM"
    ONE_BAR = "OneBar"
    ONE_HANDED_LEFT20 = "OneHandedLeft20"
    ONE_HANDED_RIGHT20 = "OneHandedRight20"
    OPEN_FILE = "OpenFile"
    OPEN_FOLDER_HORIZONTAL = "OpenFolderHorizontal"
    OPEN_IN_NEW_WINDOW = "OpenInNewWindow"
    OPEN_LOCAL = "OpenLocal"
    OPEN_PANE = "OpenPane"
    OPEN_PANE_MIRRORED = "OpenPaneMirrored"
    OPEN_WITH = "OpenWith"
    OPEN_WITH_MIRRORED = "OpenWithMirrored"
    ORIENTATION = "Orientation"
    OTHER_USER = "OtherUser"
    OUTLINE_HALF_STAR_LEFT = "OutlineHalfStarLeft"
    OUTLINE_HALF_STAR_RIGHT = "OutlineHalfStarRight"
    OUTLINE_QUARTER_STAR_LEFT = "OutlineQuarterStarLeft"
    OUTLINE_QUARTER_STAR_RIGHT = "OutlineQuarterStarRight"
    OUTLINE_STAR_LEFT_HALF = "OutlineStarLeftHalf"
    OUTLINE_STAR_RIGHT_HALF = "OutlineStarRightHalf"
    OUTLINE_THREE_QUARTER_STAR_LEFT = "OutlineThreeQuarterStarLeft"
    OUTLINE_THREE_QUARTER_STAR_RIGHT = "OutlineThreeQuarterStarRight"
    OVERWRITE_WORDS = "OverwriteWords"
    OVERWRITE_WORDS_FILL = "OverwriteWordsFill"
    OVERWRITE_WORDS_FILL_KOREAN = "OverwriteWordsFillKorean"
    OVERWRITE_WORDS_KOREAN = "OverwriteWordsKorean"
    PACKAGE = "Package"
    PAGE = "Page"
    PAGE_MARGIN_LANDSCAPE_MODERATE = "PageMarginLandscapeModerate"
    PAGE_MARGIN_LANDSCAPE_NARROW = "PageMarginLandscapeNarrow"
    PAGE_MARGIN_LANDSCAPE_NORMAL = "PageMarginLandscapeNormal"
    PAGE_MARGIN_LANDSCAPE_WIDE = "PageMarginLandscapeWide"
    PAGE_MARGIN_PORTRAIT_MODERATE = "PageMarginPortraitModerate"
    PAGE_MARGIN_PORTRAIT_NARROW = "PageMarginPortraitNarrow"
    PAGE_MARGIN_PORTRAIT_NORMAL = "PageMarginPortraitNormal"
    PAGE_MARGIN_PORTRAIT_WIDE = "PageMarginPortraitWide"
    PAGE_MIRRORED = "PageMirrored"
    PAGE_SOLID = "PageSolid"
    PAGINATION_DOT_OUTLINE10 = "PaginationDotOutline10"
    PAGINATION_DOT_SOLID10 = "PaginationDotSolid10"
    PAN_MODE = "PanMode"
    PARKING_LOCATION = "ParkingLocation"
    PARKING_LOCATION_MIRRORED = "ParkingLocationMirrored"
    PARKING_LOCATION_SOLID = "ParkingLocationSolid"
    PARTY_LEADER = "PartyLeader"
    PASSIVE_AUTHENTICATION = "PassiveAuthentication"
    PASSWORD_KEY_HIDE = "PasswordKeyHide"
    PASSWORD_KEY_SHOW = "PasswordKeyShow"
    PAUSE_BADGE12 = "PauseBadge12"
    PAYMENT_CARD = "PaymentCard"
    PC1 = "PC1"
    PDF = "PDF"
    PEN = "Pen"
    PENCIL = "Pencil"
    PENCIL_FILL = "PencilFill"
    PEN_PALETTE = "PenPalette"
    PEN_PALETTE_MIRRORED = "PenPaletteMirrored"
    PEN_TIPS = "PenTips"
    PEN_TIPS_MIRRORED = "PenTipsMirrored"
    PEN_WORKSPACE = "PenWorkspace"
    PEN_WORKSPACE_MIRRORED = "PenWorkspaceMirrored"
    PERIOD_KEY = "PeriodKey"
    PERMISSIONS = "Permissions"
    PERSONALIZE = "Personalize"
    PERSONAL_FOLDER = "PersonalFolder"
    PHONE_BOOK = "PhoneBook"
    PHONE_DESKTOP = "PhoneDesktop"
    PHONE_SCREEN = "PhoneScreen"
    PHOTO2 = "Photo2"
    PHOTO_COLLECTION = "PhotoCollection"
    PICTURE = "Picture"
    PINNED = "Pinned"
    PINNED_FILL = "PinnedFill"
    PINYIN_IME_LOGO = "PinyinIMELogo"
    PINYIN_IME_LOGO2 = "PinyinIMELogo2"
    PIN_FILL = "PinFill"
    PIN_PAD = "PINPad"
    PLAP = "PLAP"
    PLAY36 = "Play36"
    PLAYBACK_RATE1X = "PlaybackRate1x"
    PLAYBACK_RATE_OTHER = "PlaybackRateOther"
    PLAYER_SETTINGS = "PlayerSettings"
    PLAY_BADGE12 = "PlayBadge12"
    POI = "POI"
    POINTER_HAND = "PointerHand"
    POINT_ERASE = "PointErase"
    POINT_ERASE_MIRRORED = "PointEraseMirrored"
    POLICE_CAR = "PoliceCar"
    POST_UPDATE = "PostUpdate"
    POWER_BUTTON_UPDATE = "PowerButtonUpdate"
    POWER_BUTTON_UPDATE2 = "PowerButtonUpdate2"
    PPS_FOUR_LANDSCAPE = "PPSFourLandscape"
    PPS_FOUR_PORTRAIT = "PPSFourPortrait"
    PPS_ONE_LANDSCAPE = "PPSOneLandscape"
    PPS_ONE_PORTRAIT = "PPSOnePortrait"
    PPS_TWO_LANDSCAPE = "PPSTwoLandscape"
    PPS_TWO_PORTRAIT = "PPSTwoPortrait"
    PRESENCE_CHICKLET = "PresenceChicklet"
    PRESENCE_CHICKLET_VIDEO = "PresenceChickletVideo"
    PREVIEW = "Preview"
    PREVIEW_LINK = "PreviewLink"
    PREVIOUS = "Previous"
    PRINTER3_D = "Printer3D"
    PRINTFAX_PRINTER_FILE = "PrintfaxPrinterFile"
    PRINT_ALL_PAGES = "PrintAllPages"
    PRINT_CUSTOM_RANGE = "PrintCustomRange"
    PRINT_DEFAULT = "PrintDefault"
    PRIORITY = "Priority"
    PRIVATE_CALL = "PrivateCall"
    PROCESS = "Process"
    PROCESSING = "Processing"
    PRODUCTIVITY_MODE = "ProductivityMode"
    PROGRESS_RING_DOTS = "ProgressRingDots"
    PROJECT = "Project"
    PROJECT_TO_DEVICE = "ProjectToDevice"
    PROTECTED_DOCUMENT = "ProtectedDocument"
    PROTRACTOR = "Protractor"
    PROVISIONING_PACKAGE = "ProvisioningPackage"
    PUNC_KEY = "PuncKey"
    PUNC_KEY0 = "PuncKey0"
    PUNC_KEY1 = "PuncKey1"
    PUNC_KEY2 = "PuncKey2"
    PUNC_KEY3 = "PuncKey3"
    PUNC_KEY4 = "PuncKey4"
    PUNC_KEY5 = "PuncKey5"
    PUNC_KEY6 = "PuncKey6"
    PUNC_KEY7 = "PuncKey7"
    PUNC_KEY8 = "PuncKey8"
    PUNC_KEY9 = "PuncKey9"
    PUNC_KEY_LEFT_BOTTOM = "PuncKeyLeftBottom"
    PUNC_KEY_RIGHT_BOTTOM = "PuncKeyRightBottom"
    PUZZLE = "Puzzle"
    QUARENTINED_ITEMS = "QuarentinedItems"
    QUARENTINED_ITEMS_MIRRORED = "QuarentinedItemsMirrored"
    QUARTER_STAR_LEFT = "QuarterStarLeft"
    QUARTER_STAR_RIGHT = "QuarterStarRight"
    QUIET_HOURS_BADGE12 = "QuietHoursBadge12"
    QWERTY_OFF = "QWERTYOff"
    QWERTY_ON = "QWERTYOn"
    RADAR = "Radar"
    RADIO_BTN_OFF = "RadioBtnOff"
    RADIO_BTN_ON = "RadioBtnOn"
    RADIO_BULLET = "RadioBullet"
    RADIO_BULLET2 = "RadioBullet2"
    RAM = "RAM"
    READ = "Read"
    READING_LIST = "ReadingList"
    READING_MODE = "ReadingMode"
    READ_OUT_LOUD = "ReadOutLoud"
    RECEIPT_PRINTER = "ReceiptPrinter"
    RECENT = "Recent"
    RECORD = "Record"
    RECORD2 = "Record2"
    RECTANGULAR_CLIPPING = "RectangularClipping"
    REDO = "Redo"
    RED_EYE = "RedEye"
    REFRESH = "Refresh"
    RELATIONSHIP = "Relationship"
    REMEMBERED_DEVICE = "RememberedDevice"
    REMINDER = "Reminder"
    REMINDER_FILL = "ReminderFill"
    REMOTE = "Remote"
    RENAME = "Rename"
    REPAIR = "Repair"
    REPEAT_ALL = "RepeatAll"
    REPEAT_OFF = "RepeatOff"
    REPEAT_ONE = "RepeatOne"
    REPLAY = "Replay"
    REPLY = "Reply"
    REPLY_MIRRORED = "ReplyMirrored"
    REPORT_DOCUMENT = "ReportDocument"
    REPORT_HACKED = "ReportHacked"
    RESET_DEVICE = "ResetDevice"
    RESET_DRIVE = "ResetDrive"
    RESHARE = "Reshare"
    RESIZE_MOUSE_LARGE = "ResizeMouseLarge"
    RESIZE_MOUSE_MEDIUM = "ResizeMouseMedium"
    RESIZE_MOUSE_MEDIUM_MIRRORED = "ResizeMouseMediumMirrored"
    RESIZE_MOUSE_SMALL = "ResizeMouseSmall"
    RESIZE_MOUSE_SMALL_MIRRORED = "ResizeMouseSmallMirrored"
    RESIZE_MOUSE_TALL = "ResizeMouseTall"
    RESIZE_MOUSE_TALL_MIRRORED = "ResizeMouseTallMirrored"
    RESIZE_MOUSE_WIDE = "ResizeMouseWide"
    RESIZE_TOUCH_LARGER = "ResizeTouchLarger"
    RESIZE_TOUCH_NARROWER = "ResizeTouchNarrower"
    RESIZE_TOUCH_NARROWER_MIRRORED = "ResizeTouchNarrowerMirrored"
    RESIZE_TOUCH_SHORTER = "ResizeTouchShorter"
    RESIZE_TOUCH_SMALLER = "ResizeTouchSmaller"
    RESTART_UPDATE = "RestartUpdate"
    RESTART_UPDATE2 = "RestartUpdate2"
    RETURN_KEY = "ReturnKey"
    RETURN_KEY_LG = "ReturnKeyLg"
    RETURN_KEY_SM = "ReturnKeySm"
    RETURN_TO_CALL = "ReturnToCall"
    RETURN_TO_WINDOW = "ReturnToWindow"
    REVEAL_PASSWORD_MEDIUM = "RevealPasswordMedium"
    REV_TOGGLE_KEY = "RevToggleKey"
    REWIND = "Rewind"
    RIGHT_ARROW_KEY_TIME0 = "RightArrowKeyTime0"
    RIGHT_ARROW_KEY_TIME1 = "RightArrowKeyTime1"
    RIGHT_ARROW_KEY_TIME2 = "RightArrowKeyTime2"
    RIGHT_ARROW_KEY_TIME3 = "RightArrowKeyTime3"
    RIGHT_ARROW_KEY_TIME4 = "RightArrowKeyTime4"
    RIGHT_DOUBLE_QUOTE = "RightDoubleQuote"
    RIGHT_QUOTE = "RightQuote"
    RIGHT_STICK = "RightStick"
    RINGER_BADGE12 = "RingerBadge12"
    RINGER_SILENT = "RingerSilent"
    ROAMING_DOMESTIC = "RoamingDomestic"
    ROAMING_INTERNATIONAL = "RoamingInternational"
    ROTATE_CAMERA = "RotateCamera"
    ROTATE_MAP_LEFT = "RotateMapLeft"
    ROTATE_MAP_RIGHT = "RotateMapRight"
    ROTATION_LOCK = "RotationLock"
    RTT_LOGO = "RTTLogo"
    RULER = "Ruler"
    SAFE = "Safe"
    SAVE_LOCAL = "SaveLocal"
    SCAN = "Scan"
    SCREEN_TIME = "ScreenTime"
    SCROLL_MODE = "ScrollMode"
    SCROLL_UP_DOWN = "ScrollUpDown"
    SD_CARD = "SDCard"
    SEARCH_AND_APPS = "SearchAndApps"
    SEARCH_MEDIUM = "SearchMedium"
    SELECT_ALL = "SelectAll"
    SEND_FILL_MIRRORED = "SendFillMirrored"
    SEND_MIRRORED = "SendMirrored"
    SENSOR = "Sensor"
    SET = "Set"
    SETLOCK_SCREEN = "SetlockScreen"
    SETTINGS = "Settings"
    SETTINGS_BATTERY = "SettingsBattery"
    SETTINGS_DISPLAY_SOUND = "SettingsDisplaySound"
    SETTINGS_SOLID = "SettingsSolid"
    SET_HISTORY_STATUS = "SetHistoryStatus"
    SET_HISTORY_STATUS2 = "SetHistoryStatus2"
    SET_SOLID = "SetSolid"
    SET_TILE = "SetTile"
    SHARE_BROADBAND = "ShareBroadband"
    SHIELD = "Shield"
    SHOP = "Shop"
    SHOW_BCC = "ShowBcc"
    SHOW_RESULTS = "ShowResults"
    SHOW_RESULTS_MIRRORED = "ShowResultsMirrored"
    SHUFFLE = "Shuffle"
    SIGNAL_BARS1 = "SignalBars1"
    SIGNAL_BARS2 = "SignalBars2"
    SIGNAL_BARS3 = "SignalBars3"
    SIGNAL_BARS4 = "SignalBars4"
    SIGNAL_BARS5 = "SignalBars5"
    SIGNAL_BARS_VPN2 = "SignalBarsVPN2"
    SIGNAL_BARS_VPN3 = "SignalBarsVPN3"
    SIGNAL_BARS_VPN4 = "SignalBarsVPN4"
    SIGNAL_BARS_VPN5 = "SignalBarsVPN5"
    SIGNAL_BARS_VPN_ROAMING3 = "SignalBarsVPNRoaming3"
    SIGNAL_BARS_VPN_ROAMING4 = "SignalBarsVPNRoaming4"
    SIGNAL_BARS_VPN_ROAMING5 = "SignalBarsVPNRoaming5"
    SIGNAL_ERROR = "SignalError"
    SIGNAL_NOT_CONNECTED = "SignalNotConnected"
    SIGNAL_ROAMING = "SignalRoaming"
    SIGNATURE_CAPTURE = "SignatureCapture"
    SIGN_OUT = "SignOut"
    SIM_ERROR = "SIMError"
    SIM_LOCK = "SIMLock"
    SIM_MISSING = "SIMMissing"
    SIP_MOVE = "SIPMove"
    SIP_REDOCK = "SIPRedock"
    SIP_UNDOCK = "SIPUndock"
    SKIP_BACK10 = "SkipBack10"
    SKIP_FORWARD30 = "SkipForward30"
    SLIDER_THUMB = "SliderThumb"
    SLIDESHOW = "Slideshow"
    SLOW_MOTION_ON = "SlowMotionOn"
    SMALL_ERASE = "SmallErase"
    SMARTCARD = "Smartcard"
    SMARTCARD_VIRTUAL = "SmartcardVirtual"
    SMART_SCREEN = "SmartScreen"
    SNOOZE = "Snooze"
    SORT = "Sort"
    SPATIAL_VOLUME0 = "SpatialVolume0"
    SPATIAL_VOLUME1 = "SpatialVolume1"
    SPATIAL_VOLUME2 = "SpatialVolume2"
    SPATIAL_VOLUME3 = "SpatialVolume3"
    SPECIAL_EFFECT_SIZE = "SpecialEffectSize"
    SPEECH = "Speech"
    SPEECH_SOLID_BOLD = "SpeechSolidBold"
    SPELLING = "Spelling"
    SPELLING_CHINESE = "SpellingChinese"
    SPELLING_KOREAN = "SpellingKorean"
    SPELLING_SERBIAN = "SpellingSerbian"
    SPLIT20 = "Split20"
    STAPLING_LANDSCAPE_BOOK_BINDING = "StaplingLandscapeBookBinding"
    STAPLING_LANDSCAPE_BOTTOM_LEFT = "StaplingLandscapeBottomLeft"
    STAPLING_LANDSCAPE_BOTTOM_RIGHT = "StaplingLandscapeBottomRight"
    STAPLING_LANDSCAPE_TOP_LEFT = "StaplingLandscapeTopLeft"
    STAPLING_LANDSCAPE_TOP_RIGHT = "StaplingLandscapeTopRight"
    STAPLING_LANDSCAPE_TWO_BOTTOM = "StaplingLandscapeTwoBottom"
    STAPLING_LANDSCAPE_TWO_LEFT = "StaplingLandscapeTwoLeft"
    STAPLING_LANDSCAPE_TWO_RIGHT = "StaplingLandscapeTwoRight"
    STAPLING_LANDSCAPE_TWO_TOP = "StaplingLandscapeTwoTop"
    STAPLING_OFF = "StaplingOff"
    STAPLING_PORTRAIT_BOOK_BINDING = "StaplingPortraitBookBinding"
    STAPLING_PORTRAIT_BOTTOM_LEFT = "StaplingPortraitBottomLeft"
    STAPLING_PORTRAIT_BOTTOM_RIGHT = "StaplingPortraitBottomRight"
    STAPLING_PORTRAIT_TOP_LEFT = "StaplingPortraitTopLeft"
    STAPLING_PORTRAIT_TOP_RIGHT = "StaplingPortraitTopRight"
    STAPLING_PORTRAIT_TWO_BOTTOM = "StaplingPortraitTwoBottom"
    STAPLING_PORTRAIT_TWO_LEFT = "StaplingPortraitTwoLeft"
    STAPLING_PORTRAIT_TWO_RIGHT = "StaplingPortraitTwoRight"
    STAPLING_PORTRAIT_TWO_TOP = "StaplingPortraitTwoTop"
    START_POINT = "StartPoint"
    START_POINT_SOLID = "StartPointSolid"
    START_PRESENTING = "StartPresenting"
    STATUS_CHECKMARK = "StatusCheckmark"
    STATUS_CHECKMARK7 = "StatusCheckmark7"
    STATUS_CHECKMARK_LEFT = "StatusCheckmarkLeft"
    STATUS_CIRCLE = "StatusCircle"
    STATUS_CIRCLE7 = "StatusCircle7"
    STATUS_CIRCLE_BLOCK = "StatusCircleBlock"
    STATUS_CIRCLE_BLOCK2 = "StatusCircleBlock2"
    STATUS_CIRCLE_CHECKMARK = "StatusCircleCheckmark"
    STATUS_CIRCLE_ERROR_X = "StatusCircleErrorX"
    STATUS_CIRCLE_EXCLAMATION = "StatusCircleExclamation"
    STATUS_CIRCLE_INFO = "StatusCircleInfo"
    STATUS_CIRCLE_INNER = "StatusCircleInner"
    STATUS_CIRCLE_LEFT = "StatusCircleLeft"
    STATUS_CIRCLE_OUTER = "StatusCircleOuter"
    STATUS_CIRCLE_QUESTION_MARK = "StatusCircleQuestionMark"
    STATUS_CIRCLE_RING = "StatusCircleRing"
    STATUS_CIRCLE_SYNC = "StatusCircleSync"
    STATUS_CONNECTING1 = "StatusConnecting1"
    STATUS_CONNECTING2 = "StatusConnecting2"
    STATUS_DATA_TRANSFER = "StatusDataTransfer"
    STATUS_DATA_TRANSFER_ROAMING = "StatusDataTransferRoaming"
    STATUS_DATA_TRANSFER_VPN = "StatusDataTransferVPN"
    STATUS_DUAL_SIM1 = "StatusDualSIM1"
    STATUS_DUAL_SIM1_VPN = "StatusDualSIM1VPN"
    STATUS_DUAL_SIM2 = "StatusDualSIM2"
    STATUS_DUAL_SIM2_VPN = "StatusDualSIM2VPN"
    STATUS_ERROR = "StatusError"
    STATUS_ERROR_CIRCLE7 = "StatusErrorCircle7"
    STATUS_ERROR_FULL = "StatusErrorFull"
    STATUS_ERROR_LEFT = "StatusErrorLeft"
    STATUS_EXCLAMATION_CIRCLE7 = "StatusExclamationCircle7"
    STATUS_INFO = "StatusInfo"
    STATUS_INFO_LEFT = "StatusInfoLeft"
    STATUS_PAUSE7 = "StatusPause7"
    STATUS_SECURED = "StatusSecured"
    STATUS_SGLTE = "StatusSGLTE"
    STATUS_SGLTE_CELL = "StatusSGLTECell"
    STATUS_SGLTE_DATA_VPN = "StatusSGLTEDataVPN"
    STATUS_TRIANGLE = "StatusTriangle"
    STATUS_TRIANGLE_EXCLAMATION = "StatusTriangleExclamation"
    STATUS_TRIANGLE_INNER = "StatusTriangleInner"
    STATUS_TRIANGLE_LEFT = "StatusTriangleLeft"
    STATUS_TRIANGLE_OUTER = "StatusTriangleOuter"
    STATUS_UNSECURE = "StatusUnsecure"
    STATUS_VPN = "StatusVPN"
    STATUS_WARNING = "StatusWarning"
    STATUS_WARNING_LEFT = "StatusWarningLeft"
    STICKER2 = "Sticker2"
    STOCK_DOWN = "StockDown"
    STOCK_UP = "StockUp"
    STOP = "Stop"
    STOP_POINT = "StopPoint"
    STOP_POINT_SOLID = "StopPointSolid"
    STOP_PRESENTING = "StopPresenting"
    STOP_SLIDE_SHOW = "StopSlideShow"
    STOP_SOLID = "StopSolid"
    STORAGE_NETWORK_WIRELESS = "StorageNetworkWireless"
    STORAGE_OPTICAL = "StorageOptical"
    STORAGE_TAPE = "StorageTape"
    STREAMING = "Streaming"
    STREAMING_ENTERPRISE = "StreamingEnterprise"
    STREET = "Street"
    STREETSIDE_SPLIT_EXPAND = "StreetsideSplitExpand"
    STREETSIDE_SPLIT_MINIMIZE = "StreetsideSplitMinimize"
    STRIKETHROUGH = "Strikethrough"
    STROKE_ERASE = "StrokeErase"
    STROKE_ERASE2 = "StrokeErase2"
    STROKE_ERASE_MIRRORED = "StrokeEraseMirrored"
    SUBSCRIPTION_ADD = "SubscriptionAdd"
    SUBSCRIPTION_ADD_MIRRORED = "SubscriptionAddMirrored"
    SUBTITLES = "Subtitles"
    SUBTITLES_AUDIO = "SubtitlesAudio"
    SUBTRACT_BOLD = "SubtractBold"
    SURFACE_HUB = "SurfaceHub"
    SURFACE_HUB_SELECTED = "SurfaceHubSelected"
    SUSTAINABLE = "Sustainable"
    SWIPE = "Swipe"
    SWIPE_REVEAL_ART = "SwipeRevealArt"
    SWITCH = "Switch"
    SWITCH_APPS = "SwitchApps"
    SWITCH_USER = "SwitchUser"
    SYNC_BADGE12 = "SyncBadge12"
    SYNC_ERROR = "SyncError"
    SYNC_FOLDER = "SyncFolder"
    SYSTEM = "System"
    TABLET = "Tablet"
    TABLET_MODE = "TabletMode"
    TABLET_SELECTED = "TabletSelected"
    TAP_AND_SEND = "TapAndSend"
    TASKBAR_PHONE = "TaskbarPhone"
    TASK_MANAGER_APP = "TaskManagerApp"
    TASK_VIEW = "TaskView"
    TASK_VIEW_EXPANDED = "TaskViewExpanded"
    TASK_VIEW_SETTINGS = "TaskViewSettings"
    TEXT_BULLET_LIST_SQUARE = "TextBulletListSquare"
    TEXT_EDIT = "TextEdit"
    TEXT_NAVIGATE = "TextNavigate"
    TEXT_SELECT = "TextSelect"
    THIS_PC = "ThisPC"
    THOUGHT_BUBBLE = "ThoughtBubble"
    THREE_BARS = "ThreeBars"
    THREE_QUARTER_STAR_LEFT = "ThreeQuarterStarLeft"
    THREE_QUARTER_STAR_RIGHT = "ThreeQuarterStarRight"
    TILT_DOWN = "TiltDown"
    TILT_UP = "TiltUp"
    TIME_LANGUAGE = "TimeLanguage"
    TOGGLE_BORDER = "ToggleBorder"
    TOGGLE_FILLED = "ToggleFilled"
    TOGGLE_LEFT = "ToggleLeft"
    TOGGLE_RIGHT = "ToggleRight"
    TOGGLE_THUMB = "ToggleThumb"
    TOLL_SOLID = "TollSolid"
    TOOL_TIP = "ToolTip"
    TOUCH = "Touch"
    TOUCHPAD = "Touchpad"
    TOUCHSCREEN = "Touchscreen"
    TOUCH_POINTER = "TouchPointer"
    TRACKERS = "Trackers"
    TRACKERS_MIRRORED = "TrackersMirrored"
    TRAFFIC_CONGESTION_SOLID = "TrafficCongestionSolid"
    TRAFFIC_LIGHT = "TrafficLight"
    TRAIN_SOLID = "TrainSolid"
    TREE_FOLDER_FOLDER = "TreeFolderFolder"
    TREE_FOLDER_FOLDER_FILL = "TreeFolderFolderFill"
    TREE_FOLDER_FOLDER_OPEN = "TreeFolderFolderOpen"
    TREE_FOLDER_FOLDER_OPEN_FILL = "TreeFolderFolderOpenFill"
    TRIGGER_LEFT = "TriggerLeft"
    TRIGGER_RIGHT = "TriggerRight"
    TRIM = "Trim"
    TV_MONITOR = "TVMonitor"
    TV_MONITOR_SELECTED = "TVMonitorSelected"
    TWO_BARS = "TwoBars"
    TWO_PAGE = "TwoPage"
    TYPE = "Type"
    UNDERLINE = "Underline"
    UNDERSCORE_SPACE = "UnderscoreSpace"
    UNDO = "Undo"
    UNFAVORITE = "Unfavorite"
    UNINSTALL = "Uninstall"
    UNKNOWN = "Unknown"
    UNKNOWN_MIRRORED = "UnknownMirrored"
    UNLOCK = "Unlock"
    UNSYNC_FOLDER = "UnsyncFolder"
    UPDATE_RESTORE = "UpdateRestore"
    UPDATE_STATUS_DOT = "UpdateStatusDot"
    UPDATE_STATUS_DOT2 = "UpdateStatusDot2"
    UPLOAD = "Upload"
    UP_ARROW_SHIFT_KEY = "UpArrowShiftKey"
    UP_SHIFT_KEY = "UpShiftKey"
    USB = "USB"
    USB_SAFE_CONNECT = "USBSafeConnect"
    USER_APN = "UserAPN"
    USER_REMOVE = "UserRemove"
    VERTICAL_BATTERY0 = "VerticalBattery0"
    VERTICAL_BATTERY1 = "VerticalBattery1"
    VERTICAL_BATTERY10 = "VerticalBattery10"
    VERTICAL_BATTERY2 = "VerticalBattery2"
    VERTICAL_BATTERY3 = "VerticalBattery3"
    VERTICAL_BATTERY4 = "VerticalBattery4"
    VERTICAL_BATTERY5 = "VerticalBattery5"
    VERTICAL_BATTERY6 = "VerticalBattery6"
    VERTICAL_BATTERY7 = "VerticalBattery7"
    VERTICAL_BATTERY8 = "VerticalBattery8"
    VERTICAL_BATTERY9 = "VerticalBattery9"
    VERTICAL_BATTERY_CHARGING0 = "VerticalBatteryCharging0"
    VERTICAL_BATTERY_CHARGING1 = "VerticalBatteryCharging1"
    VERTICAL_BATTERY_CHARGING10 = "VerticalBatteryCharging10"
    VERTICAL_BATTERY_CHARGING2 = "VerticalBatteryCharging2"
    VERTICAL_BATTERY_CHARGING3 = "VerticalBatteryCharging3"
    VERTICAL_BATTERY_CHARGING4 = "VerticalBatteryCharging4"
    VERTICAL_BATTERY_CHARGING5 = "VerticalBatteryCharging5"
    VERTICAL_BATTERY_CHARGING6 = "VerticalBatteryCharging6"
    VERTICAL_BATTERY_CHARGING7 = "VerticalBatteryCharging7"
    VERTICAL_BATTERY_CHARGING8 = "VerticalBatteryCharging8"
    VERTICAL_BATTERY_CHARGING9 = "VerticalBatteryCharging9"
    VERTICAL_BATTERY_UNKNOWN = "VerticalBatteryUnknown"
    VIBRATE = "Vibrate"
    VIDEO360 = "Video360"
    VIDEO_CAPTURE = "VideoCapture"
    VIDEO_CHAT = "VideoChat"
    VIDEO_SOLID = "VideoSolid"
    VIEW_ALL = "ViewAll"
    VIEW_DASHBOARD = "ViewDashboard"
    VIRTUAL_MACHINE_GROUP = "VirtualMachineGroup"
    VOICE_CALL = "VoiceCall"
    VOLUME0 = "Volume0"
    VOLUME1 = "Volume1"
    VOLUME2 = "Volume2"
    VOLUME3 = "Volume3"
    VOLUME_BARS = "VolumeBars"
    VOLUME_DISABLED = "VolumeDisabled"
    VPN_OVERLAY = "VPNOverlay"
    VPN_ROAMING_OVERLY = "VPNRoamingOverly"
    WALK = "Walk"
    WALK_SOLID = "WalkSolid"
    WARNING = "Warning"
    WEBCAM = "Webcam"
    WEBCAM2 = "Webcam2"
    WEBSITE = "Website"
    WEB_SEARCH = "WebSearch"
    WHEEL = "Wheel"
    WIFI1 = "Wifi1"
    WIFI2 = "Wifi2"
    WIFI3 = "Wifi3"
    WIFI_ATTENTION_OVERLAY = "WifiAttentionOverlay"
    WIFI_CALL0 = "WifiCall0"
    WIFI_CALL1 = "WifiCall1"
    WIFI_CALL2 = "WifiCall2"
    WIFI_CALL3 = "WifiCall3"
    WIFI_CALL4 = "WifiCall4"
    WIFI_CALL_BARS = "WifiCallBars"
    WIFI_ERROR0 = "WifiError0"
    WIFI_ERROR1 = "WifiError1"
    WIFI_ERROR2 = "WifiError2"
    WIFI_ERROR3 = "WifiError3"
    WIFI_ERROR4 = "WifiError4"
    WIFI_ETHERNET = "WifiEthernet"
    WIFI_HOTSPOT = "WifiHotspot"
    WIFI_VPN3 = "WifiVPN3"
    WIFI_VPN4 = "WifiVPN4"
    WIFI_VPN5 = "WifiVPN5"
    WIFI_WARNING0 = "WifiWarning0"
    WIFI_WARNING1 = "WifiWarning1"
    WIFI_WARNING2 = "WifiWarning2"
    WIFI_WARNING3 = "WifiWarning3"
    WIFI_WARNING4 = "WifiWarning4"
    WINDOWS_INSIDER = "WindowsInsider"
    WINDOW_SNIPPING = "WindowSnipping"
    WIND_DIRECTION = "WindDirection"
    WIRE = "Wire"
    WIRED_USB = "WiredUSB"
    WIRELESS_USB = "WirelessUSB"
    WORK = "Work"
    WORK_SOLID = "WorkSolid"
    WORLD = "World"
    XBOX_ONE_CONSOLE = "XboxOneConsole"
    ZERO_BARS = "ZeroBars"
    ZOOM_MODE = "ZoomMode"

    def path(self, theme=Theme.AUTO):
        return f':/qfluentwidgets/images/icons/{self.value}_{getIconColor(theme)}.svg'


class Icon(QIcon):

    def __init__(self, fluentIcon: FluentIcon):
        super().__init__(fluentIcon.path())
        self.fluentIcon = fluentIcon


def toQIcon(icon: Union[QIcon, FluentIconBase, str]) -> QIcon:
    """ convet `icon` to `QIcon` """
    if isinstance(icon, str):
        return QIcon(icon)

    if isinstance(icon, FluentIconBase):
        return icon.icon()

    return icon


class Action(QAction):
    """ Fluent action

    Constructors
    ------------
    * Action(`parent`: QWidget = None, `**kwargs`)
    * Action(`text`: str, `parent`: QWidget = None, `**kwargs`)
    * Action(`icon`: QIcon | FluentIconBase, `parent`: QWidget = None, `**kwargs`)
    """

    @singledispatchmethod
    def __init__(self, parent: QObject = None, **kwargs):
        super().__init__(parent, **kwargs)
        self.fluentIcon = None

    @__init__.register
    def _(self, text: str, parent: QObject = None, **kwargs):
        super().__init__(text, parent, **kwargs)
        self.fluentIcon = None

    @__init__.register
    def _(self, icon: QIcon, text: str, parent: QObject = None, **kwargs):
        super().__init__(icon, text, parent, **kwargs)
        self.fluentIcon = None

    @__init__.register
    def _(self, icon: FluentIconBase, text: str, parent: QObject = None, **kwargs):
        super().__init__(icon.icon(), text, parent, **kwargs)
        self.fluentIcon = icon

    def icon(self) -> QIcon:
        if self.fluentIcon:
            return Icon(self.fluentIcon)

        return super().icon()

    def setIcon(self, icon: Union[FluentIconBase, QIcon]):
        if isinstance(icon, FluentIconBase):
            self.fluentIcon = icon
            icon = icon.icon()

        super().setIcon(icon)
