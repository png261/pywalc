import pywal
import os
from .settings import CACHE_DIR, WALLPAPER_DIR

WAL= pywal.colors.file(os.path.join(CACHE_DIR,"colors.json"))
THEME={}
COLOR={}
WALLPAPER={}

# wallpaper
def update_wall():
    WALLPAPER.update({
        'current': WAL["wallpaper"],
        'list': os.listdir(WALLPAPER_DIR)
    })

# color
def update_color():
    WAL = pywal.colors.file(os.path.join(CACHE_DIR,"colors.json"))
    COLOR.update(WAL["colors"])

# theme
def update_theme():
    dark_themes = [theme.name.replace(".json", "")
                   for theme in pywal.theme.list_themes()]
    light_themes = [theme.name.replace(".json", "")
                   for theme in pywal.theme.list_themes(dark=False)]
    THEME.update({
        "dark": dark_themes,
        "light": light_themes
    })

update_theme()
