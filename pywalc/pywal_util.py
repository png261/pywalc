import pywal
import os

from .settings import BACKUP_FILE, PYWAL_DATA_FILE, PYWALL_CACHE, PYWAL_MODULE_DIR
from . import util


def setup_backup():
    util.copy_dir(PYWAL_DATA_FILE, BACKUP_FILE)


def apply(data):
    pywal.export.every(data)
    pywal.sequences.send(data)
    pywal.reload.env()


def convert_to_pywal_util(colors, wallpaper):
    colors_value = [colors[color_name] for color_name in colors]
    data = pywal.colors.colors_to_dict(colors_value, wallpaper)
    return data


def get_colors():
    return pywal.colors.file(PYWAL_DATA_FILE)["colors"]


def get_backup_colors():
    return util.read_file_json(BACKUP_FILE)["colors"]


def get_current_wallpaper():
    return util.read_file(os.path.join(PYWALL_CACHE, "wal"))[0]


def get_color_from_image(image_path):
    return pywal.colors.get(image_path)["colors"]


def change_wallpaper(image):
    image = pywal.image.get(image)
    pywal.wallpaper.change(image)


def get_theme_list():
    dark_themes = [
        theme.name.replace(".json", "") for theme in pywal.theme.list_themes()
    ]
    light_themes = [
        theme.name.replace(".json", "") for theme in pywal.theme.list_themes(dark=False)
    ]
    return {"dark": dark_themes, "light": light_themes}


def get_theme(name, category):
    themes_path = os.path.join(
        PYWAL_MODULE_DIR, "colorschemes", category, name + ".json"
    )
    themes = util.read_file_json(themes_path)
    return themes
