# coding: utf-8
from distutils.sysconfig import get_python_lib
import os
import sys
import shutil
import warnings

from pathlib import Path

import PyQt6
from PyQt6.QtCore import QProcessEnvironment, QProcess


def get_designer_path():
    """ get the path of qt designer """
    site_packages = get_python_lib()

    if sys.platform == "win32":
        designer_name = "designer.exe"
    elif sys.platform == "darwin":
        designer_name = "designer.app"
    else:
        designer_name = "designer"

    path = Path(f"{site_packages}/qt6_applications/Qt/bin/{designer_name}")
    if not path.exists():
        raise Exception(
            "Can't find available QtDesigner for current environment. You can try `pyqt6-plugins` to solve this problem.")

    # check pyqt6 dll
    if sys.platform == "win32":
        dll_name = "pyqt6.dll"
    elif sys.platform == "darwin":
        dll_name = "libpyqt6.dylib"
    else:
        dll_name = "libpyqt6.so"

    dll_path = Path(f"{site_packages}/qt6_applications/Qt/plugins/designer/{dll_name}")
    if dll_path.exists():
        return str(path)

    plugin_dll_path = Path(f"{site_packages}/pyqt6_plugins/Qt/plugins/designer/{dll_name}")
    if not plugin_dll_path.exists():
        warnings.warn(f"Can't find avaliable {dll_name}, which may cause PyQt-Fluent-Widgets not being visible in QtDesigner.")
        return str(path)

    # copy pyqt6 dll
    dll_path.parent.mkdir(exist_ok=True, parents=True)
    shutil.copy(plugin_dll_path, dll_path)
    print(f'Copy {plugin_dll_path} to {dll_path}.')
    return str(path)


tools_dir = Path(__file__).absolute().parent
project_dir = tools_dir.parent

# set up environment variables
env = QProcessEnvironment.systemEnvironment()
PATH = f"{os.path.dirname(PyQt6.__file__)};{sys.prefix};{env.value('PATH', '')}"

env.insert('PATH', PATH)
env.insert('PYQTDESIGNERPATH', str(project_dir / 'plugins'))
env.insert('PYTHONPATH', str(project_dir))

if sys.platform == "darwin":
    env.insert('DYLD_LIBRARY_PATH', get_python_lib() + "/../..")

# launch QtDesigner
designer = QProcess()
designer.setProcessEnvironment(env)

designer.start(get_designer_path(), [])
designer.waitForFinished(-1)
sys.exit(designer.exitCode())
