import sublime
import sublime_plugin

from datetime import datetime

from .modules import messages
from .modules import serialize
from .modules import settings
from .modules.session import Session

on_query_completions_callbacks = {}

def plugin_loaded():
    settings.load()


def error_message(error_key, *args):
    sublime.error_message(messages.error(error_key, *args))


def get_sessions_list():
    return serialize.available()


class InputCompletionsListener(sublime_plugin.EventListener):
    def on_query_completions(self, view, prefix, locations):
        if view.id() in on_query_completions_callbacks.keys():
            return on_query_completions_callbacks[view.id()](prefix, locations)


class SaveSession(sublime_plugin.ApplicationCommand):
    input_panel = None

    def run(self):
        self.input_panel = sublime.active_window().show_input_panel(
            messages.dialog("session_name"),
            self.generate_name(),
            on_done=self.save_session,
            on_change=self.input_changed,
            on_cancel=None
        )
        self.register_callbacks()

    def register_callbacks(self):
        on_query_completions_callbacks[self.input_panel.id()] = lambda prefix, locations: self.on_query_completions(prefix, locations)

    def on_query_completions(self, prefix, locations):
        if len(prefix) > 0:
            completions_list = get_sessions_list()
            #needed the "hit Tab" label due to https://github.com/SublimeTextIssues/Core/issues/1727           
            completions_list = [["{0}\t hit Tab to insert".format(item), item] for item in completions_list if item.startswith(prefix)]
            if len(completions_list) == 1 and completions_list[0][1] != prefix:
                #workaround for https://github.com/SublimeTextIssues/Core/issues/2425
                completions_list += [["{0}\t hit Tab to insert".format(prefix), prefix]]
            return (
                        completions_list,
                        sublime.INHIBIT_WORD_COMPLETIONS | sublime.INHIBIT_EXPLICIT_COMPLETIONS
                    )
        else: #if no prefix return None
            return

    def input_changed(self, session_name_prefix):
        """
            on input changed open autocomplete menu with a delay
        """
        if len(session_name_prefix) > 0 and \
        self.input_panel and \
        self.input_panel.command_history(0)[0] not in ['insert_completion', 'insert_best_completion']: #remove the looping
            if self.input_panel.is_auto_complete_visible():
                self.input_panel.run_command('hide_auto_complete')
            delay = 500
            sublime.set_timeout(lambda: self.run_autocomplete(), delay)
        else:
            return

    def run_autocomplete(self):
        self.input_panel.run_command('auto_complete')

    def generate_name(self):
        nameformat = settings.get('session_name_format')
        return datetime.now().strftime(nameformat)

    def save_session(self, session_name):
        if not serialize.is_valid(session_name):
            error_message("invalid_name", session_name)
            self.run()
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
        self.session_names = get_sessions_list()
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
