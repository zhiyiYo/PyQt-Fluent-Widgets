## Theme

### Theme mode
You can use the `setTheme()` method to switch the light/dark theme of PyQt-Fluent-Widgets. The parameter of `setTheme()` accepts the following three values:
* `Theme.LIGHT`: Light theme
* `Theme.DARK`: Dark theme
* `Theme.AUTO`: Follow system theme. If the system theme cannot be detected, the light theme will be used.

When the theme changes, the config instance managed by `qconfig` (i.e., the config object passed in using the `qconfig.load()` method) will emit the `themeChanged` signal.

If you want to automatically switch the interface style when the theme changes, you can inherit `StyleSheetBase` and override the `path()` method. Suppose you have a `MainWindow` class and its qss file paths are `app/resource/qss/light/main_window.qss` and `app/resource/qss/dark/main_window.qss`, the code can be written like this:

```python
from enum import Enum
from qfluentwidgets import StyleSheetBase, Theme, isDarkTheme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet  """

    MAIN_WINDOW = "main_window"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f"app/resource/qss/{theme.value.lower()}/{self.value}.qss"


class MainWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # apply style sheet to main window
        StyleSheet.MAIN_WINDOW.apply(self)
```


### Theme color
You can use `setThemeColor()` method to change the theme color of PyQt-Fluent-Widgets. This method accepts the following three types of parameters:
* `QColor`
* `Qt.GlobalColor`
* `str`: Hex color strings or color names, such as `#0065d5` or `red`.

When the theme color changes, `qconfig` will emit the `themeColorChanged` signal.