import json
import sublime

from ..modules import session


class SessionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, session.Session):
            return {
                "name": obj.name,
                "windows": [
                    WindowEncoder.default(self, w) for w in obj.windows
                ]
            }

        return json.JSONEncoder.default(self, obj)


class WindowEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, session.Window):
            return {
                "project": obj.project,
                "project_path": obj.project_path,
                "views": [
                    ViewEncoder.default(self, v) for v in obj.views
                ]
            }

        return json.JSONEncoder.default(self, obj)


class ViewEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, session.View):
            return {
                "file_path": obj.file_path,
                "active": obj.active,
                "sel_regions": [
                    RegionEncoder.default(self, r) for r in obj.sel_regions
                ],
                "visible_region": RegionEncoder.default(self, obj.visible_region)
            }

        return json.JSONEncoder.default(self, obj)


class RegionEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, sublime.Region):
            return (obj.a, obj.b)

        return json.JSONEncoder.default(self, obj)
