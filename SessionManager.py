import json
import os

import sublime
import sublime_plugin

from .modules import messages


class SaveSession(sublime_plugin.WindowCommand):
    def run(self):
        self.window.show_input_panel(
            messages.dialog("session_name"),
            self.generate_name(),
            self.save_session
        )

    def generate_name(self):
        return "placeholder"

    def save_session(self, session_name):
        pass
