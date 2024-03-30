from PySide6.QtDesigner import QPyDesignerCustomWidgetCollection
import os

plugins = []

def get_modules(py):
    # I don't know why, but they are nessary
    from PySide6.QtDesigner import QDesignerCustomWidgetInterface
    import inspect

    modules = []
    for name, obj in inspect.getmembers(py, inspect.isclass):
        if name.endswith('Plugin'):
            obj = obj()
            # print(name, isinstance(obj, QDesignerCustomWidgetInterface))
            if isinstance(obj, QDesignerCustomWidgetInterface):
                print(f"Loading {name}")
                modules.append(obj)
    return modules

for filename in os.listdir('.'):
    if filename.endswith('.py') and not filename.startswith('_'):
        # print(filename)
        # plugins += get_modules(__import__(f"{filename}".replace('.py', '')))

        py = __import__(f"{filename}".replace('.py', ''))
        for plug in get_modules(py):
            QPyDesignerCustomWidgetCollection.addCustomWidget(plug)