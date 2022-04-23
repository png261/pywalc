import os
import pywal
from data import WALLPAPER,update_wall
from settings import WALLPAPER_DIR,OS 

from app import app

def save(files):
    newUrl = []
    for file in files:
        filename = str(uuid.uuid4())
        path = os.path.join(WALLPAPER_DIR,filename)
        file.save(path)
        newUrl.append(filename)
    return newUrl

@app.get("/wallpaper")
def get_wallpapers():
    update_wall()
    return WALLPAPER

@app.put("/wallpaper")
def set_wallpaper():
    image = pywal.image.get(os.path.join(WALLPAPER_DIR, id))
    pywal.wallpaper.change(image)
    WALLPAPER["current"] = id

@app.post("/wallpaper")
def add_wallpaper():
    files = request.files.getlist("images")
    newUrl = save(files)
    update_wall()
    return {"success": True, "newUrl": newUrl}

@app.delete("/wallpaper")
def delete_wallpaper():
    os.remove(os.path.join(WALLPAPER_DIR, id))
    update_wall()
