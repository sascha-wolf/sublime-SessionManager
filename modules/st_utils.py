import sublime


def open_window():
    sublime.run_command("new_window")
    return sublime.active_window()
