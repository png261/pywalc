import os
import argparse

from .server import Server
from . import util
from . import pywal_util
from .settings import (
    __version__,
    WALLPAPER_DIR,
    CACHE_DIR,
)


class App:
    def __init__(self):
        self.port = 2601

    def setup(self):
        self._setup_create_dir()
        self._setup_pywal_data()

    def _setup_create_dir(self):
        util.create_dir(CACHE_DIR)
        util.create_dir(WALLPAPER_DIR)

    def _setup_pywal_data(self):
        pywal_util.setup_backup()
        util.copy_dir(
            pywal_util.get_current_wallpaper(), os.path.join(WALLPAPER_DIR, "current")
        )

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
