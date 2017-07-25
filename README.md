# Uni-Qt

Uni-Qt is a wrapper for PyQt4, PyQt5, PySide, PySide2 which supports PyQt5 code format to run properly in all these four kinds of environments. Uni-Qt has been used by [Base FX](http://www.base-fx.com) in feature films such as *Monster Hunt 2*, *Wish Dragon* and helps the team to construct a universal production pipeline.

### Goals

The Uni-Qt codes was inspired by [Qt.py](https://github.com/mottosso/Qt.py). But unlike the Qt.py, Uni-Qt provides flexible interfaces to make it fit different production environments. And it also cares about some relative packages include sip, shiboken, pysideuic, pyqt4topyqt5 and pyuic which will be explained below. So it's much more suitable for large scale VFX production environments.

User can directly use the default Uni-Qt or make some custom modifications by using the handily interface. I'm glad if anybody wants to push your own modifications here.

### References

- [Qt.py](https://github.com/mottosso/Qt.py)
- [pyqt4topyqt5](https://github.com/rferrazz/pyqt4topyqt5)
- [pysideuic](https://github.com/bpabel/pysideuic)
- [pyside-uicfix](https://github.com/jerch/pyside-uicfix)

All the codes of these references have been included in Uni-Qt package with some secondary developments. So generally, you don't need an additional download.

### Usage

The default Uni-Qt is a subset of PyQt5 with a custom submodule called 'clib' which is a wrapper for sip/shiboken/shiboken2. You can use it by simply expanding Uni-Qt 'lib' directory to your PYTHONPATH.

Besides, it keeps a few old features from PyQt4 to strengthen backward compatibility, such as 'setBackgroundColor', 'setTextColor' and 'setItemHidden'. These methods have been removed in original PyQt5 package. But in consideration of the codes are translated from PyQt4 in most of businesses, it's acceptable and helpful to temporarily keep them in our codes. If you want to add more, please read the documentations below.

    import sys
    from Qt import QtWidgets
    
    app = QtWidgets.QApplication(sys.argv)
    button = QtWidgets.QPushButton("Hello World")
    button.show()
    app.exec_()

There are also two utilities in Uni-Qt 'bin' folder. 'pyqt4toqt' is a secondary developed [pyqt4topyqt5](https://github.com/rferrazz/pyqt4topyqt5) tool. It uses 'Qt' or user's input as the name of Qt library in generating codes rather than the rigid 'PyQt5'.

And the 'pyuic' is a wrapper of pyuic4 and pyuic5, it can automatically choose the same binding with Uni-Qt then translate the generating codes to fit Uni-Qt syntax. 

### Documentations

##### Attributes

| Attribute            | Returns   | Description
|:---------------------|:----------|:------------
| `__binding__`        | `str`     | The name of the current binding.
| `__binding_path__`   | `str`     | The path of the current binding's package.

##### Environment Variables

You can change the variables' name or the default value of QT_PREFERRED_BINDING by editing the qt_conf script.

| Variable        | Type   | Description
|:----------------|:-------|:------------
| `QT_PREFERRED_BINDING`    | `str`  | Set the order of bindings, must be a comma separated list of pyqt4, pyqt5, pyside, pyside2.
| `PYQT4_DIR`     | `str`  | Set the pyqt4 installation path. By default, Uni-Qt will search it in sys.path.
| `PYQT5_DIR`     | `str`  | Set the pyqt5 installation path. By default, Uni-Qt will search it in sys.path.
| `PYSIDE_DIR`    | `str`  | Set the pyside installation path. By default, Uni-Qt will search it in sys.path.
| `PYSIDE2_DIR`   | `str`  | Set the pyside2 installation path. By default, Uni-Qt will search it in sys.path.

##### qt_member

It's a json file which contains all the submodules and members of Uni-Qt. If you want to use any members which missed in default Uni-Qt, please add them here.

##### qt_modify

Uni-Qt design the qt_modify to unify the differences between all four kinds of python bindings for the Qt.

For instance, there is a method called 'setTextColor' in PyQt4.QtGui.QTreeWidgetItem which is disappeared in PyQt5. It leads a big trouble after we translate our codes from PyQt4 to PyQt5 even though we can find another way to implement it in PyQt5.

For this reason, Uni-Qt provides a way to keep this method in all kinds of bindings, here is the example:

	from PyQt5 import QtWidgets	
		
	@pyqt5_modifier.register("QtWidgets.QTreeWidgetItem.setTextColor")
	def setTextColor(self, p_int, QColor):
    	QtWidgets.QTreeWidgetItem.setForeground(self, p_int, QColor)

Each time you add a member by changing the qt_member, you should make sure this new member can work properly in all bindings by editing the qt_modify.

You are welcomed to further implement the qt_modify and I will really appreciate your generous commitments. I believe that if we work together to improve this package, more people will be benefited from it. It is my faith on the community and the main intention of publishing this package.

##### Maintainer

- Calven Gu [cz069069@outlook.com](mailto:cz069069@outlook.com)

##### Credits

- Alok Gandhi
- Ramin Kamal
- Cheng Chen
- Wei Liu

##### License

GNU Lesser General Public License v3.0
