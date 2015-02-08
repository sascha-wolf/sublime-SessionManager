import sublime

import json
import os

from ..json import encoder
from ..json import decoder

from . import settings

_DEFAULT_PATH = os.path.join('User', 'sessions')
_DEFAULT_EXTENSION = '.sublime-session'


def dump(name, session):
    session_path = _generate_path(name)
    with open(session_path, 'w') as f:
        json.dump(session, f, cls=encoder.SessionEncoder)


def load(name):
    session_path = _generate_path(name)
    with open(session_path, 'r') as f:
        return json.load(f, cls=decoder.SessionDecoder)


def _generate_path(name):
    return os.path.join(_generate_folder(), _generate_name(name))


def _generate_folder():
    folder = settings.get('session_path')
    if folder:
        folder = os.path.normpath(folder)
    else:
        folder = os.path.join(sublime.packages_path(), _DEFAULT_PATH)

    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    return folder


def _generate_name(name, extension=_DEFAULT_EXTENSION):
    return ''.join([name, extension])
