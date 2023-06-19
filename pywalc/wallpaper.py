import os
from fastapi import File, UploadFile
from typing import List

from .settings import WALLPAPER_DIR
from . import util
from . import pywal_util


class Wallpaper:
    def __init__(self):
        self.wallpaper = {}
        self.wallpaper["current"] = "current"
        self.wallpaper["list"] = os.listdir(WALLPAPER_DIR)

    def update(self):
        self.wallpaper["list"] = os.listdir(WALLPAPER_DIR)

    def get(self):
        self.update()
        return self.wallpaper

    def get_colors(self, id):
        return pywal_util.get_color_from_image(os.path.join(WALLPAPER_DIR, id))

    def get_current(self):
        return self.wallpaper["current"]

    def set(self, id: str):
        self.wallpaper["current"] = id
        return self.get()

    async def upload(self, files: List[UploadFile] = File(...)):
        imgs = []
        for file in files:
            filename = util.get_random_id()
            util.save_file(
                await file.read(), os.path.join(WALLPAPER_DIR, filename), mode="wb"
            )
            imgs.append(filename)

        self.update()
        return imgs

    def apply(self):
        pywal_util.change_wallpaper(
            os.path.join(WALLPAPER_DIR, self.wallpaper["current"])
        )
        return self.get()

    def reset(self):
        self.wallpaper["current"] = "current"
