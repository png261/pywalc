import pywal
import os
import shutil

HOME = pywal.settings.HOME
OS = pywal.settings.OS
CACHE_DIR = pywal.settings.CACHE_DIR
MODULE_DIR = pywal.settings.MODULE_DIR

WALLPAPER_DIR=os.path.join(HOME,".cache","pwy","wallpapers")
DATA_DIR=os.path.join(HOME,".cache","pwy")

BACKUP_FILE=os.path.join(DATA_DIR,"backup.json")
WAL_FILE=os.path.join(CACHE_DIR,"colors.json")

shutil.copy(WAL_FILE, BACKUP_FILE)
WAL= pywal.colors.file(WAL_FILE)
