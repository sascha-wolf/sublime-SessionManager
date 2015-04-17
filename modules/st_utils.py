import sublime

from os import path


def close_windows(windows = None):
    if not windows:
        windows = sublime.windows()

    for window in windows:
        window.run_command('close_window')


def open_window():
    sublime.run_command("new_window")
    return sublime.active_window()


def resolve_project_paths(project_file_path, project_data):
    if not project_data:
        return None
    if not project_file_path:
        return project_data

    resolved = dict(project_data)
    basefolder = path.dirname(project_file_path)
    for folder in resolved['folders']:
        folder_path = folder['path']
        if path.isabs(folder_path):
            continue

        new_path = path.join(basefolder, folder_path)
        new_path = path.normpath(new_path)
        folder['path'] = new_path

    return resolved
