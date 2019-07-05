import os
import types
from .utils import seek_module_file, secure_load_module, search_module_dir


def import_pyside(path):
    """
    Loading all of the pyside submodules into memory from the input path
    This import function works with path argument rather than search from sys.path
    """
    # List of dynamic submodules
    _dynamic_modules = [
        "QtCore",
        "QtGui",
        "QtNetwork",
        "QtSvg",
        "QtSql",
        "QtTest",
        "QtXml",
        "QtUiTools"
    ]

    # Import shiboken
    shiboken_file = seek_module_file(path, "shiboken", "dynamic") or \
                    seek_module_file(os.path.join(path, "PySide"), "shiboken", "dynamic") or \
                    seek_module_file(search_module_dir("shiboken"), "shiboken", "dynamic")
    if shiboken_file:
        secure_load_module("shiboken", shiboken_file, "dynamic")

    # Import pysideuic
    pysideuic_file = seek_module_file(path, "pysideuic", "package") or \
                     seek_module_file(os.path.join(path, "PySide"), "pysideuic", "package") or \
                     seek_module_file(search_module_dir("pysideuic"), "pysideuic", "package")
    if pysideuic_file:
        secure_load_module("pysideuic", pysideuic_file, "package")

    # Import Qt namespace
    qt_dir = os.path.join(path, "PySide")
    module = secure_load_module("PySide", qt_dir, "package")

    # Import Qt submodules
    for submodule in _dynamic_modules:
        setattr(module, submodule,
                secure_load_module("PySide." + submodule, seek_module_file(qt_dir, submodule, "dynamic"), "dynamic"))

    # Update lacking submodules
    setattr(module, "QtWidgets", getattr(module, "QtGui"))
    setattr(module, "uic", types.ModuleType("uic"))
    setattr(module, "clib", types.ModuleType("clib"))

    # Compatible Fix
    module.QtCore.QStringListModel = module.QtGui.QStringListModel
    module.QtCore.QAbstractProxyModel = module.QtGui.QAbstractProxyModel
    module.QtCore.QSortFilterProxyModel = module.QtGui.QSortFilterProxyModel
    module.QtCore.QItemSelection = module.QtGui.QItemSelection
    module.QtCore.QItemSelectionModel = module.QtGui.QItemSelectionModel

    module.QtCore.pyqtProperty = module.QtCore.Property
    module.QtCore.pyqtSignal = module.QtCore.Signal
    module.QtCore.pyqtSlot = module.QtCore.Slot

    return module
