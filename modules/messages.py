from os import strerror

messages = {
    "dialog": {
        "session_name": "Enter session name:"
    },
    "message": {
        "no_sessions": "No sessions available.",
        "deleted": "Deleted session '{}'."
    },
    "error": {
        "default": "Unknown error!"
    }
}


def get(group, key, *args):
    return str.format(messages[group][key], *args)


def error(error_key, *args):
    if isinstance(error_key, int):
        msg = _errno(error_key)
    elif isinstance(error_key, str):
        msg = _error(error_key)

    return str.format(msg, *args)


def _errno(error_code):
    try:
        msg = strerror(error_code)
    except ValueError:
        msg = messages["error"]["default"]

    return str.format(msg + " (errno: {})", error_code)


def _error(error_key):
    try:
        msg = messages["error"][error_key]
    except KeyError:
        msg = messages["error"]["default"]

    return msg


def dialog(key, *args):
    return get("dialog", key, *args)


def message(key, *args):
    return get("message", key, *args)
