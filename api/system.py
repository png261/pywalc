import socket
import json
from app import app
from settings import OS, BACKUP_FILE
from color import COLOR
from wallpaper import WALLPAPER


@app.get("/reset", tags=["system"])
def reset_all():
    backup = open(BACKUP_FILE)
    data = json.load(backup)
    COLOR.update(data["colors"])
    WALLPAPER.update({"current": "current"})


@app.get("/sys", tags=["system"])
def get_system_info():
    name = socket.gethostname()
    return {"os": OS, "name": name}


@app.get("/health", tags=["system"])
def check_health():
    return {"connected": True}
