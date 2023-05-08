# coding: utf-8
from distutils.sysconfig import get_python_lib
import os
import sys
from pathlib import Path

import PyQt5
from PyQt5.QtCore import QProcessEnvironment, QProcess, QLibraryInfo


def get_designer_path():
    """ get the path of qt designer """
    site_packages = get_python_lib()
    ext = '.exe' if os.name == 'nt' else ''
    bins = [
        f"{QLibraryInfo.location(QLibraryInfo.BinariesPath)}/designer{ext}",
        f"{site_packages}/pyqt5_tools/designer{ext}",
        f"{site_packages}/qt5_applications/Qt/bin/designer{ext}",
    ]
    for f in bins:
        if os.path.exists(f):
            return f

    raise Exception("Can't find avalibale QtDesigner")


tools_dir = Path(__file__).absolute().parent
project_dir = tools_dir.parent

# set up environment variables
env = QProcessEnvironment.systemEnvironment()
PATH = f"{os.path.dirname(PyQt5.__file__)};{sys.prefix};{env.value('PATH', '')}"

env.insert('PATH', PATH)
env.insert('PYQTDESIGNERPATH', str(project_dir / 'plugins'))
env.insert('PYTHONPATH', str(project_dir))

# launch QtDesigner
designer = QProcess()
designer.setProcessEnvironment(env)

designer.start(get_designer_path())
designer.waitForFinished(-1)
sys.exit(designer.exitCode())
