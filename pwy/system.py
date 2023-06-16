import socket
import json

from .settings import OS, BACKUP_FILE
from .colors import COLOR
from .wallpaper import WALLPAPER
from fastapi import APIRouter

systemRouter = APIRouter()


@systemRouter.get("/reset", tags=["system"])
def reset():
    with open(BACKUP_FILE) as file:
        data = json.load(file)
    COLOR.clear()
    COLOR.update(data["colors"])
    WALLPAPER["current"] = "current"
    return {"color": COLOR, "wallpaper": WALLPAPER}


@systemRouter.get("/sys", tags=["system"])
def get_system_info():
    return {"os": OS, "name": socket.gethostname()}


@systemRouter.get("/health", tags=["system"])
def check_health():
    return {"connected": True}
