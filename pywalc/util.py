"""
Helper functions.
"""

import json
import os
import shutil
import uuid
import io
import qrcode


def read_file(input_file):
    """Read data from a file and trim newlines"""
    with open(input_file, "r") as file:
        return file.read().splitlines()


def read_file_json(input_file):
    """Read data from a json file"""
    with open(input_file, "r") as json_file:
        return json.load(json_file)


def read_file_raw(input_file):
    """Read data from a file as is, don't strip
    newlines or other special characters"""
    with open(input_file, "r") as file:
        return file.readlines()


def save_file(data, export_file, mode="w"):
    """Write data to a file"""
    create_dir(os.path.dirname(export_file))

    try:
        with open(export_file, mode) as file:
            file.write(data)
    except PermissionError:
        print("Couldn't write to %s.", export_file)


def save_file_json(data, export_file):
    """Write data to a json file"""
    create_dir(os.path.dirname(export_file))

    with open(export_file, "w") as file:
        json.dump(data, file, indent=4)


def create_dir(directory):
    """Alias to create the cache dir"""
    os.makedirs(directory, exist_ok=True)


def copy_file(source, dest):
    """Copy file"""
    try:
        shutil.copyfile(source, dest)
    except shutil.SameFileError:
        pass


def show_ascii_qrcode(url):
    """Show ASCII QR code"""
    qr_gen = qrcode.QRCode()
    qr_gen.add_data(url)
    output_buffer = io.StringIO()
    qr_gen.print_ascii(out=output_buffer)
    output_buffer.seek(0)
    print(output_buffer.read())


def get_random_id():
    """Generate random id"""
    return str(uuid.uuid1().hex)
