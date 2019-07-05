import os
import sys
import types
import json
import warnings
import platform
from .qt_conf import QT_PREFERRED_BINDING, PYQT4_DIR, PYQT5_DIR, PYSIDE_DIR, PYSIDE2_DIR
from .qt_import import import_pyqt4, import_pyqt5, import_pyside, import_pyside2, search_module_dir
from .qt_modify import pyqt4_modifier, pyqt5_modifier, pyside_modifier, pyside2_modifier


PWD = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(PWD, "qt_member.json"), "r") as f:
    QT_MEMBER = f.readlines()


def byteify(source):
    """
    Convert input variable from unicode to str
    """
    if isinstance(source, dict):
        return {byteify(key): byteify(value) for key, value in source.items()}
    elif isinstance(source, (list, tuple)):
        return [byteify(element) for element in source]
    elif isinstance(source, unicode):
        return source.encode("utf-8")
    else:
        return source


def get_member_linenum(name):
    """
    Get line number of input member from qt_member.json
    """
    for index, line in enumerate(QT_MEMBER):
        if line.strip().strip(",").strip("\"") == name:
            return index + 1


def promote_module(module):
    """
    Enable direct import of submodule
    e.g. import Qt.QtCore
    """
    for submodule in module.__all__:
        sys.modules[".".join([module.__name__, submodule])] = getattr(module, submodule)


def setup(qt):
    """
    Kernel loading processing
    """
    import_table = {
        "pyside": import_pyside,
        "pyside2": import_pyside2,
        "pyqt4": import_pyqt4,
        "pyqt5": import_pyqt5
    }

    path_table = {
        "pyside": PYSIDE_DIR or search_module_dir("PySide"),
        "pyside2": PYSIDE2_DIR or search_module_dir("PySide2"),
        "pyqt4": PYQT4_DIR or search_module_dir("PyQt4"),
        "pyqt5": PYQT5_DIR or search_module_dir("PyQt5")
    }

    modifier_table = {
        "pyside": pyside_modifier,
        "pyside2": pyside2_modifier,
        "pyqt4": pyqt4_modifier,
        "pyqt5": pyqt5_modifier
    }

    binding_order = QT_PREFERRED_BINDING.split(",")
    for each in binding_order:
        if path_table[each]:
            QT_BINDING = each
            break
    else:
        raise ImportError("No python binding for Qt was found.")

    # Loading common members from json
    common_members = json.loads("".join(QT_MEMBER))
    if platform.python_version() < "3":
        common_members = byteify(common_members)

    # Import ordinary qt package to tmp_module
    tmp_qt = import_table[QT_BINDING](path_table[QT_BINDING])

    # Change the ordinary code to Qt grammar by executing particular modification
    modifier_table[QT_BINDING]().modify(tmp_qt)

    # Store empty submodules to qt package
    for name in list(common_members):
        setattr(qt, name, types.ModuleType(name))

    # Set Qt particular attributes
    setattr(qt, "__binding__", QT_BINDING)
    setattr(qt, "__binding_path__", path_table[QT_BINDING])

    # Install to Qt package
    for submodule, members in common_members.items():
        tmp_submodule = getattr(tmp_qt, submodule)
        qt_submodule = getattr(qt, submodule)
        for member in members:
            tmp_member = getattr(tmp_submodule, member, None)
            if not tmp_member:
                warnings.showwarning("Missing {} from {}.".format(member, tmp_submodule.__name__), 
                    RuntimeWarning, "qt_member", get_member_linenum(member))
            else:
                setattr(qt_submodule, member, tmp_member)

    # Enable from Qt import *
    setattr(qt, "__all__", list(common_members))

    # Enable direct import of submodule
    promote_module(qt)