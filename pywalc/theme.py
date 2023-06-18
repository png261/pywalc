import os
import pywal
from .settings import PYWAL_MODULE_DIR
from . import util


class Theme:
    def __init__(self):
        dark_themes = [
            theme.name.replace(".json", "") for theme in pywal.theme.list_themes()
        ]
        light_themes = [
            theme.name.replace(".json", "")
            for theme in pywal.theme.list_themes(dark=False)
        ]

        self.data = {"dark": dark_themes, "light": light_themes}

    def get(self):
        return self.data

    def set(self, name, category):
        themes_path = os.path.join(PYWAL_MODULE_DIR, "colorschemes", category, name + ".json")
        themes = util.read_file_json(themes_path)
        return themes["colors"]
