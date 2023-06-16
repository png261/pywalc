import argparse
import sys

from . import util

from .settings import __version__,WAL_FILE, BACKUP_FILE, WALLPAPER_DIR,CACHE_DIR
from .server import Server

server = Server()

def get_args():
    """Get the script arguments."""
    description = "Pwy - Change Pywal color online"
    arg = argparse.ArgumentParser(description=description)

    arg.add_argument("-start", action="store_true",
                     help="Start server")

    arg.add_argument("-stop", action="store_true",
                     help="Stop server")

    arg.add_argument("-copy", action="store_true",
                     help="Copy control website url to clipboard")

    arg.add_argument("-qrcode",action="store_true",
                     help="Show qrcode to control website")

    arg.add_argument("-v", action="store_true",
                     help="Print \"wal\" version.")


    return arg


def parse_args_exit(parser):
    """Process args that exit."""
    args = parser.parse_args()

    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)

    if args.v:
        parser.exit(0, "pywal %s\n" % __version__)

    if args.start:
        server.run();

    if args.stop:
        server.stop();

    if args.copy:
        url = server.getUrl();
        util.copyToClipboard(url);

    if args.qrcode:
        util.showQRCODE();


def parse_args(parser):
    """Process args."""
    args = parser.parse_args()


def main():
    """Main script function."""
    util.create_dir(CACHE_DIR)
    util.create_dir(WALLPAPER_DIR)
    util.copy_dir(WAL_FILE, BACKUP_FILE)

    parser = get_args()

    parse_args_exit(parser)
    parse_args(parser)


if __name__ == "__main__":
    main()
