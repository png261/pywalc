import socket
import json
from app import app
from settings import OS, BACKUP_FILE
from color import COLOR
from wallpaper import WALLPAPER


@app.get("/reset", tags=["system"])
def reset():
    data = json.load(open(BACKUP_FILE))
    COLOR.update(data["colors"])
    WALLPAPER.update({"current": "current"})
    return {"color": COLOR, "wallpaper": WALLPAPER}


@app.get("/sys", tags=["system"])
def get_system_info():
    return {"os": OS, "name": socket.gethostname()}


@app.get("/health", tags=["system"])
def check_health():
    return {"connected": True}
