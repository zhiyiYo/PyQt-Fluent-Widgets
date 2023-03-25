# coding:utf-8
import os
import sys

from PySide6.QtCore import Qt, QLocale, QTranslator
from PySide6.QtWidgets import QApplication

from app.common.config import cfg, Language
from app.view.main_window import MainWindow


# enable dpi scale
if cfg.get(cfg.dpiScale) != "Auto":
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

# create application
app = QApplication(sys.argv)
app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

# internationalization
translator = QTranslator()
galleryTranslator = QTranslator()
language = cfg.get(cfg.language)

if language == Language.AUTO:
    translator.load(QLocale.system(), "app/resource/i18n/qfluentwidgets_")
    galleryTranslator.load(QLocale.system(), "app/resource/i18n/gallery_")
elif language != Language.ENGLISH:
    translator.load(f"app/resource/i18n/qfluentwidgets_{language.value}.qm")
    galleryTranslator.load(f"app/resource/i18n/gallery_{language.value}.qm")

app.installTranslator(translator)
app.installTranslator(galleryTranslator)

# create main window
w = MainWindow()
w.show()

app.exec()