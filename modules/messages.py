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
    msg = None
    if error_code in messages["error"]:
        msg = messages["error"][error_code]
    else:
        msg = messages["error"]["default"]

    return str.format(msg + " ({})", error_code)


def dialog(key, *args):
    return get("dialog", key, *args)
