## Icon
Many widgets need icons, if you want PyQt-Fluent-Widgets change your icons automatically when the theme changes, then you can inherit `FluentIconBase` and overide `path()` method. Here is an example:

```python
from enum import Enum

from qfluentwidgets import getIconColor, Theme, FluentIconBase


class MyFluentIcon(FluentIconBase, Enum):
    """ Custom icons """

    ADD = "Add"
    CUT = "Cut"
    COPY = "Copy"

    def path(self, theme=Theme.AUTO):
        if theme == Theme.AUTO:
            c = getIconColor()
        else:
            c = "white" if theme == Theme.DARK else "black"

        return f':/icons/{self.value}_{c}.svg'
```