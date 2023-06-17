import pywal
from .settings import WAL
from fastapi import Request

class Color:
    def __init__(self):
        self.data = WAL["colors"]

    def get(self):
        return self.data

    async def update(self, colors: Request):
        self.data.update(await colors.json())
        return self.data

    def load(self, wallpaper):
        colors = [self.data[name] for name in self.data]
        data = pywal.colors.colors_to_dict(colors, wallpaper)
        pywal.export.every(data)
        pywal.sequences.send(data)
        pywal.reload.env()
        return self.data
