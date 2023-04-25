import pywal
import os

HOME = pywal.settings.HOME
OS = pywal.settings.OS
PYWALL_CACHE = pywal.settings.CACHE_DIR
MODULE_DIR = pywal.settings.MODULE_DIR

CACHE_DIR = os.path.join(HOME, ".cache", "pwy")
WALLPAPER_DIR = os.path.join(CACHE_DIR, "wallpapers")

BACKUP_FILE = os.path.join(CACHE_DIR, "backup.json")
WAL_FILE = os.path.join(PYWALL_CACHE, "colors.json")

WAL = pywal.colors.file(WAL_FILE)
