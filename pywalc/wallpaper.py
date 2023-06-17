import os
import uuid
from typing import List
import pywal
from .settings import WALLPAPER_DIR
from . import util
from fastapi import File, UploadFile

class Wallpaper:
    def __init__(self):
        self.data = {'current': 'current', 'list': os.listdir(WALLPAPER_DIR)}

    def get_info(self):
        return self.data

    def update(self,):
        self.data.update({'list': os.listdir(WALLPAPER_DIR)})

    def get(self):
        self.update()
        return self.data

    def get_colors(self,id):
        img = os.path.join(WALLPAPER_DIR, id)
        colors = pywal.colors.get(img)["colors"]
        return colors

    def get_current(self):
        return self.data["current"]

    def set(self, id: str):
        self.data.update({"current": id})
        return self.data

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
        return self.data
