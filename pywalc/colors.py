"""
Color
"""

from fastapi import Request

from . import pywal_util


class Color:
    """Color"""

    def __init__(self):
        """Initialize Color"""
        self.colors = pywal_util.get_colors()

    def get(self):
        """Get colors"""
        return self.colors

    async def update(self, colors: Request):
        """Update colors"""
        self.colors.update(await colors.json())
        return self.get()

    def apply(self, wallpaper):
        """Apply colors change"""
        data = pywal_util.convert_to_pywal_data(self.colors, wallpaper)
        pywal_util.apply(data)
        return self.get()

    def reset(self):
        """Reset colors to backup colors"""
        self.colors = pywal_util.get_backup_colors()
