<p align="center">
  <img width="18%" align="center" src="https://raw.githubusercontent.com/zhiyiYo/PyQt-Fluent-Widgets/master/docs/source/_static/logo.png" alt="logo">
</p>
  <h1 align="center">
  PySide6-Fluent-Widgets
</h1>
<p align="center">
  A fluent design widgets library based on PySide6
</p>

<p align="center">
  <a href="https://pypi.org/project/PyQt-Fluent-Widgets" target="_blank">
    <img src="https://img.shields.io/pypi/v/pyqt-fluent-widgets?color=%2334D058&label=Version" alt="Version">
  </a>

  <a style="text-decoration:none">
    <img src="https://static.pepy.tech/personalized-badge/pyside2-fluent-widgets?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads" alt="Download"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/License-GPLv3-blue?color=#4ec820" alt="GPLv3"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Win32%20|%20Linux%20|%20macOS-blue?color=#4ec820" alt="Platform Win32 | Linux | macOS"/>
  </a>
</p>


<p align="center">
English | <a href="docs/README_zh.md">简体中文</a> | <a href="https://qfluentwidgets.com/">官网</a>
</p>

![Interface](https://raw.githubusercontent.com/zhiyiYo/PyQt-Fluent-Widgets/master/docs/source/_static/Interface.jpg)


## Install
To install lite version (`AcrylicLabel` is not available):
```shell
pip install PySide6-Fluent-Widgets -i https://pypi.org/simple/
```
Or install full-featured version:
```shell
pip install "PySide6-Fluent-Widgets[full]" -i https://pypi.org/simple/
```

The [Pro version](https://qfluentwidgets.com/pages/pro) library contains more advance components. You can download `PyQt-Fluent-Widgets-Pro-Gallery.zip` from the [release page](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/releases) for preview purposes.

C++ QFluentWidgets require purchasing a license from the [official website](https://qfluentwidgets.com/price). You can also download the compiled demo `C++_QFluentWidgets.zip` from the [release page](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/releases).

> **Warning**
> Don't install PyQt-Fluent-Widgets, PyQt6-Fluent-Widgets, PySide2-Fluent-Widgets and PySide6-Fluent-Widgets at the same time, because their package names are all `qfluentwidgets`.


## Run Example
After installing PySide6-Fluent-Widgets package using pip, you can run any demo in the examples directory, for example:
```python
cd examples/gallery
python demo.py
```

If you encounter `ImportError: cannot import name 'XXX' from 'qfluentwidgets'`, it indicates that the package version you installed is too low. You can replace the mirror source with https://pypi.org/simple and reinstall again.

## Documentation
Want to know more about PySide6-Fluent-Widgets? Please read the [help document](https://qfluentwidgets.com) 👈


## License
PySide6-Fluent-Widgets adopts dual licenses. Non-commercial usage is licensed under [GPLv3](./LICENSE). For commercial purposes, please purchase [commercial license](https://qfluentwidgets.com/price) to support the development of this project.

Copyright © 2021 by zhiyiYo.


## Video Demonstration
Check out this [▶ example video](https://www.bilibili.com/video/BV12c411L73q) that shows off what PyQt-Fluent-Widgets are capable of 🎉

## Support
If this project helps you a lot and you want to support the development and maintenance of this project, feel free to sponsor me via [爱发电](https://afdian.net/a/zhiyiYo) or [ko-fi](https://ko-fi.com/zhiyiYo). Your support is highly appreciated 🥰

## See Also
Here are some projects based on PyQt-Fluent-Widgets:
* [**zhiyiYo/QMaterialWidgets**: A material design widgets library based on PySide](https://qmaterialwidgets.vercel.app)
* [**zhiyiYo/Groove**: A cross-platform music player based on PyQt5](https://github.com/zhiyiYo/Groove)
* [**zhiyiYo/Alpha-Gobang-Zero**: A gobang robot based on reinforcement learning](https://github.com/zhiyiYo/Alpha-Gobang-Zero)

## Reference
* [**Windows design**: Design guidelines and toolkits for creating native app experiences](https://learn.microsoft.com/zh-cn/windows/apps/design/)
* [**Microsoft/WinUI-Gallery**: An app demonstrates the controls available in WinUI and the Fluent Design System](https://github.com/microsoft/WinUI-Gallery)
