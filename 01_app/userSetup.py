""" Import shelf modules """

import os
import sys

PATH = "./scripts"
PYTHON_PATH = f'{PATH}/py'
MEL_PATH = f'{PATH}/mel'
ICONS_PATH = f'{PATH}/icons'

ICONS_ENV = 'XBMLANGPATH'
MEL_ENV = 'MAYA_SCRIPT_PATH'

path_list = [PATH, PYTHON_PATH, MEL_PATH, ICONS_PATH]

def _path_exists(path):
    """
    Check if file path exists in the folder hierarchy.
    :param path: Path to the custom scripts.
    :return: True if file exists.
    """
    if os.path.exists(path):
        return True
    return False


def _path_in_sys(path):
    """
    Check if path is already in system variable list.
    :param path: Path to the custom scripts.
    :return: True if path already exists in sys.
    """
    if path in sys.path:
        return True
    return False


def _path_in_env(path, env):
    """
    Check if path is already in environ variable list.
    :param path: Path to the custom scripts.
    :param env: Inside which environment do you want to check.
    :return: True if path already exists in env.
    """
    if path in os.environ.get(env):
        return True
    return False


def _path_sys_insert(path):
    """
    insert the path into the system variable list.
    :param path: Path to the custom scripts.
    :return: None.
    """
    if not _path_in_sys(path):
        sys.path.insert(0, path)
        print(f'path insert : {path}')

def _path_env_insert(path, env):
    """
    insert the path into the environment variable list.
    :param path: Path to the custom scripts.
    :return: None.
    """
    if not _path_in_env(path, env):
        os.environ[env] += ";" + (str(path))
        print(f'path insert : {path}')


# check if path exists
for path in path_list:
    if not _path_exists(path):
        raise RuntimeError(f"Target folder doesn't exist :"
                           f" {PATH}")

# add path to sys and env
_path_sys_insert(PATH)

_path_env_insert(ICONS_PATH, ICONS_ENV)

_path_env_insert(MEL_PATH, MEL_ENV)

# import shelves.shelf
# import pyutils.pyutil
#
# pyutils.pyutil.unload(shelves)

# import my_package.module
# my_package.module.main()

# importlib.reload(test_shelf)
# shelves.shelf.AnimShelf
print("Shelf loaded")
