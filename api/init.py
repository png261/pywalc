import shutil
from settings import WAL_FILE, BACKUP_FILE


def setupFiles():
    shutil.copy(WAL_FILE, BACKUP_FILE)
