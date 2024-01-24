# ------------------------------------------------------------
# --- PYTHON UTILS ---
# Description   = Useful python scrits
#
# Date   = 2024 - 01 - 23
# Author = Juls
# Email  = segretovfx@gmail.com
#
# Usage = import the modules
# ------------------------------------------------------------

import os
import sys
import importlib


def unload_module(pkg, *Args):
    """unload imported package/modules.

    Args:
        pkg (str): Name of the package to unload
    """

    pkg_dir = os.path.abspath(os.path.dirname(pkg.__file__))

    def _is_part_of_pkg(module_):
        module_path = getattr(module_, "__file__", os.sep)
        module_dir = os.path.abspath(os.path.dirname(module_path))

        return module_dir.startswith(pkg_dir)

    to_unload = [
        name for name, module in sys.modules.items() if _is_part_of_pkg(module)
    ]

    for name in to_unload:
        sys.modules.pop(name)


def import_module(pkg, pkg_path=None, *Args):
    if pkg_path is None:
        pass
        # importlib.import_module(f"{pkg}")
        # importlib.reload(f"{pkg}")
    else:
        importlib.import_module(f"{pkg_path}.{pkg}")
        importlib.reload(f"{pkg_path}.{pkg}")
