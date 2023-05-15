<p align="center">
  <img width="18%" align="center" src="https://raw.githubusercontent.com/zhiyiYo/PyQt-Fluent-Widgets/master/docs/source/_static/logo.png" alt="logo">
</p>
  <h1 align="center">
  PySide6-Fluent-Widgets
</h1>
<p align="center">
  基于 PySide6 的 Fluent Design 风格组件库
</p>

<p align="center">
  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/Platform-Win32%20|%20Linux%20|%20macOS-blue?color=#4ec820" alt="Platform Win32 | Linux | macOS"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://static.pepy.tech/personalized-badge/pyqt-fluent-widgets?period=total&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads" alt="Download"/>
  </a>

  <a style="text-decoration:none">
    <img src="https://img.shields.io/badge/License-GPLv3-blue?color=#4ec820" alt="GPLv3"/>
  </a>
</p>

<p align="center">
<a href="../README.md">English</a> | 简体中文
</p>

![Interface](https://raw.githubusercontent.com/zhiyiYo/PyQt-Fluent-Widgets/master/docs/source/_static/Interface.jpg)


## 安装📥
安装轻量版 (`AcrylicLabel` 不可用)：
```shell
pip install PySide6-Fluent-Widgets -i https://pypi.org/simple/
```
安装完整版：
```shell
pip install "PySide-Fluent-Widgets[full]" -i https://pypi.org/simple/
```

> **Warning**
> 请勿同时安装 PyQt-Fluent-Widgets、PyQt6-Fluent-Widgets、PySide2-Fluent-Widgets 和 PySide6-Fluent-Widgets，因为他们的包名都是 `qfluentwidgets`


## 运行示例▶️
使用 pip 安装好 PySide6-Fluent-Widgets 包并下载好此仓库的代码之后，就可以运行 examples 目录下的任意示例程序，比如：
```python
cd examples/gallery
python demo.py
```

如果遇到 `ImportError: cannot import name 'XXX' from 'qfluentwidgets'`，这表明安装的包版本过低。可以按照上面的安装指令将 pypi 源替换为 https://pypi.org/simple 并重新安装.

## 在线文档📕
想要了解 PyQt-Fluent-Widgets 的正确使用姿势？请仔细阅读 [帮助文档](https://pyqt-fluent-widgets.readthedocs.io/zh_CN/latest/) 👈

## 演示视频📽️
请查收哔哩哔哩上的 [视频合集](https://www.bilibili.com/video/BV12c411L73q)，它展示了 PySide6-Fluent-Widgets 的全部组件和特性 🎉

## 搭配 QtDesigner🚀
切换到 PyQt5 分支（PySide6 的插件不稳定），运行 `python ./tools/designer.py` 启动安装了 PyQt-Fluent-Widgets 插件的 QtDesigner。如果操作成功，QtDesigner 的侧边栏中将会显示 PyQt-Fluent-Widgets 的组件。对于旧项目的改造，推荐使用 [视频教程](https://www.bilibili.com/video/BV1na4y1V7jH) 中介绍的 `提升为...`。

> **Note**
> 推荐在虚拟环境中安装 pyqt5-tools 和 PyQt-Fluent-Widgets，并确保 PyQt5-Frameless-Window 的版本号 >= 0.2.7，不然可能出现各种奇怪的问题。

## 支持💖
如果您正在使用这个项目并感觉良好，或者是想支持我继续开发，可以通过 [爱发电](https://afdian.net/a/zhiyiYo) 或者 [ko-fi](https://ko-fi.com/zhiyiYo) 请我喝一杯奶茶，还能获得相应的奖励哦😊。非常感谢您的支持与鼓励 🥰

## 加入我们🚩
可以在 [ Discord ](https://discord.gg/mYZME3wraK) 上和我们一起交流探讨，分享自己对这个组件库的新发现和新想法 🚀

## 另见👀
下面是一些使用了 PyQt-Fluent-Widgets 的项目：
* [**zhiyiYo/Groove**: A cross-platform music player based on PyQt5](https://github.com/zhiyiYo/Groove)
* [**zhiyiYo/Alpha-Gobang-Zero**: A gobang robot based on reinforcement learning](https://github.com/zhiyiYo/Alpha-Gobang-Zero)

## 参考
* [**Windows design**: Design guidelines and toolkits for creating native app experiences](https://learn.microsoft.com/zh-cn/windows/apps/design/)
* [**Microsoft/WinUI-Gallery**: An app demonstrates the controls available in WinUI and the Fluent Design System](https://github.com/microsoft/WinUI-Gallery)

## 许可证
PySide6-Fluent-Widgets 使用双许可证。非商业用途使用 [GPLv3](../LICENSE) 许可证进行授权，商用请在 [爱发电](https://afdian.net/a/zhiyiYo) 或者 [ko-fi](https://ko-fi.com/s/b5000d2dd7) 上进行购买以支持作者的开发。

Copyright © 2021 by zhiyiYo.