from os import strerror as _strerror
from sys import platform as _platform

_DEFAULT = "base"
_DIALOG = "dialog"
_GENERAL = "general"
_ERROR = "error"

_messages = {
    _DEFAULT: {
        _DIALOG: {
            "session_name": "Enter session name:"
        },
        _GENERAL: {
            "no_sessions": "No sessions available.",
            "deleted": "Deleted session '{}'."
        },
        _ERROR: {
            "invalid_name": "Invalid name \"{}\"!",
            "default": "Unknown error!"
        }
    },
    "win32": {
        _ERROR: {
            "invalid_name": "Invalid name \"{}\"!\n\nForbidden characters: / ? < > \ : * | \"",
        }
    }
}


def get(group, key, *args):
    try:
        msg = _messages[_platform][group][key]
    except KeyError:
        msg = _messages[_DEFAULT][group][key]

    return str.format(msg, *args)


def error(error_key, *args):
    if isinstance(error_key, int):
        msg = _errno(error_key, args)
    elif isinstance(error_key, str):
        msg = _error(error_key, args)

    return msg


def _errno(error_code, args):
    try:
        msg = _strerror(error_code)
    except ValueError:
        msg = get(_ERROR, "default", *args)

    return str.format(msg + " (errno: {})", error_code)


def _error(error_key, args):
    try:
        msg = get(_ERROR, error_key, *args)
    except KeyError:
        msg = get(_ERROR, "default", *args)

    return msg


def dialog(key, *args):
    return get(_DIALOG, key, *args)


def message(key, *args):
    return get(_GENERAL, key, *args)
