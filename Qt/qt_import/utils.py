import os
import sys
import imp
import platform


def search_module_dir(name):
    """
    Search the path which contains the following module. Return false if it's unable to find
    """
    try:
        _, path, _ = imp.find_module(name)
    except ImportError:
        return ""
    return os.path.dirname(path)


def seek_module_file(path, name, module_type):
    """
    Return the path of module file in the following path by searching the name
    """
    _binary_suffix_table = {
        "Darwin": "so",
        "Linux": "so",
        "Windows": "pyd"
    }

    if module_type == "dynamic":
        full_name = os.extsep.join([name, _binary_suffix_table[platform.system()]])
        full_path = os.path.join(path, full_name)
        return full_path if os.path.isfile(full_path) else ""

    elif module_type == "source":
        full_path = os.path.join(path, os.extsep.join([name, "py"]))
        if not os.path.isfile(full_path):
            full_path = os.path.join(path, os.extsep.join([name, "pyw"]))
        return full_path if os.path.isfile(full_path) else ""

    elif module_type == "compiled":
        full_name = os.extsep.join([name, "pyc"])
        full_path = os.path.join(path, full_name)
        return full_path if os.path.isfile(full_path) else ""

    elif module_type == "package":
        full_name = name
        full_path = os.path.join(path, full_name)
        return full_path if os.path.isdir(full_path) else ""

    else:
        raise ImportError("Invalid module type: %s" % module_type)


def secure_load_module(name, path, module_type):
    """
    Safely load python module from disk, simply return the catch if it's already exist
    """
    load_function = getattr(imp, "load_%s" % module_type, None)
    if not load_function:
        raise ImportError("Invalid module type: %s" % module_type)

    if name in sys.modules.keys():
        return sys.modules[name]
    else:
        return load_function(name, path)
