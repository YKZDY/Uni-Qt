from .utils import QtModifier


pyqt4_modifier = QtModifier()


@pyqt4_modifier.register("clib.wrapinstance")
def wrapinstance(*args, **kwargs):

    try:
        import sip
    except ImportError:
        raise RuntimeError("This method isn't executable without sip module.")

    return sip.wrapinstance(*args, **kwargs)


@pyqt4_modifier.register("clib.unwrapinstance")
def unwrapinstance(*args, **kwargs):

    try:
        import sip
    except ImportError:
        raise RuntimeError("This method isn't executable without sip module.")

    return sip.unwrapinstance(*args, **kwargs)


@pyqt4_modifier.register("QtCore.QString.__str__")
def to_string(self):
    return str(self.toUtf8())
