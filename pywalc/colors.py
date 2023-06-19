from fastapi import Request

from . import pywal_util


class Color:
    def __init__(self):
        self.colors = pywal_util.get_colors()

    def get(self):
        return self.colors

    async def update(self, colors: Request):
        self.colors.update(await colors.json())
        return self.get()

    def apply(self, wallpaper):
        data = pywal_util.convert_to_pywal_util(self.colors, wallpaper)
        pywal_util.apply(data)
        return self.get()

    def reset(self):
        self.colors = pywal_util.get_backup_colors()
