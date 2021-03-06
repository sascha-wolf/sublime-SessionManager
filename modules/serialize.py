import sublime

import glob
import json
import os

from ..json import encoder
from ..json import decoder

from . import settings

_DEFAULT_PATH = os.path.join('User', 'sessions')
_DEFAULT_EXTENSION = '.sublime-session'


def is_valid(name):
    session_path = _generate_path(name)
    try:
        open(session_path, 'w').close()
        os.unlink(session_path)
    except OSError:
        return False
    else:
        return True


def dump(name, session):
    session_path = _generate_path(name)
    with open(session_path, 'w') as f:
        json.dump(session, f, cls=encoder.SessionEncoder)


def load(name):
    session_path = _generate_path(name)
    with open(session_path, 'r') as f:
        return json.load(f, cls=decoder.SessionDecoder)


def delete(name):
    session_path = _generate_path(name)
    os.remove(session_path)


def available():
    paths = _available_paths()
    files = [os.path.basename(p) for p in paths]
    # Remove the extension
    names = [f[:-len(_DEFAULT_EXTENSION)] for f in files]

    return names


def _available_paths():
    session_folder = _generate_folder()
    search_pattern = os.path.join(
        session_folder,
        ''.join(['*', _DEFAULT_EXTENSION])
    )

    return glob.glob(search_pattern)


def _generate_path(name):
    return os.path.join(_generate_folder(), _generate_name(name))


def _generate_folder():
    folder = settings.get('session_path')
    if folder:
        folder = os.path.normpath(folder)
    else:
        folder = os.path.join(sublime.packages_path(), _DEFAULT_PATH)

    # Ensure the folder exists
    try:
        os.makedirs(folder, exist_ok=True)
    except FileExistsError:
        # Issue 21082 (http://bugs.python.org/issue21082)
        # Before Python 3.4.1, if exist_ok was True and the directory existed,
        # makedirs() would still raise an error if mode did not match the mode of the existing directory
        pass

    return folder


def _generate_name(name, extension=_DEFAULT_EXTENSION):
    return ''.join([name, extension])
