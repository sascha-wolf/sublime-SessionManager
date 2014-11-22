import sublime

_settings_file = "SessionManager.sublime-settings"
_subl_settings = {}
_default_settings = {
    "session_path": ""
}


def load():
    global _subl_settings

    _subl_settings = sublime.load_settings(_settings_file)


def get(key):
    return _subl_settings.get(key, _default_settings[key])
