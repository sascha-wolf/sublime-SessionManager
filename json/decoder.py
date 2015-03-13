import json
import sublime

from ..modules import session


def _objectify(s):
    if isinstance(s, str):
        return json.loads(s)

    return s


class SessionDecoder(json.JSONDecoder):
    def decode(self, s):
        o = _objectify(s)
        try:
            name = o["name"]
            windows = [
                WindowDecoder.decode(self, w) for w in o["windows"]
            ]
        except NameError:
            pass
        else:
            return session.Session(name, windows)

        return json.JSONDecoder.decode(self, o)


class WindowDecoder(json.JSONDecoder):
    def decode(self, s):
        o = _objectify(s)
        try:
            project = o["project"]
            project_path = o["project_path"]
            views = [
                ViewDecoder.decode(self, view) for view in o["views"]
            ]
        except NameError:
            pass
        else:
            return session.Window(project, project_path, views)

        return json.JSONDecoder.decode(self, o)


class ViewDecoder(json.JSONDecoder):
    def decode(self, s):
        o = _objectify(s)
        try:
            file_path = o["file_path"]
            active = o["active"]
            sel_regions = [
                RegionDecoder.decode(self, region) for region in o["sel_regions"]
            ]
            visible_region = RegionDecoder.decode(self, o["visible_region"])
        except NameError:
            pass
        else:
            return session.View(file_path, active, sel_regions, visible_region)

        return json.JSONDecoder.decode(self, o)


class RegionDecoder(json.JSONDecoder):
    def decode(self, s):
        o = _objectify(s)
        try:
            a = o[0]
            b = o[1]
        except IndexError:
            pass
        else:
            return sublime.Region(a, b)

        return json.JSONDecoder.decode(self, o)
