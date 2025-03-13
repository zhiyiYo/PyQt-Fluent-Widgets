<p align="center">
  <img width="18%" align="center" src="https://raw.githubusercontent.com/zhiyiYo/PyQt-Fluent-Widgets/master/docs/source/_static/logo.png" alt="logo">
</p>
  <h1 align="center">
  PySide2-Fluent-Widgets
</h1>
<p align="center">
  A fluent design widgets library based on PySide2
</p>

<div align="center">

[![Version](https://img.shields.io/pypi/v/pyside2-fluent-widgets?color=%2334D058&label=Version)](https://pypi.org/project/PyQt-Fluent-Widgets)
[![Download](https://static.pepy.tech/personalized-badge/pyside2-fluent-widgets?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)]()
[![GPLv3](https://img.shields.io/badge/License-GPLv3-blue?color=#4ec820)](LICENSE)
[![Platform Win32 | Linux | macOS](https://img.shields.io/badge/Platform-Win32%20|%20Linux%20|%20macOS-blue?color=#4ec820)]()

</div>


<p align="center">
English | <a href="docs/README_zh.md">简体中文</a>
</p>

![Interface](https://raw.githubusercontent.com/zhiyiYo/PyQt-Fluent-Widgets/master/docs/source/_static/Interface.jpg)


## Install
To install lite version (`AcrylicLabel` is not available):
```shell
pip install PySide2-Fluent-Widgets -i https://pypi.org/simple/
```
Or install full-featured version:
```shell
pip install "PySide2-Fluent-Widgets[full]" -i https://pypi.org/simple/
```


The [Pro version](https://qfluentwidgets.com/pages/pro) library contains more advance components. You can download `PyQt-Fluent-Widgets-Pro-Gallery.zip` from the [release page](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/releases) for preview purposes.

C++ QFluentWidgets require purchasing a license from the [official website](https://qfluentwidgets.com/price). You can also download the compiled demo `C++_QFluentWidgets.zip` from the [release page](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/releases).

> [!Warning]
> Don't install PyQt-Fluent-Widgets, PyQt6-Fluent-Widgets, PySide2-Fluent-Widgets and PySide6-Fluent-Widgets at the same time, because their package names are all `qfluentwidgets`.


## Run Example
After installing PySide2-Fluent-Widgets package using pip, you can run any demo in the examples directory, for example:
```shell
cd examples/gallery
python demo.py
```

If you encounter `ImportError: cannot import name 'XXX' from 'qfluentwidgets'`, it indicates that the package version you installed is too low. You can replace the mirror source with https://pypi.org/simple and reinstall again.

## Documentation
Want to know more about PySide2-Fluent-Widgets? Please read the [help document](https://qfluentwidgets.com) 👈


## License
PySide2-Fluent-Widgets adopts dual licenses. Non-commercial usage is licensed under [GPLv3](./LICENSE). For commercial purposes, please purchase [commercial license](https://qfluentwidgets.com/price) to support the development of this project.

Copyright © 2021 by zhiyiYo.


## Work with Designer
[Fluent Client](https://www.youtube.com/watch?v=7UCmcsOlhTk) integrates designer plugins, supporting direct drag-and-drop usage of QFluentWidgets components in Designer. You can purchase the client from [TaoBao](https://item.taobao.com/item.htm?ft=t&id=767961666600) or [Afdian](https://afdian.com/item/6726fcc4247311ef8c6852540025c377).

![Fluent Designer](https://img.fastmirror.net/s/2024/02/18/65d22363d4a73.jpg)


## See Also
Here are some projects based on PyQt-Fluent-Widgets:
* [**zhiyiYo/Fluent-M3U8**: A cross-platform m3u8 downloader](https://fluent-m3u8.org)
* [**zhiyiYo/Groove**: A cross-platform music player based on PyQt5](https://github.com/zhiyiYo/Groove)
* [**zhiyiYo/Alpha-Gobang-Zero**: A gobang robot based on reinforcement learning](https://github.com/zhiyiYo/Alpha-Gobang-Zero)

## Reference
* [**Windows design**: Design guidelines and toolkits for creating native app experiences](https://learn.microsoft.com/zh-cn/windows/apps/design/)
* [**Microsoft/WinUI-Gallery**: An app demonstrates the controls available in WinUI and the Fluent Design System](https://github.com/microsoft/WinUI-Gallery)
