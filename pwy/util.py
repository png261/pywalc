import shutil
import pyperclip
import os

def copy_dir(source, dest):
    shutil.copy(source, dest)

def copyToClipboard(data):
    pyperclip.copy(data)

def showQRCODE():
    print("TODO: show qr code")

def create_dir(directory):
    """Alias to create the cache dir."""
    os.makedirs(directory, exist_ok=True)

def save_file(data, export_file):
    """Write data to a file."""
    print(export_file)
    create_dir(os.path.dirname(export_file))

    with open(export_file, "w") as file:
        file.write(data)

def read_file(input_file):
    """Read data from a file and trim newlines."""
    with open(input_file, "r") as file:
        return file.read().splitlines()


 

