import os
import types
from .utils import seek_module_file, secure_load_module, search_module_dir


def import_pyqt4(path):
    """
    Loading all of the pyqt4 submodules into memory from the input path
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
        "QtXml"
    ]

    # List of submodule packages
    _package_modules = [
        "uic"
    ]

    # Import sip
    sip_file = seek_module_file(path, "sip", "dynamic") or \
               seek_module_file(os.path.join(path, "PyQt4"), "sip", "dynamic") or \
               seek_module_file(search_module_dir("sip"), "sip", "dynamic")
    if sip_file:
        secure_load_module("sip", sip_file, "dynamic")

    # Import Qt namespace
    qt_dir = os.path.join(path, "PyQt4")
    module = secure_load_module("PyQt4", qt_dir, "package")

    # Import Qt submodules
    for submodule in _dynamic_modules:
        setattr(module, submodule,
                secure_load_module("PyQt4." + submodule, seek_module_file(qt_dir, submodule, "dynamic"), "dynamic"))
    for submodule in _package_modules:
        setattr(module, submodule,
                secure_load_module("PyQt4." + submodule, seek_module_file(qt_dir, submodule, "package"), "package"))

    # Update lacking submodules
    setattr(module, "QtWidgets", getattr(module, "QtGui"))
    setattr(module, "clib", types.ModuleType("clib"))

    # Compatible Fix
    module.QtCore.QStringListModel = module.QtGui.QStringListModel
    module.QtCore.QAbstractProxyModel = module.QtGui.QAbstractProxyModel
    module.QtCore.QSortFilterProxyModel = module.QtGui.QSortFilterProxyModel
    module.QtCore.QItemSelection = module.QtGui.QItemSelection
    module.QtCore.QItemSelectionModel = module.QtGui.QItemSelectionModel

    return module
