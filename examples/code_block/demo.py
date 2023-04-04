# coding:utf-8
import sys
import PySide6
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QTextBrowser,
    QVBoxLayout
)
from PySide6.QtGui import QAction,QTextCharFormat,QSyntaxHighlighter,QFont
from PySide6.QtCore import Qt,QRegularExpression
from qfluentwidgets import SmoothScroll, setStyleSheet, SwitchButton
from qfluentwidgets.components import RoundMenu
from qfluentwidgets.common.icon import FluentIcon as FIF
import inspect
import keyword
from typing import *

class PythonHightlighter(QSyntaxHighlighter):
    def __init__(self,*args,**kwds):
        super().__init__(*args,**kwds)
    def highlightBlock(self, text):
        baseFormat = QTextCharFormat()
        baseFormat.setForeground(Qt.GlobalColor.darkMagenta)
        keywordFormat = QTextCharFormat()
        keywordFormat.setFontItalic(True)
        keywordFormat.setForeground(Qt.GlobalColor.red)
        commentFormat = QTextCharFormat()
        commentFormat.setForeground(Qt.GlobalColor.gray)
        keywordFormat.setFontItalic(True)
        wordExp = QRegularExpression("\\b[A-Za-z_]+\\b")
        commentExp = QRegularExpression("\#.*")
        wordMatchs = wordExp.globalMatch(text)
        while wordMatchs.hasNext():
            match = wordMatchs.next()
            snippet=match.capturedView()
            if keyword.iskeyword(snippet):
                self.setFormat(match.capturedStart(), match.capturedLength(), keywordFormat)
            else:
                self.setFormat(match.capturedStart(), match.capturedLength(), baseFormat)
        commentMatchs = commentExp.globalMatch(text)
        while commentMatchs.hasNext():
            match = commentMatchs.next()
            snippet=match.capturedView()
            self.setFormat(match.capturedStart(), match.capturedLength(), commentFormat)

class TextCopyMenu(RoundMenu):
    """Only copy menu"""

    def __init__(self, parent: QTextBrowser):
        super().__init__(parent=parent)

    def createActions(self):
        self.copyAct = QAction(
            FIF.COPY.icon(),
            self.tr("Copy"),
            self,
            shortcut="Ctrl+C",
            triggered=self.copyAll,
        )

    def exec(self, pos, ani=True):
        self.clear()
        self.createActions()
        self.addAction(self.copyAct)

        super().exec(pos, ani)

    def copyAll(self):
        parent: QTextBrowser = self.parent()
        parent.selectAll()
        parent.copy()


class CodeBlock(QTextBrowser):
    """Show code block in a pretty way"""

    def __init__(
        self, parent=None, class_names:List[Callable]=None, minShowHeight=25, maxShowHeight=500
    ):
        super().__init__(parent=parent)
        self.verticalSmoothScroll = SmoothScroll(self, Qt.Vertical)
        self.horizonSmoothScroll = SmoothScroll(self, Qt.Horizontal)
        setStyleSheet(self, "line_edit")
        # set code
        self.setFont(QFont("Hack",10))
        self.highlighter=PythonHightlighter(self)
        if class_names is not None:
            self.setCodeName(class_names=class_names)
        # changable ui
        self.__minShowHeight = minShowHeight
        self.__maxShowHeight = maxShowHeight
        self.setFixedHeight(self.__minShowHeight)
        self.__dropButton = SwitchButton(parent=self)
        self.__dropButton.setText(None)
        self.__dropButton.checkedChanged.connect(self.__drop)

    def resizeEvent(self, e: PySide6.QtGui.QResizeEvent) -> None:
        self.__dropButton.move(self.width() - self.__dropButton.width(), 0)
        return super().resizeEvent(e)

    def contextMenuEvent(self, e):
        menu = TextCopyMenu(self)
        menu.exec_(e.globalPos())

    def wheelEvent(self, e):
        if e.modifiers() == Qt.NoModifier:
            self.verticalSmoothScroll.wheelEvent(e)
        else:
            self.horizonSmoothScroll.wheelEvent(e)

    def setCodeName(self, class_names):
        code = '\n'.join([inspect.getsource(name) for name in class_names])
        self.setMarkdown("```python\n{}```".format(code))

    def __drop(self, isChecked: bool):
        self.setFixedHeight(self.__maxShowHeight if isChecked else self.__minShowHeight)

    def setMinShowHeight(self, height: float):
        self.__minShowHeight = height

    def setMaxShowHeight(self, height: float):
        self.__maxShowHeight = height


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.codeblock = CodeBlock(self, [CodeBlock])
        self.highlighter=PythonHightlighter(self.codeblock.document())
        _layout = QVBoxLayout()
        _layout.addWidget(self.codeblock)
        self.setLayout(_layout)
        self.resize(700, 600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
