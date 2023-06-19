from . import pywal_util


class Theme:
    def __init__(self):
        self.data = pywal_util.get_theme_list()

    def get(self):
        return self.data

    def get_color(self, name, category):
        return pywal_util.get_theme(name, category)["colors"]
