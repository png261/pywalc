import pywal
import os

HOME = pywal.settings.HOME
CACHE_DIR = pywal.settings.CACHE_DIR
MODULE_DIR = pywal.settings.MODULE_DIR

WALLPAPER_DIR="app/static/wallpapers/"
DATA_DIR=os.path.join(HOME,".cache","pwy")
BACKUP_FILE=os.path.join(DATA_DIR,"backup.json")

wal = pywal.colors.file(os.path.join(CACHE_DIR,"colors.json"))
dark_themes = os.listdir(os.path.join(MODULE_DIR, "colorschemes", "dark"))
dark_themes  = [theme.split('.')[0] for theme in dark_themes]

light_themes = os.listdir(os.path.join(MODULE_DIR, "colorschemes", "light"))
light_themes  = [theme.split('.')[0] for theme in light_themes]

theme_list = {
    "dark": dark_themes,
    "light": light_themes
}

DATA = {
    'color': wal["colors"],
    'theme':{
        'dark': True,
        'list': theme_list
    },
    'wallpaper':{
        'current': wal["wallpaper"],
        'list': os.listdir(WALLPAPER_DIR)
    },
    'options':{
        'update_on_change' : True,
    }
}


