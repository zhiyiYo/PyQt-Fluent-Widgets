# coding:utf-8
from PyQt5.QtGui import QColor
from qfluentwidgets.components.widgets.label import AcrylicLabel
from qfluentwidgets import FluentIcon as FIF

from .gallery_interface import GalleryInterface
from ..common.translator import Translator


class MaterialInterface(GalleryInterface):
    """ Material interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.menus,
            subtitle='qfluentwidgets.components.widgets',
            parent=parent
        )

        label = AcrylicLabel(15, QColor(105, 114, 168, 102))
        label.setImage('app/resource/images/chidanta.jpg')
        label.setMaximumSize(787, 579)
        label.setMinimumSize(197, 145)
        self.addExampleCard(
            self.tr('Acrylic label'),
            label,
            'https://github.com/zhiyiYo/PyQt-Fluent-Widgets/blob/master/examples/acrylic_label/demo.py',
            stretch=1
        )
