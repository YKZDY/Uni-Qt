# Copyright (c) 2017 Calven Gu <cz069069@outlook.com>
# Licence: LGPL3
# Visit https://github.com/YKZDY/Uni-Qt for more details.

import sys
from .qt_base import setup


setup(sys.modules[__name__])

# Support for PyCharm auto-complete. Crazy PyCharm people!!!
if False:
    from PyQt4 import QtCore, QtGui, QtOpenGL, QtNetwork, QtSvg, uic
    QtWidgets = QtGui
    from PyQt5 import QtCore, QtGui, QtWidgets, QtOpenGL, QtNetwork, QtSvg, uic
