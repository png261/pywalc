"""
App
"""

import os
import argparse

import pywalc
from .server import Server
from . import util
from . import pywal_util
from .settings import (
    WALLPAPER_DIR,
    CACHE_DIR,
)


class App:
    """App"""

    def __init__(self):
        """Initialize app"""
        self.port = 2601

    def setup(self):
        """Setup"""
        self._setup_create_dir()
        self._setup_pywal_data()

    def _setup_create_dir(self):
        """Setup dir"""
        util.create_dir(CACHE_DIR)
        util.create_dir(WALLPAPER_DIR)

    def _setup_pywal_data(self):
        """Setup Pywal data"""
        pywal_util.setup_backup()
        util.copy_file(
            pywal_util.get_current_wallpaper(),
            os.path.join(WALLPAPER_DIR, "current"),
        )

    def parse_args(self):
        """Process args"""
        parser = self._get_args()
        self._parse_args_exit(parser)
        self._parse_args_exit(parser)
        self._parse_args(parser)

    def _get_args(self):
        """Get the script arguments"""
        description = "pywalc - Pywal client"
        arg = argparse.ArgumentParser(description=description)

        arg.add_argument(
            "-v", action="store_true", help='print "pywalc" version.'
        )

        arg.add_argument("-p", metavar="port", help="port to start Api server")

        return arg

    def _parse_args_exit(self, parser):
        """Process args that exit"""
        args = parser.parse_args()

        if args.v:
            parser.exit(0, f"pywalc {pywalc.__version__}\n")

    def _parse_args(self, parser):
        """Process args"""
        args = parser.parse_args()

        if args.p:
            self.port = args.p

    def run(self):
        """Run app"""
        server = Server(self.port)
        server.setup()
        server.run()
