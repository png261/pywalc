"""
Wallpaper
"""

import os
from typing import List
from fastapi import File, UploadFile

from .settings import WALLPAPER_DIR
from . import util
from . import pywal_util


class Wallpaper:
    """Wallpaper"""

    def __init__(self):
        """Initialize wallpaper"""
        self.wallpaper = {}
        self.wallpaper["current"] = "current"
        self.wallpaper["list"] = os.listdir(WALLPAPER_DIR)

    def update(self):
        """Reload list wallpaper"""
        self.wallpaper["list"] = os.listdir(WALLPAPER_DIR)

    def get(self):
        """Get list wallpaper"""
        self.update()
        return self.wallpaper

    def get_colors(self, wallpaper_id):
        """Get wallpaper's colors by ID"""
        return pywal_util.get_color_from_image(
            os.path.join(WALLPAPER_DIR, wallpaper_id)
        )

    def get_current(self):
        """Get current wallpaper ID"""
        return self.wallpaper["current"]

    def set(self, wallpaper_id: str):
        """Change current wallpaper"""
        self.wallpaper["current"] = wallpaper_id
        return self.get()

    async def upload(self, files: List[UploadFile] = File(...)):
        """Upload images with random IDs"""
        images = []
        for file in files:
            filename = util.get_random_id()
            util.save_file(
                await file.read(), os.path.join(WALLPAPER_DIR, filename), mode="wb"
            )
            images.append(filename)

        self.update()
        return images

    def apply(self):
        """Apply wallpaper change"""
        pywal_util.change_wallpaper(
            os.path.join(WALLPAPER_DIR, self.wallpaper["current"])
        )
        return self.get()

    def reset(self):
        """Reset wallpaper"""
        self.wallpaper["current"] = "current"
