## Settings
PyQt-Fluent-Widgets presents each configuration item as a `SettingCard` on the interface. The behavior of user on the `SettingCard` will change the value of the configuration item, and PyQt-Fluent-Widgets will update the configuration item to the json configuration file automatically.

### Config
PyQt-Fluent-Widgets uses the `ConfigItem` class to represent a configuration item and uses the `QConfig` class to read and write the value of `ConfigItem`. The `QConfig` class will automatically update the configuration file when the value of the `ConfigItem` changes.

Since the value in config file may be manually modified by the user to an invalid value, PyQt-Fluent-Widgets use `ConfigValidator` and its subclass to verify and correct the config value.

Json files only support string, boolean value, list and dict, for enumeration classes or `QColor`, we can't use `json.dump()` to write them directly into a json file, so PyQt-Fluent-Widgets provides `ConfigSerializer` and its subclass to serialize and deserialize config item from config file. For example, you can use `ColorSerializer` to serialize config items with `QColor` value type.

`ConfigItem` has the following attributes:

|  Attribute   |        Type        | Description                                                  |
| :----------: | :----------------: | ------------------------------------------------------------ |
|   `group`    |       `str`        | The group to which the config item belongs                   |
|    `name`    |       `str`        | Name of config item                                          |
|  `default`   |       `Any`        | The default value of config item, it will be used when the value in the config file is illegal |
| `validator`  | `ConfigValidator`  | Config validator                                             |
| `serializer` | `ConfigSerializer` | Config serializer                                            |
|  `restart`   |       `bool`       | Whether to restart the application after updating value      |

You should add config items to the class attribute of `QConfig` subclasss,  then use `qconfig.load()` to load config file, for example:

```python
class MvQuality(Enum):
    """ MV quality enumeration class """

    FULL_HD = "Full HD"
    HD = "HD"
    SD = "SD"
    LD = "LD"

    @staticmethod
    def values():
        return [q.value for q in MvQuality]


class Config(QConfig):
    """ Config of application """

    # main window
    enableAcrylic = ConfigItem("MainWindow", "EnableAcrylic", False, BoolValidator())
    playBarColor = ColorConfigItem("MainWindow", "PlayBarColor", "#225C7F")
    themeMode = OptionsConfigItem("MainWindow", "ThemeMode", "Light", OptionsValidator(["Light", "Dark", "Auto"]), restart=True)
    recentPlaysNumber = RangeConfigItem("MainWindow", "RecentPlayNumbers", 300, RangeValidator(10, 300))

    # online
    onlineMvQuality = OptionsConfigItem("Online", "MvQuality", MvQuality.FULL_HD, OptionsValidator(MvQuality), EnumSerializer(MvQuality))


# create config object and initialize it
cfg = Config()
qconfig.load('config/config.json', cfg)
```

### Setting card

PyQt-Fluent-Widgets provides many kinds of setting card:

|          Class           | Description                                                  |
| :----------------------: | ------------------------------------------------------------ |
|     `HyperlinkCard`      | Setting card with a hyper link                               |
|    `ColorSettingCard`    | Setting card with a color picker                             |
| `CustomColorSettingCard` | Setting card with a button to choose color                   |
|   `ComboBoxSettingCard`  | Setting card with a combo box                                |
|    `RangeSettingCard`    | Setting card with a slider                                   |
|    `PushSettingCard`     | Setting card with a naive push button                        |
| `PrimaryPushSettingCard` | Setting card with a push button highlighted in the background |
|   `SwitchSettingCard`    | Setting card with a switch button                            |
|   `OptionsSettingCard`   | Setting card with a group of radio buttons                   |
| `FolderListSettingCard`  | Setting card for showing and managing folder list            |

You can use `SettingCardGroup.addSettingCard()` to add a setting card to the same group, and `SettingCardGroup` will adjust its layout automatically based on the height of setting cards.

For the usage of these components, see [settings_ interface.py](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/settings/setting_interface.py).


