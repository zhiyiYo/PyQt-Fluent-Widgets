Quick start
-----------

Install
~~~~~~~

To install lite version (``AcrylicLabel`` is not available) use pip:

.. code:: shell

   pip install PyQt-Fluent-Widgets -i https://pypi.org/simple/

Or install full-featured version use pip:

.. code:: shell

   pip install "PyQt-Fluent-Widgets[full]" -i https://pypi.org/simple/

If you are using PySide2, PySide6 or PyQt6, you can download the code in `PySide2 <https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/PySide2>`__, `PySide6 <https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/PySide6>`__ or `PyQt6 <https://github.com/zhiyiYo/PyQt-Fluent-Widgets/tree/PyQt6>`__ branch.

.. warning:: Don't install PyQt-Fluent-Widgets, PyQt6-Fluent-Widgets, PySide2-Fluent-Widgets and PySide6-Fluent-Widgets at the same time, because their package names are all ``qfluentwidgets``.

Run example
~~~~~~~~~~~

After installing PyQt-Fluent-Widgets package using pip, you can run any
demo in the examples directory, for example:

.. code:: python

   cd examples/gallery
   python demo.py

.. note:: If you encounter ``ImportError: cannot import name 'XXX' from 'qfluentwidgets'``, it indicates that the package version you installed is too low. You can replace the mirror source with https://pypi.org/simple and reinstall again.
