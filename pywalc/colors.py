import pywal
from fastapi import Request

from .settings import BACKUP_FILE, PYWAL_DATA
from . import util


class Color:
    def __init__(self):
        self.data = PYWAL_DATA["colors"]

    def get(self):
        return self.data

    async def update(self, colors: Request):
        self.data.update(await colors.json())
        return self.get()

    def load(self, wallpaper):
        colors = [self.data[name] for name in self.data]
        data = pywal.colors.colors_to_dict(colors, wallpaper)
        pywal.export.every(data)
        pywal.sequences.send(data)
        pywal.reload.env()
        return self.get()

    def reset(self):
        backup = util.read_file_json(BACKUP_FILE)
        self.data.clear()
        self.data.update(backup["colors"])
