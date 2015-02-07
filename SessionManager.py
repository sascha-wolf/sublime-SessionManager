import sublime
import sublime_plugin

from .modules import messages


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
        return "placeholder"

    def save_session(self, session_name):
        pass

    def is_enabled(self):
        windows = sublime.windows()
        for window in windows:
            if is_saveable(window):
                return True

        return False


def is_saveable(window):
    return bool(window.views()) or bool(window.project_data())
