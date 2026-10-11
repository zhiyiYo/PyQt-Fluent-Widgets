# coding:utf-8
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout

from qfluentwidgets import ListPicker


class Demo(QWidget):

    def __init__(self):
        super().__init__()
        self.vBoxLayout = QVBoxLayout(self)

        # pick value from a list of texts
        picker1 = ListPicker(items=['柠檬', '西瓜', '苹果', '葡萄', '樱桃'])
        picker1.valueChanged.connect(print)

        # pick value from a list of (value, text) tuples
        picker2 = ListPicker(
            items=[(1, '柠檬'), (2, '西瓜'), (3, '苹果'), (4, '葡萄'), (5, '樱桃')],
            placeholder='选择一个数字',
        )
        picker2.valueChanged.connect(print)

        # adjust the width of panel to its contents
        picker3 = ListPicker(
            items=[
                '一个比较长的选项文本',
                '一个特别特别特别长的选项文本',
                '短选项',
            ],
            widthMode=ListPicker.ADJUST_TO_CONTENTS,
        )
        picker3.valueChanged.connect(print)

        # the button text is elided when it is wider than the button
        picker4 = ListPicker(
            items=['一个特别特别特别长的选项文本', '另一个也很长很长的选项文本'],
            placeholder='选择一段文本',
        )
        picker4.valueChanged.connect(print)

        self.vBoxLayout.addWidget(picker1, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(picker2, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(picker3, 0, Qt.AlignCenter)
        self.vBoxLayout.addWidget(picker4, 0, Qt.AlignCenter)
        self.resize(500, 500)
        self.setStyleSheet('Demo{background: white}')

        # picker1.setValue('西瓜')
        # picker1.valueChanged.disconnect()
        # picker1.setPickerWidth(200)
        # picker1.reset()


if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    w = Demo()
    w.show()
    app.exec_()
