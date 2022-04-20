import pywal
import os
from .settings import WALLPAPER_DIR
from .data import COLOR, THEME, WALLPAPER

def reload():
    img_path = os.path.join(WALLPAPER_DIR,WALLPAPER["current"])
    data = pywal.colors.colors_to_dict(COLOR,img_path)
    pywal.export.every(data)
    pywal.sequences.send(data)
    pywal.reload.xrdb()

# def reset():
#     file = open(BACKUP_FILE)
#     backup = json.load(backup)
#     DATA["color"] = backup["colors"]
#     DATA["wallpaper"]["current"] = backup["wallpaper"]
#     reload()
#     return json.dumps({"success": True, "message": "colors has been update"})

# def getWallpaperColors(wallpaperId):
#     img = os.path.join(WALLPAPER_DIR, wallpaperId)
# shutil.copy(os.path.join(CACHE_DIR,"colors.json"),BACKUP_FILE)

#     return json.dumps(pywal.colors.get(img))

