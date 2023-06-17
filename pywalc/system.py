import socket
import json

from .settings import OS, BACKUP_FILE

class System:
    def reset(self, color, wallpaper):
        with open(BACKUP_FILE) as file:
            data = json.load(file)
        color.clear()
        color.update(data["colors"])
        wallpaper["current"] = "current"
        return {"color": color, "wallpaper": wallpaper}

    def get(self):
        return {"os": OS, "name": socket.gethostname()}
