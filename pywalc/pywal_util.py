"""
Pywal helper functions.
"""

import os
import pywal

from .settings import BACKUP_FILE, PYWAL_DATA_FILE, PYWALL_CACHE, PYWAL_MODULE_DIR
from . import util


def setup_backup():
    """Backup current Pywal data file"""
    util.copy_file(PYWAL_DATA_FILE, BACKUP_FILE)


def apply(data):
    """Apply change"""
    pywal.export.every(data)
    pywal.sequences.send(data)
    pywal.reload.env()


def convert_to_pywal_data(colors, wallpaper):
    """Convert colors and wallpaper to Pywal data"""
    colors_value = [colors[color_name] for color_name in colors]
    data = pywal.colors.colors_to_dict(colors_value, wallpaper)
    return data


def get_colors():
    """Get Pywal colors"""
    return pywal.colors.file(PYWAL_DATA_FILE)["colors"]


def get_backup_colors():
    """Get colors from backup file"""
    return util.read_file_json(BACKUP_FILE)["colors"]


def get_current_wallpaper():
    """Get Pywal current wallpaper"""
    return util.read_file(os.path.join(PYWALL_CACHE, "wal"))[0]


def get_color_from_image(image_path):
    """Get color from image"""
    return pywal.colors.get(image_path)["colors"]


def change_wallpaper(image):
    """Change wallpaper"""
    image = pywal.image.get(image)
    pywal.wallpaper.change(image)


def get_theme_list():
    """Get theme list"""
    dark_themes = [
        theme.name.replace(".json", "") for theme in pywal.theme.list_themes()
    ]
    light_themes = [
        theme.name.replace(".json", "") for theme in pywal.theme.list_themes(dark=False)
    ]
    return {"dark": dark_themes, "light": light_themes}


def get_theme(category, name):
    """Get theme's colors by category and name"""
    themes_path = os.path.join(
        PYWAL_MODULE_DIR, "colorschemes", category, name + ".json"
    )
    themes = util.read_file_json(themes_path)
    return themes
