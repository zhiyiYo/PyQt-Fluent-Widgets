# coding: utf-8
import os
from pathlib import Path

from PySide6.scripts.pyside_tool import designer


def append_to_path_var(var, value):
    env_value = os.environ.get(var)
    if env_value:
        env_value = f'{env_value}{os.pathsep}{value}'
    else:
        env_value = value

    os.environ[var] = env_value


project_dir = Path(__file__).absolute().parent.parent

# set up environment variables
append_to_path_var('PYSIDE_DESIGNER_PLUGINS', str(project_dir / 'plugins'))
append_to_path_var('PYTHONPATH', str(project_dir))


# launch QtDesigner
designer()

