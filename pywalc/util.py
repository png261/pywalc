"""
Misc helper functions.
"""
import json
import logging
import os
import shutil
import sys
import qrcode
import io


def read_file(input_file):
    """Read data from a file and trim newlines."""
    with open(input_file, "r") as file:
        return file.read().splitlines()


def read_file_json(input_file):
    """Read data from a json file."""
    with open(input_file, "r") as json_file:
        return json.load(json_file)


def read_file_raw(input_file):
    """Read data from a file as is, don't strip
    newlines or other special characters."""
    with open(input_file, "r") as file:
        return file.readlines()


def save_file(data, export_file, mode="w"):
    """Write data to a file."""
    create_dir(os.path.dirname(export_file))

    try:
        with open(export_file, mode) as file:
            file.write(data)
    except PermissionError:
        logging.warning("Couldn't write to %s.", export_file)


def save_file_json(data, export_file):
    """Write data to a json file."""
    create_dir(os.path.dirname(export_file))

    with open(export_file, "w") as file:
        json.dump(data, file, indent=4)


def create_dir(directory):
    """Alias to create the cache dir."""
    os.makedirs(directory, exist_ok=True)


def setup_logging():
    """Logging config."""
    logging.basicConfig(
        format=(
            "[%(levelname)s\033[0m] " "\033[1;31m%(module)s\033[0m: " "%(message)s"
        ),
        level=logging.INFO,
        stream=sys.stdout,
    )
    logging.addLevelName(logging.ERROR, "\033[1;31mE")
    logging.addLevelName(logging.INFO, "\033[1;32mI")
    logging.addLevelName(logging.WARNING, "\033[1;33mW")


def copy_dir(source, dest):
    try:
        shutil.copyfile(source, dest)
    except shutil.SameFileError:
        pass


def show_ascii_qrcode(
    url,
):
    qr = qrcode.QRCode()
    qr.add_data(url)
    f = io.StringIO()
    qr.print_ascii(out=f)
    f.seek(0)
    print(f.read())
