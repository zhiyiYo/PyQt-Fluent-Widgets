# coding:utf-8
import json
from copy import deepcopy
from enum import Enum
from pathlib import Path
from typing import List

import darkdetect
from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QColor

from .exception_handler import exceptionHandler


ALERT = "\n\033[1;33m📢 Tips:\033[0m QFluentWidgets Pro is now released. Click \033[1;96mhttps://qfluentwidgets.com/pages/pro\033[0m to learn more about it.\n"


class Theme(Enum):
    """ Theme enumeration """

    LIGHT = "Light"
    DARK = "Dark"
    AUTO = "Auto"


class ConfigValidator:
    """ Config validator """

    def validate(self, value):
        """ Verify whether the value is legal """
        return True

    def correct(self, value):
        """ correct illegal value """
        return value


class RangeValidator(ConfigValidator):
    """ Range validator """

    def __init__(self, min, max):
        self.min = min
        self.max = max
        self.range = (min, max)

    def validate(self, value):
        return self.min <= value <= self.max

    def correct(self, value):
        return min(max(self.min, value), self.max)


class OptionsValidator(ConfigValidator):
    """ Options validator """

    def __init__(self, options):
        if not options:
            raise ValueError("The `options` can't be empty.")

        if isinstance(options, Enum):
            options = options._member_map_.values()

        self.options = list(options)

    def validate(self, value):
        return value in self.options

    def correct(self, value):
        return value if self.validate(value) else self.options[0]


class BoolValidator(OptionsValidator):
    """ Boolean validator """

    def __init__(self):
        super().__init__([True, False])


class FolderValidator(ConfigValidator):
    """ Folder validator """

    def validate(self, value):
        return Path(value).exists()

    def correct(self, value):
        path = Path(value)
        path.mkdir(exist_ok=True, parents=True)
        return str(path.absolute()).replace("\\", "/")


class FolderListValidator(ConfigValidator):
    """ Folder list validator """

    def validate(self, value):
        return all(Path(i).exists() for i in value)

    def correct(self, value: List[str]):
        folders = []
        for folder in value:
            path = Path(folder)
            if path.exists():
                folders.append(str(path.absolute()).replace("\\", "/"))

        return folders


class ColorValidator(ConfigValidator):
    """ RGB color validator """

    def __init__(self, default):
        self.default = QColor(default)

    def validate(self, color):
        try:
            return QColor(color).isValid()
        except:
            return False

    def correct(self, value):
        return QColor(value) if self.validate(value) else self.default


class ConfigSerializer:
    """ Config serializer """

    def serialize(self, value):
        """ serialize config value """
        return value

    def deserialize(self, value):
        """ deserialize config from config file's value """
        return value


class EnumSerializer(ConfigSerializer):
    """ enumeration class serializer """

    def __init__(self, enumClass):
        self.enumClass = enumClass

    def serialize(self, value):
        return value.value

    def deserialize(self, value):
        return self.enumClass(value)


class ColorSerializer(ConfigSerializer):
    """ QColor serializer """

    def serialize(self, value: QColor):
        return value.name(QColor.HexArgb)

    def deserialize(self, value):
        if isinstance(value, list):
            return QColor(*value)

        return QColor(value)


class ConfigItem(QObject):
    """ Config item """

    valueChanged = Signal(object)

    def __init__(self, group, name, default, validator=None, serializer=None, restart=False):
        """
        Parameters
        ----------
        group: str
            config group name

        name: str
            config item name, can be empty

        default:
            default value

        options: list
            options value

        serializer: ConfigSerializer
            config serializer

        restart: bool
            whether to restart the application after updating value
        """
        super().__init__()
        self.group = group
        self.name = name
        self.validator = validator or ConfigValidator()
        self.serializer = serializer or ConfigSerializer()
        self.__value = default
        self.value = default
        self.restart = restart
        self.defaultValue = self.validator.correct(default)

    @property
    def value(self):
        """ get the value of config item """
        return self.__value

    @value.setter
    def value(self, v):
        v = self.validator.correct(v)
        ov = self.__value
        self.__value = v
        if ov != v:
            self.valueChanged.emit(v)

    @property
    def key(self):
        """ get the config key separated by `.` """
        return self.group+"."+self.name if self.name else self.group

    def __str__(self):
        return f'{self.__class__.__name__}[value={self.value}]'

    def serialize(self):
        return self.serializer.serialize(self.value)

    def deserializeFrom(self, value):
        self.value = self.serializer.deserialize(value)


class RangeConfigItem(ConfigItem):
    """ Config item of range """

    @property
    def range(self):
        """ get the available range of config """
        return self.validator.range

    def __str__(self):
        return f'{self.__class__.__name__}[range={self.range}, value={self.value}]'


class OptionsConfigItem(ConfigItem):
    """ Config item with options """

    @property
    def options(self):
        return self.validator.options

    def __str__(self):
        return f'{self.__class__.__name__}[options={self.options}, value={self.value}]'


class ColorConfigItem(ConfigItem):
    """ Color config item """

    def __init__(self, group, name, default, restart=False):
        super().__init__(group, name, QColor(default), ColorValidator(default),
                         ColorSerializer(), restart)

    def __str__(self):
        return f'{self.__class__.__name__}[value={self.value.name()}]'


class QConfig(QObject):
    """ Config of app """

    appRestartSig = Signal()
    themeChanged = Signal(Theme)
    themeChangedFinished = Signal()
    themeColorChanged = Signal(QColor)

    themeMode = OptionsConfigItem(
        "QFluentWidgets", "ThemeMode", Theme.LIGHT, OptionsValidator(Theme), EnumSerializer(Theme))
    themeColor = ColorConfigItem("QFluentWidgets", "ThemeColor", '#009faa')

    def __init__(self):
        super().__init__()
        self.file = Path("config/config.json")
        self._theme = Theme.LIGHT
        self._cfg = self

    def get(self, item):
        """ get the value of config item """
        return item.value

    def set(self, item, value, save=True, copy=True):
        """ set the value of config item

        Parameters
        ----------
        item: ConfigItem
            config item

        value:
            the new value of config item

        save: bool
            whether to save the change to config file

        copy: bool
            whether to deep copy the new value
        """
        if item.value == value:
            return

        # deepcopy new value
        try:
            item.value = deepcopy(value) if copy else value
        except:
            item.value = value

        if save:
            self.save()

        if item.restart:
            self._cfg.appRestartSig.emit()

        if item is self._cfg.themeMode:
            self.theme = value
            self._cfg.themeChanged.emit(value)

        if item is self._cfg.themeColor:
            self._cfg.themeColorChanged.emit(value)

    def toDict(self, serialize=True):
        """ convert config items to `dict` """
        items = {}
        for name in dir(self._cfg.__class__):
            item = getattr(self._cfg.__class__, name)
            if not isinstance(item, ConfigItem):
                continue

            value = item.serialize() if serialize else item.value
            if not items.get(item.group):
                if not item.name:
                    items[item.group] = value
                else:
                    items[item.group] = {}

            if item.name:
                items[item.group][item.name] = value

        return items

    def save(self):
        """ save config """
        self._cfg.file.parent.mkdir(parents=True, exist_ok=True)
        with open(self._cfg.file, "w", encoding="utf-8") as f:
            json.dump(self._cfg.toDict(), f, ensure_ascii=False, indent=4)

    @exceptionHandler()
    def load(self, file=None, config=None):
        """ load config

        Parameters
        ----------
        file: str or Path
            the path of json config file

        config: Config
            config object to be initialized
        """
        if isinstance(config, QConfig):
            self._cfg = config
            self._cfg.themeChanged.connect(self.themeChanged)

        if isinstance(file, (str, Path)):
            self._cfg.file = Path(file)

        try:
            with open(self._cfg.file, encoding="utf-8") as f:
                cfg = json.load(f)
        except:
            cfg = {}

        # map config items'key to item
        items = {}
        for name in dir(self._cfg.__class__):
            item = getattr(self._cfg.__class__, name)
            if isinstance(item, ConfigItem):
                items[item.key] = item

        # update the value of config item
        for k, v in cfg.items():
            if not isinstance(v, dict) and items.get(k) is not None:
                items[k].deserializeFrom(v)
            elif isinstance(v, dict):
                for key, value in v.items():
                    key = k + "." + key
                    if items.get(key) is not None:
                        items[key].deserializeFrom(value)

        self.theme = self.get(self._cfg.themeMode)

    @property
    def theme(self):
        """ get theme mode, can be `Theme.Light` or `Theme.Dark` """
        return self._cfg._theme

    @theme.setter
    def theme(self, t):
        """ chaneg the theme without modifying the config file """
        if t == Theme.AUTO:
            t = darkdetect.theme()
            t = Theme(t) if t else Theme.LIGHT

        self._cfg._theme = t


qconfig = QConfig()
try:
    print(ALERT)
except UnicodeEncodeError:
    print(ALERT.replace("📢", ""))


def isDarkTheme():
    """ whether the theme is dark mode """
    return qconfig.theme == Theme.DARK

def theme():
    """ get theme mode """
    return qconfig.theme

def isDarkThemeMode(theme=Theme.AUTO):
    """ whether the theme is dark mode """
    return theme == Theme.DARK if theme != Theme.AUTO else isDarkTheme()