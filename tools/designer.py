import qfluentwidgets
import os
from pathlib import Path

print(f"cd { str(Path(__file__).parent.parent) } && export PYSIDE_DESIGNER_PLUGINS=\"./tools\" && pyside6-designer")
os.system(f"cd { str(Path(__file__).parent.parent) } && export PYSIDE_DESIGNER_PLUGINS=\"./tools\" && pyside6-designer")