import sublime
import sublime_plugin

from datetime import datetime

from .modules import messages
from .modules import serialize
from .modules import settings
from .modules.session import Session


def plugin_loaded():
    settings.load()


def error_message(error_key, *args):
    sublime.error_message(messages.error(error_key, *args))


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
        nameformat = settings.get('session_name_dateformat')
        return datetime.now().strftime(nameformat)

    def save_session(self, session_name):
        if not serialize.is_valid(session_name):
            error_message("invalid_name", session_name)
            return

        session = Session.save(session_name, sublime.windows())
        try:
            serialize.dump(session_name, session)
        except OSError as e:
            error_message(e.errno)

    def is_enabled(self):
        windows = sublime.windows()
        for window in windows:
            if self.is_saveable(window):
                return True

        return False

    @staticmethod
    def is_saveable(window):
        return bool(window.views()) or bool(window.project_data())


class ListSessionCommand:
    def run(self):
        self.session_names = serialize.available()
        if not self.session_names:
            sublime.message_dialog(messages.message("no_sessions"))
            return

        sublime.active_window().show_quick_panel(
            self.session_names,
            self._handle_selection
        )

    def _handle_selection(self, selected_index):
        if selected_index < 0:
            return

        self.handle_session(self.session_names[selected_index])


class LoadSession(ListSessionCommand, sublime_plugin.ApplicationCommand):
    def handle_session(self, session_name):
        try:
            session = serialize.load(session_name)
        except OSError as e:
            error_message(e.errno)
        else:
            session.load()


class DeleteSession(ListSessionCommand, sublime_plugin.ApplicationCommand):
    def handle_session(self, session_name):
        try:
            serialize.delete(session_name)
        except OSError as e:
            error_message(e.errno)
        else:
            sublime.status_message(messages.message("deleted", session_name))
