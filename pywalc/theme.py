import os
import json
import pywal
from .settings import MODULE_DIR

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
        themes_path = os.path.join(
            MODULE_DIR, "colorschemes", category, name + ".json"
        )
        with open(themes_path) as file:
            themes = json.loads(file.read())
        return themes["colors"]
