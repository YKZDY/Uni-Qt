from .utils import QtModifier
from PyQt5 import QtWidgets, QtGui


pyqt5_modifier = QtModifier()


@pyqt5_modifier.register("clib.wrapinstance")
def wrapinstance(*args, **kwargs):

    try:
        import sip
    except ImportError:
        raise RuntimeError("This method isn't executable without sip module.")

    return sip.wrapinstance(*args, **kwargs)


@pyqt5_modifier.register("clib.unwrapinstance")
def unwrapinstance(*args, **kwargs):

    try:
        import sip
    except ImportError:
        raise RuntimeError("This method isn't executable without sip module.")

    return sip.unwrapinstance(*args, **kwargs)


@pyqt5_modifier.register("QtWidgets.QTreeWidgetItem.setBackgroundColor")
def setBackgroundColor(self, p_int, QColor):
    QtWidgets.QTreeWidgetItem.setBackground(self, p_int, QColor)


@pyqt5_modifier.register("QtWidgets.QTreeWidgetItem.setTextColor")
def setTextColor(self, p_int, QColor):
    QtWidgets.QTreeWidgetItem.setForeground(self, p_int, QColor)


@pyqt5_modifier.register("QtWidgets.QTableWidgetItem.setBackgroundColor")
def setBackgroundColor(self, QColor):
    QtWidgets.QTableWidgetItem.setBackground(self, QColor)


@pyqt5_modifier.register("QtWidgets.QTableWidgetItem.setTextColor")
def setTextColor(self, QColor):
    QtWidgets.QTableWidgetItem.setForeground(self, QColor)


@pyqt5_modifier.register("QtWidgets.QTreeWidget.setItemHidden")
def setItemHidden(self, QTreeWidgetItem, bool):
    QTreeWidgetItem.setHidden(bool)


@pyqt5_modifier.register("QtGui.QWheelEvent.delta")
def delta(self):
    return QtGui.QWheelEvent.angleDelta(self).y()


@pyqt5_modifier.register("QtGui.QDrag.start")
def start(self, supportedActions=None):
    QtGui.QDrag.exec_(self, supportedActions)
