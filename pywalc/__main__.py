import os

from . import util
from .settings import WAL_FILE, BACKUP_FILE, WALLPAPER_DIR, CACHE_DIR, PYWALL_CACHE
from .server import Server


def main():
    """Main script function."""
    util.setup_logging()

    util.create_dir(CACHE_DIR)
    util.create_dir(WALLPAPER_DIR)
    util.copy_dir(WAL_FILE, BACKUP_FILE)

    current_wallpaper = util.read_file(os.path.join(PYWALL_CACHE, 'wal'))[0]
    util.copy_dir(current_wallpaper, os.path.join(WALLPAPER_DIR,'current'))

    server = Server()
    server.run()

if __name__ == "__main__":
    main()
