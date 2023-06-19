import pywal
import os

__version__ = "0.2.1"

HOME = pywal.settings.HOME
XDG_CACHE_DIR = os.getenv("XDG_CACHE_HOME", os.path.join(HOME, ".cache"))

PYWALL_CACHE = pywal.settings.CACHE_DIR
PYWAL_DATA_FILE = os.path.join(PYWALL_CACHE, "colors.json")
PYWAL_MODULE_DIR = pywal.settings.MODULE_DIR

MODULE_DIR = os.path.dirname(__file__)
CACHE_DIR = os.path.join(XDG_CACHE_DIR, "pywalc")
WALLPAPER_DIR = os.path.join(CACHE_DIR, "wallpapers")
BACKUP_FILE = os.path.join(CACHE_DIR, "backup.json")

OS = pywal.settings.OS
