import sublime

import json
import os

from ..json import encoder
from ..json import decoder

_DEFAULT_PATH = ['User', 'sessions']
_DEFAULT_EXTENSION = 'json'


def dump(name, session):
    session_path = _generate_path(name)
    with open(session_path, 'w') as f:
        json.dump(session, f, cls=encoder.SessionEncoder)


def load(name):
    session_path = _generate_path(name)
    with open(session_path, 'r') as f:
        return json.load(f, cls=decoder.SessionDecoder)


def _generate_path(name, path=_DEFAULT_PATH):
    folder = os.path.join(sublime.packages_path(), *_DEFAULT_PATH)

    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    return os.path.join(folder, _generate_name(name))


def _generate_name(name, extension=_DEFAULT_EXTENSION):
    return '.'.join([name, extension])
