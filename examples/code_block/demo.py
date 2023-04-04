# coding:utf-8
import sys

from PySide6.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from qfluentwidgets import SmoothScroll, setStyleSheet
from qfluentwidgets.components import RoundMenu
from qfluentwidgets.common.icon import FluentIcon as FIF
import inspect
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter


class TextCopyMenu(RoundMenu):
    """Only copy menu"""
    def __init__(self, parent: QTextEdit):
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
        parent: QTextEdit = self.parent()
        parent.selectAll()
        parent.copy()


class CodeBlock(QTextEdit):
    """ Show code block in a pretty way """
    def __init__(self, parent=None, class_name=None):
        super().__init__(parent=parent)
        self.verticalSmoothScroll = SmoothScroll(self, Qt.Vertical)
        self.horizonSmoothScroll = SmoothScroll(self, Qt.Horizontal)
        setStyleSheet(self, "line_edit")
        self.setReadOnly(True)
        self.lexer = PythonLexer()
        self.formatter = HtmlFormatter(style="xcode")
        self.template = '<!DOCTYPE html>\
            <html lang="en">\
            <head>\
                <meta charset="UTF-8">\
                <meta http-equiv="X-UA-Compatible" content="IE=edge">\
                <meta name="viewport" content="width=device-width, initial-scale=1.0">\
                <style>{}</style>\
            </head>\
            <body>{}</body>\
            </html>'
        if callable(class_name):
            self.setCodeName(class_name=class_name)

    def contextMenuEvent(self, e):
        menu = TextCopyMenu(self)
        menu.exec_(e.globalPos())

    def wheelEvent(self, e):
        if e.modifiers() == Qt.NoModifier:
            self.verticalSmoothScroll.wheelEvent(e)
        else:
            self.horizonSmoothScroll.wheelEvent(e)

    def setCodeName(self, class_name):
        code = inspect.getsource(class_name)
        code = highlight(code, lexer=self.lexer, formatter=self.formatter)
        css = self.formatter.get_style_defs(".highlight")
        pretty = self.template.format(css, code)
        self.setText(pretty)


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.codeblock = CodeBlock(self,CodeBlock)
        _layout = QVBoxLayout()
        _layout.addWidget(self.codeblock)
        self.setLayout(_layout)
        self.resize(700,600)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec()
