from os import strerror

messages = {
    "dialog": {
        "session_name": "Enter session name:"
    },
    "error": {
        "default": "Unknown error!"
    }
}


def get(group, key, *args):
    return str.format(messages[group][key], *args)


def error(error_code):
    try:
        msg = strerror(error_code)
    except ValueError:
        msg = _error(error_code)

    return str.format(msg + " (errno: {})", error_code)


def _error(error_code):
    if error_code in messages["error"]:
        msg = messages["error"][error_code]
    else:
        msg = messages["error"]["default"]

    return msg


def dialog(key, *args):
    return get("dialog", key, *args)
