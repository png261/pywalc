import os
import argparse

from .settings import (
    __version__,
    PYWAL_FILE_PATH,
    BACKUP_FILE,
    WALLPAPER_DIR,
    CACHE_DIR,
    PYWAL_CURRENT_WALLPAPER,
)
from .server import Server
from . import util


def get_args():
    """Get the script arguments."""
    description = "pywalc - Pywal client"
    arg = argparse.ArgumentParser(description=description)

    arg.add_argument("-v", action="store_true", help='Print "pywalc" version.')

    return arg


def parse_args_exit(parser):
    """Process args that exit."""
    args = parser.parse_args()

    if args.v:
        parser.exit(0, "wal %s\n" % __version__)


def main():
    """Main script function."""
    util.setup_logging()
    util.create_dir(CACHE_DIR)
    util.create_dir(WALLPAPER_DIR)
    util.copy_dir(PYWAL_FILE_PATH, BACKUP_FILE)
    util.copy_dir(PYWAL_CURRENT_WALLPAPER, os.path.join(WALLPAPER_DIR, "current"))

    parser = get_args()
    parse_args_exit(parser)

    server = Server(2601)
    server.run()


if __name__ == "__main__":
    main()
