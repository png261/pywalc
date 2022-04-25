import os
import uuid
from typing import List
import pywal
from settings import WALLPAPER_DIR,OS, WAL
from fastapi import Request, FastAPI, File, UploadFile
from app import app

WALLPAPER = {}
def update_wall():
    WALLPAPER.update({
        'current': WAL["wallpaper"],
        'list': os.listdir(WALLPAPER_DIR)
    })
update_wall()

@app.get("/wallpaper/{id}/color", tags=[ "wallpaper" ])
def get_wallpaper_colors(id):
    img = os.path.join(WALLPAPER_DIR, id)
    colors = pywal.colors.get(img)["colors"]
    return colors

@app.get("/wallpaper", tags=["wallpaper"])
def get_wallpapers():
    update_wall()
    return WALLPAPER

@app.put("/wallpaper/{id}", tags=[ "wallpaper" ])
def set_wallpaper(id:str):
    image = pywal.image.get(os.path.join(WALLPAPER_DIR, id))
    pywal.wallpaper.change(image)
    WALLPAPER["current"] = id

@app.post("/wallpaper", tags=[ "wallpaper" ])
async def upload(files: List[UploadFile] = File(...)):
    newUrl = []
    for file in files:
        content = await file.read()
        filename = str(uuid.uuid4())
        path = os.path.join(WALLPAPER_DIR,filename) 
        with open(path, 'wb') as f:
            f.write(content)
        newUrl.append(filename)
    return {"newUrl": newUrl}

@app.delete("/wallpaper/{id}",tags=[ "wallpaper" ])
def delete_wallpaper(id:str):
    os.remove(os.path.join(WALLPAPER_DIR, id))
    update_wall()
