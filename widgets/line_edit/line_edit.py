# coding:utf-8
from PyQt5.QtCore import QEasingCurve, QEvent, QPropertyAnimation, QRect, Qt
from PyQt5.QtGui import QContextMenuEvent, QIcon
from PyQt5.QtWidgets import QAction, QApplication, QLineEdit, QMenu

from three_state_button import ThreeStateButton
from window_effect import WindowEffect


class LineEdit(QLineEdit):
    """ 包含清空按钮的单行输入框 """

    def __init__(self, text=None, parent=None):
        super().__init__(text, parent)
        # 鼠标点击次数
        iconPath_dict = {
            "normal": "resource/images/清空_normal.png",
            "hover": "resource/images/清空_hover.png",
            "pressed": "resource/images/清空_pressed.png",
        }
        self.clearButton = ThreeStateButton(iconPath_dict, self)
        self.menu = LineEditMenu(self)
        self.__clickedTime = 0
        self.__initWidget()

    def __initWidget(self):
        """ 初始化小部件 """
        self.resize(300, 40)
        self.setTextMargins(0, 0, self.clearButton.width(), 0)
        self.clearButton.hide()
        self.textChanged.connect(self.textChangedEvent)
        # 安装事件过滤器
        self.clearButton.installEventFilter(self)
        # 设置层叠样式
        with open('resource/style/line_edit.qss', encoding='utf-8') as f:
            self.setStyleSheet(f.read())

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            # 如果已经全选了再次点击就取消全选
            if self.__clickedTime == 0:
                self.selectAll()
            else:
                # 需要调用父类的鼠标点击事件，不然无法部分选中
                super().mousePressEvent(e)
            self.setFocus()
            # 如果输入框中有文本，就设置为只读并显示清空按钮
            if self.text():
                self.clearButton.show()
        self.__clickedTime += 1

    def contextMenuEvent(self, e: QContextMenuEvent):
        """ 设置右击菜单 """
        self.menu.exec_(e.globalPos())

    def focusOutEvent(self, e):
        """ 当焦点移到别的输入框时隐藏按钮 """
        # 调用父类的函数，消除焦点
        super().focusOutEvent(e)
        self.__clickedTime = 0
        self.clearButton.hide()

    def textChangedEvent(self):
        """ 如果输入框中文本改变且此时清空按钮不可见，就显示清空按钮 """
        if self.text() and not self.clearButton.isVisible():
            self.clearButton.show()

    def resizeEvent(self, e):
        """ 改变大小时需要移动按钮的位置 """
        self.clearButton.move(self.width() - self.clearButton.width()-1, 1)

    def eventFilter(self, obj, e):
        """ 清空按钮按下时清空内容并隐藏按钮 """
        if obj == self.clearButton:
            if e.type() == QEvent.MouseButtonRelease and e.button() == Qt.LeftButton:
                self.clear()
                self.clearButton.hide()
                return True
        return super().eventFilter(obj, e)


class LineEditMenu(QMenu):
    """ 单行输入框右击菜单 """

    def __init__(self, parent):
        super().__init__("", parent)
        self.windowEffect = WindowEffect()
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.Popup | Qt.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground | Qt.WA_StyledBackground)
        # 不能直接改width
        self.animation = QPropertyAnimation(self, b"geometry")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutQuad)

    def event(self, e: QEvent):
        if e.type() == QEvent.WinIdChange:
            self.windowEffect.addShadowEffect(self.winId())
        return QMenu.event(self, e)

    def createActions(self):
        # 创建动作
        self.cutAct = QAction(
            QIcon("resource/images/剪切.png"),
            "剪切",
            self,
            shortcut="Ctrl+X",
            triggered=self.parent().cut,
        )
        self.copyAct = QAction(
            QIcon("resource/images/复制.png"),
            "复制",
            self,
            shortcut="Ctrl+C",
            triggered=self.parent().copy,
        )
        self.pasteAct = QAction(
            QIcon("resource/images/粘贴.png"),
            "粘贴",
            self,
            shortcut="Ctrl+V",
            triggered=self.parent().paste,
        )
        self.cancelAct = QAction(
            QIcon("resource/images/撤销.png"),
            "取消操作",
            self,
            shortcut="Ctrl+Z",
            triggered=self.parent().undo,
        )
        self.selectAllAct = QAction(
            "全选", self, shortcut="Ctrl+A", triggered=self.parent().selectAll
        )
        # 创建动作列表
        self.action_list = [
            self.cutAct,
            self.copyAct,
            self.pasteAct,
            self.cancelAct,
            self.selectAllAct,
        ]

    def exec_(self, pos):
        # 删除所有动作
        self.clear()
        # clear之后之前的动作已不再存在故需重新创建
        self.createActions()
        # 初始化属性
        self.setProperty("hasCancelAct", "false")
        width = 176
        actionNum = len(self.action_list)
        # 访问系统剪贴板
        self.clipboard = QApplication.clipboard()
        # 根据剪贴板内容是否为text分两种情况讨论
        if self.clipboard.mimeData().hasText():
            # 再根据3种情况分类讨论
            if self.parent().text():
                self.setProperty("hasCancelAct", "true")
                width = 213
                if self.parent().selectedText():
                    self.addActions(self.action_list)
                else:
                    self.addActions(self.action_list[2:])
                    actionNum -= 2
            else:
                self.addAction(self.pasteAct)
                actionNum = 1
        else:
            if self.parent().text():
                self.setProperty("hasCancelAct", "true")
                width = 213
                if self.parent().selectedText():
                    self.addActions(
                        self.action_list[:2] + self.action_list[3:])
                    actionNum -= 1
                else:
                    self.addActions(self.action_list[3:])
                    actionNum -= 3
            else:
                return
        # 每个item的高度为38px，10为上下的内边距和
        height = actionNum * 38 + 10
        # 不能把初始的宽度设置为0px，不然会报警
        self.animation.setStartValue(QRect(pos.x(), pos.y(), 1, 1))
        self.animation.setEndValue(QRect(pos.x(), pos.y(), width, height))
        self.setStyle(QApplication.style())
        # 开始动画
        self.animation.start()
        super().exec_(pos)
