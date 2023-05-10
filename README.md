<p align="center">
  <img width="18%" align="center" src="https://raw.githubusercontent.com/zhiyiYo/PyQt-Fluent-Widgets/master/docs/source/_static/logo.png" alt="logo">
</p>
  <h1 align="center">
  PyQt6-Fluent-Widgets
</h1>
<p align="center">
  A fluent design widgets library based on PyQt6
</p>

<p align="center">
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Win32%20|%20Linux%20|%20macOS-blue?color=#4ec820" alt="Platform Win32 | Linux | macOS"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://static.pepy.tech/personalized-badge/pyqt6-fluent-widgets?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads" alt="Download"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/PyQt-6.3.1-blue?color=#4ec820" alt="PyQt 6.3.1"/>
  </a>
</p>

![Interface](https://raw.githubusercontent.com/zhiyiYo/PyQt-Fluent-Widgets/master/docs/source/_static/Interface.jpg)


## Install
To install lite version (`AcrylicLabel` is not available):
```shell
pip install PyQt6-Fluent-Widgets -i https://pypi.org/simple/
```
Or install full-featured version:
```shell
pip install "PyQt6-Fluent-Widgets[full]" -i https://pypi.org/simple/
```

## Run Example
After installing PyQt-Fluent-Widgets package using pip, you can run any demo in the examples directory, for example:
```python
cd examples/gallery
python demo.py
```

If you encounter `ImportError: cannot import name 'XXX' from 'qfluentwidgets'`, it indicates that the package version you installed is too low. You can replace the mirror source with https://pypi.org/simple and reinstall again.

## Documentation
Want to know more about PyQt-Fluent-Widgets? Please read the [help document](https://pyqt-fluent-widgets.readthedocs.io/) 👈

## Video Demonstration
Check out this [▶ example video](https://www.bilibili.com/video/BV12c411L73q) that shows off what PyQt-Fluent-Widgets are capable of 🎉

## Work with QtDesigner
You can use PyQt6-Fluent-Widgets in QtDesigner directly by running `python ./tools/designer.py`. If the operation is successful, you should be able to see the PyQt-Fluent-Widgets in the sidebar of QtDesigner.
> **NOTE**
> It is recommended to install pyqt6-plugins and PyQt6-Fluent-Widgets in a virtual environment.

## See Also
Here are some projects that use PyQt-Fluent-Widgets:
* [**zhiyiYo/Groove**: A cross-platform music player based on PyQt5](https://github.com/zhiyiYo/Groove)
* [**zhiyiYo/Alpha-Gobang-Zero**: A gobang robot based on reinforcement learning](https://github.com/zhiyiYo/Alpha-Gobang-Zero)

## Reference
* [**Windows design**: Design guidelines and toolkits for creating native app experiences](https://learn.microsoft.com/zh-cn/windows/apps/design/)
* [**Microsoft/WinUI-Gallery**: An app demonstrates the controls available in WinUI and the Fluent Design System](https://github.com/microsoft/WinUI-Gallery)

## License
PyQt-Fluent-Widgets is licensed under [GPLv3](./LICENSE).

Copyright © 2021 by zhiyiYo.
