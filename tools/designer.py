# coding: utf-8
from distutils.sysconfig import get_python_lib
import os
import sys
import shutil
import warnings

from pathlib import Path

import PyQt5
from PyQt5.QtCore import QProcessEnvironment, QProcess, QLibraryInfo


def get_designer_path():
    """ get the path of qt designer """
    site_packages = get_python_lib()

    if sys.platform == "win32":
        designer_name = "designer.exe"
    elif sys.platform == "darwin":
        designer_name = "designer.app"
    else:
        designer_name = "designer"

    path = Path(f"{site_packages}/qt5_applications/Qt/bin/{designer_name}")
    if not path.exists():
        raise Exception(
            "Can't find available QtDesigner for current environment. You can try `pip install pyqt5-tools` to solve this problem.")

    # check pyqt5 dll
    if sys.platform == "win32":
        dll_name = "pyqt5.dll"
    elif sys.platform == "darwin":
        dll_name = "libpyqt5.dylib"
    else:
        dll_name = "libpyqt5.so"

    dll_path = Path(f"{site_packages}/qt5_applications/Qt/plugins/designer/{dll_name}")
    if dll_path.exists():
        return str(path)

    plugin_dll_path = Path(f"{site_packages}/pyqt5_plugins/Qt/plugins/designer/{dll_name}")
    if not plugin_dll_path.exists():
        warnings.warn(f"Can't find avaliable {dll_name}, which may cause PyQt-Fluent-Widgets not being visible in QtDesigner.")
        return str(path)

    # copy pyqt5 dll
    dll_path.parent.mkdir(exist_ok=True, parents=True)
    shutil.copy(plugin_dll_path, dll_path)
    print(f'Copy {plugin_dll_path} to {dll_path}.')
    return str(path)


tools_dir = Path(__file__).absolute().parent
project_dir = tools_dir.parent

# set up environment variables
env = QProcessEnvironment.systemEnvironment()
PATH = f"{os.path.dirname(PyQt5.__file__)};{sys.prefix};{env.value('PATH', '')}"

env.insert('PATH', PATH)
env.insert('PYQTDESIGNERPATH', str(project_dir / 'plugins'))
env.insert('PYTHONPATH', str(project_dir))

if sys.platform == "darwin":
    env.insert('DYLD_LIBRARY_PATH', get_python_lib() + "/../..")

args = []
for arg in sys.argv:
    if arg.endswith("ui"):
        args.append(arg)

# launch QtDesigner
designer = QProcess()
designer.setProcessEnvironment(env)
# add the arguments to allow .ui files to be opened directly without dragging and dropping in designer
designer.start(get_designer_path(), args)
designer.waitForFinished(-1)
sys.exit(designer.exitCode())
