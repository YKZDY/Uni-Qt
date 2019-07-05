import os
import types
from .utils import seek_module_file, secure_load_module, search_module_dir


def import_pyside2(path):
    """
    Loading all of the pyside2 submodules into memory from the input path
    This import function works with path argument rather than search from sys.path
    """
    # List of dynamic submodules
    _dynamic_modules = [
        "QtCore",
        "QtGui",
        "QtWidgets",
        "QtNetwork",
        "QtSvg",
        "QtSql",
        "QtTest",
        "QtXml",
        "QtUiTools"
    ]

    # Import shiboken2
    shiboken2_file = seek_module_file(path, "shiboken2", "dynamic") or \
                     seek_module_file(os.path.join(path, "PySide2"), "shiboken2", "dynamic") or \
                     seek_module_file(search_module_dir("shiboken2"), "shiboken2", "dynamic")
    if shiboken2_file:
        secure_load_module("shiboken2", shiboken2_file, "dynamic")

    # Import pyside2uic
    pyside2uic_file = seek_module_file(path, "pyside2uic", "package") or \
                      seek_module_file(os.path.join(path, "PySide2"), "pyside2uic", "package") or \
                      seek_module_file(search_module_dir("pyside2uic"), "pyside2uic", "package")
    if pyside2uic_file:
        secure_load_module("pyside2uic", pyside2uic_file, "package")

    # Import Qt namespace
    qt_dir = os.path.join(path, "PySide2")
    module = secure_load_module("PySide2", qt_dir, "package")

    # Import Qt submodules
    for submodule in _dynamic_modules:
        setattr(module, submodule,
                secure_load_module("PySide2." + submodule, seek_module_file(qt_dir, submodule, "dynamic"), "dynamic"))

    # Update lacking submodules
    setattr(module, "uic", types.ModuleType("uic"))
    setattr(module, "clib", types.ModuleType("clib"))

    # Compatible Fix
    module.QtCore.QStringListModel = module.QtGui.QStringListModel

    module.QtCore.pyqtProperty = module.QtCore.Property
    module.QtCore.pyqtSignal = module.QtCore.Signal
    module.QtCore.pyqtSlot = module.QtCore.Slot

    return module
