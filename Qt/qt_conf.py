import os


# Parsing QT_PREFERRED_BINDING environment.
QT_PREFERRED_BINDING = os.getenv("QT_PREFERRED_BINDING") or "pyside,pyside2,pyqt4,pyqt5"
QT_PREFERRED_BINDING = QT_PREFERRED_BINDING.lower()
for each in QT_PREFERRED_BINDING.split(","):
    if each not in {"pyqt5", "pyside2", "pyqt4", "pyside"}:
        raise EnvironmentError("Invalid QT_PREFERRED_BINDING env: %s" % QT_PREFERRED_BINDING)

# Parsing PYQT4_DIR environment.
PYQT4_DIR = os.getenv("PYQT4_DIR")

# Parsing PYQT5_DIR environment.
PYQT5_DIR = os.getenv("PYQT5_DIR")

# Parsing PYSIDE_DIR environment.
PYSIDE_DIR = os.getenv("PYSIDE_DIR")

# Parsing PYSIDE2_DIR environment.
PYSIDE2_DIR = os.getenv("PYSIDE2_DIR")
