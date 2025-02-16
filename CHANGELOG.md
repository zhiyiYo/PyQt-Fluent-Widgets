# 更新日志

## v1.7.5
### 新特性
* 添加 `InfoBar` 桌面通知功能
* 更新工具提示样式

### 修复
* 修复菜单无法显示工具提示的问题 ([#1053](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/1053))
* 修复多媒体组件播放按钮重复触发的问题 ([#1054](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/1054))
* 修复 `HyperlinkButton` 禁用状态下的图标颜色问题 ([#1038](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/1038))

## v1.7.4
### 新组件
* 添加 `SimpleExpandGroupSettingCard`

### 新特性
* 添加禁用下拉框选项的功能 ([#1026](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/1026))

### 修复
* 修复侧边导航栏的触控板滚动问题
* 修复导航栏在展开子项时无法自动扩展问题 ([#1029](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/1029))
* 修复 `FastCalendarPicker` 无法选择第一个日期的问题 ([#1028](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/1028))

## v1.7.3

### 修复
* 修复表格项工具提示没有及时隐藏的问题

## v1.7.2
### 新特性
* 重绘单选按钮 ([#1010](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/1010))
* 添加表格项工具提示 ([#1017](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/1017))
* 添加输入框的 Error 状态 ([#1012](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/1012))

### 修复
* 修复 InfoBar 会导致主进程退出的问题 ([#1006](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/1006))
* 修复 macOS 深色模式下对话框的确定按钮显示聚焦框的问题 ([#1014](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/1014))


## v1.7.1
### 新特性
* 添加头像组件显示名称的功能

### 修复
* 修复 macos 下 Pivot 的布局问题
* 修复 FlipView 圆角被视口挡住的问题 ([#995](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/995))
* 修复表格和列表组件设置不可选中模式不起作用的问题 ([#992](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/992))
* 修复 ExpandSettingCard 标签样式受到父级样式表影响的问题 ([#993](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/993))
* 修复 ExpandGroupSettingCard 动态删减组件时的高度计算问题 ([#1002](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/1002))

## v1.7.0
### 新组件
* 添加快速日历选择器 `FastCalendarPicker` ([#983](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/983))
* 添加富文本浏览器 `TextBrowser` ([#972](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/972))

### 新特性
* 添加系统主题监听器 ([#954](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/954))
* 添加下拉框 activated 信号 ([#978](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/978))
* 添加输入框自定义动作的功能 ([#987](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/987))
* 添加点击遮罩关闭对话框的功能 ([#957](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/957))
* 添加对话框验证表单数据的接口 ([#967](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/967))
* 添加 ImageLabel 设置任意分辨率的功能
* 添加设置 Pivot 和 BreadcrumbBar 导航项文本的功能

### 修复
* 修复内存泄漏问题 ([#963](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/954), [#977](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/954))
* 修复遮罩对话框颜色问题 ([#964](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/954))
* 修复清空菜单不彻底的问题 ([#988](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/954))
* 修复二级菜单显示位置错误问题 ([#844](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/954))
* 修复 IconInfoBadge.info 位置错误 ([#950](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/954))
* 修复 ExpandLayout 坐标计算问题 ([#941](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/954))
* 修复 SegmentedWidget.clear 报错的问题 ([#975](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/954))
* 修复手风琴设置卡滚动事件被拦截的问题 ([#945](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/954))

## v1.6.0
### 新组件
* 添加分组卡片组件 `GroupHeaderCardWidget` ([#920](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/920))

### 新特性
* 添加俄罗斯语翻译文件 ([#923](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/923))
* 添加滚动区域透明背景接口 ([#912](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/912))
* 添加 Pivot 当前选项变化信号 ([#908](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/908))
* 添加 FlowLayout 插入组件的功能 ([#886](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/886))
* 添加 FlipView 惰性加载图片的功能 ([#907](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/907))
* 添加自定义侧边导航栏文本颜色的功能 ([#826](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/826))
* 更新 FluentWindow 浅色模式下的默认背景颜色 ([#928](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/928))
* 添加自定义 `FluentIconBase` 亮暗模式颜色的功能 ([#927](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/927))


### 修复
* 修复滚动事件被拦截的问题
* 修复 Pivot 指示器位置问题 ([#888](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/888))
* 修复 VideoWidget 停止播放的问题 ([#143](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/143))
* 修复 SegmentedWidget 图标偏移的问题 ([#888](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/888))
* 修复对话框报错 `QPainter::begin` 的问题 ([#867](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/867))
* 修复 MessageBoxBase 重复触发信号的问题 ([#915](https://github.com/zhiyiYo/PyQt-Fluent-Widgets/issues/915))