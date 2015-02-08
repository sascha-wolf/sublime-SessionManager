import sublime
import sublime_plugin

from datetime import datetime

from .modules import messages
from .modules import serialize
from .modules import settings
from .modules.session import Session


def plugin_loaded():
    settings.load()


def error_message(errno):
    sublime.error_message(messages.error(errno))


class SaveSession(sublime_plugin.ApplicationCommand):
    def run(self):
        sublime.active_window().show_input_panel(
            messages.dialog("session_name"),
            self.generate_name(),
            on_done=self.save_session,
            on_change=None,
            on_cancel=None
        )

    def generate_name(self):
        now = datetime.now()
        timestamp = now.strftime(settings.get('session_name_dateformat'))
        return '_'.join(['session', timestamp])

    def save_session(self, session_name):
        session = Session.save(session_name, sublime.windows())
        try:
            serialize.dump(session_name, session)
        except OSError as e:
            error_message(e.errno)

    def is_enabled(self):
        windows = sublime.windows()
        for window in windows:
            if is_saveable(window):
                return True

        return False


def is_saveable(window):
    return bool(window.views()) or bool(window.project_data())
