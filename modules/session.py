import sublime

from . import st_utils


class Session:
    def __init__(self, name, window_sessions):
        self.name = name
        self.windows = window_sessions

    @classmethod
    def save(cls, name, st_windows):
        return cls(
            name,
            [Window.save(w) for w in st_windows]
        )

    def load(self):
        for window in self.windows:
            window.load()


class Window:
    def __init__(self, project, project_path, view_sessions):
        self.project = project
        self.project_path = project_path
        self.views = view_sessions

    @classmethod
    def save(cls, st_window):
        project = st_window.project_data()
        project_path = st_window.project_file_name()
        views = [View.save(v) for v in st_window.views()]

        return cls(project, project_path, views)

    def load(self):
        st_window = st_utils.open_window()

        self._load_project(st_window)
        self._load_views(st_window)

    def _load_project(self, st_window):
        st_window.set_project_data(self.project)

    def _load_views(self, st_window):
        # Workaround: Sublime focus bug on new views (issue #39)
        sublime.set_timeout(lambda: self._load_views_intern(st_window), 0)

    def _load_views_intern(self, st_window):
        for view in self.views:
            view.load(st_window)


class View:
    def __init__(self, file_path, active, sel_regions, visible_region):
        self.file_path = file_path
        self.active = active
        self.sel_regions = sel_regions
        self.visible_region = visible_region

    @classmethod
    def save(cls, st_view):
        file_path = st_view.file_name()
        active = (st_view.id() == st_view.window().active_view().id())
        sel_regions = [region for region in st_view.sel()]
        visible_region = st_view.visible_region()

        return cls(file_path, active, sel_regions, visible_region)

    def load(self, st_window):
        view = st_window.open_file(self.file_path)
        sublime.set_timeout(lambda: self._init_view(view), 50)

    def _init_view(self, view):
        if view.is_loading():
            sublime.set_timeout(lambda: self._init_view(view), 50)
            return

        selection = view.sel()
        selection.clear()
        selection.add_all(self.sel_regions)

        view.show_at_center(self.visible_region)

        if self.active:
            view.window().focus_view(view)
