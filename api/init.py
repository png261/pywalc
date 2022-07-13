import shutil
from settings import WAL_FILE, BACKUP_FILE

shutil.copy(WAL_FILE, BACKUP_FILE)

