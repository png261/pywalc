import os
import uuid
import pywal
from fastapi import File, UploadFile
from typing import List

from .settings import WALLPAPER_DIR
from . import util


class Wallpaper:
    def __init__(self):
        self.data = {"current": "current", "list": os.listdir(WALLPAPER_DIR)}

    def update(self):
        self.data.update({"list": os.listdir(WALLPAPER_DIR)})

    def get(self):
        self.update()
        return self.data

    def get_colors(self, id):
        img = os.path.join(WALLPAPER_DIR, id)
        return pywal.colors.get(img)["colors"]

    def get_current(self):
        return self.data["current"]

    def set(self, id: str):
        self.data.update({"current": id})
        return self.get()

    async def upload(self, files: List[UploadFile] = File(...)):
        imgs = []
        for file in files:
            content = await file.read()
            filename = str(uuid.uuid1().hex)
            util.save_file(content, os.path.join(WALLPAPER_DIR, filename), mode="wb")
            imgs.append(filename)
        self.update()
        return imgs

    def load(self):
        image = pywal.image.get(os.path.join(WALLPAPER_DIR, self.data["current"]))
        pywal.wallpaper.change(image)
        return self.get()

    def reset(self):
        self.data["current"] = "current"
