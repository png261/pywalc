import pywal
import os
import shutil

HOME = pywal.settings.HOME
OS = pywal.settings.OS
PYWALL_CACHE = pywal.settings.CACHE_DIR
MODULE_DIR = pywal.settings.MODULE_DIR

WALLPAPER_DIR = os.path.join(HOME, ".cache", "pwy", "wallpapers")
DATA_DIR = os.path.join(HOME, ".cache", "pwy")

BACKUP_FILE = os.path.join(DATA_DIR, "backup.json")
WAL_FILE = os.path.join(PYWALL_CACHE, "colors.json")

WAL = pywal.colors.file(WAL_FILE)
