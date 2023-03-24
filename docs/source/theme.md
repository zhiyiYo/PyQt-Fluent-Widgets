## Theme

### Theme mode
You can use the `setTheme()` method to switch the light/dark theme of PyQt-Fluent-Widgets. The parameter of `setTheme()` accepts the following three values:
* `Theme.LIGHT`: Light theme
* `Theme.DARK`: Dark theme
* `Theme.AUTO`: Follow system theme. If the system theme cannot be detected, the light theme will be used.

When the theme changes, `qconfig` will emit the `themeChanged` signal.

### Theme color
You can use `setThemeColor()` method to change the theme color of PyQt-Fluent-Widgets. This method accepts the following three types of parameters:
* `QColor`
* `Qt.GlobalColor`
* `str`: Hex color strings or color names, such as `#0065d5` or `red`.