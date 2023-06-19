import os
import argparse

from .server import Server
from . import util
from .settings import (
    __version__,
    PYWAL_FILE_PATH,
    BACKUP_FILE,
    WALLPAPER_DIR,
    CACHE_DIR,
    PYWAL_CURRENT_WALLPAPER,
)


class App:
    def __init__(self):
        self.port = 2601

    def setup(self):
        util.setup_logging()
        self._setup_create_dir()
        self._setup_copy_pywal_data()

    def _setup_create_dir(self):
        util.create_dir(CACHE_DIR)
        util.create_dir(WALLPAPER_DIR)

    def _setup_copy_pywal_data(self):
        util.copy_dir(PYWAL_FILE_PATH, BACKUP_FILE)
        util.copy_dir(PYWAL_CURRENT_WALLPAPER, os.path.join(WALLPAPER_DIR, "current"))

    def parse_args(self):
        parser = self._get_args()
        self._parse_args_exit(parser)
        self._parse_args_exit(parser)
        self._parse_args(parser)

    def _get_args(self):
        description = "pywalc - Pywal client"
        arg = argparse.ArgumentParser(description=description)

        arg.add_argument("-v", action="store_true", help='print "pywalc" version.')

        arg.add_argument("-p", metavar="port", help="port to start Api server")

        return arg

    def _parse_args_exit(self, parser):
        args = parser.parse_args()

        if args.v:
            parser.exit(0, "pywalc %s\n" % __version__)

    def _parse_args(self, parser):
        args = parser.parse_args()

        if args.p:
            self.port = args.p

    def run(self):
        server = Server(self.port)
        server.run()
