import os
import uuid
from typing import List
import pywal
from data import WALLPAPER,update_wall
from settings import WALLPAPER_DIR,OS 
from fastapi import Request
from fastapi import FastAPI, File, UploadFile

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

@app.put("/wallpaper/{id}")
def set_wallpaper(id:str):
    image = pywal.image.get(os.path.join(WALLPAPER_DIR, id))
    pywal.wallpaper.change(image)
    WALLPAPER["current"] = id

def save_file(filename, data):
    with open(filename, 'wb') as f:
        f.write(data)

@app.post("/wallpaper")
async def upload(files: List[UploadFile] = File(...)):
    newUrl = []
    for file in files:
        contents = await file.read()
        filename = str(uuid.uuid4())
        save_file(os.path.join(WALLPAPER_DIR,filename), contents)
        newUrl.append(filename)
    return {"newUrl": newUrl}

@app.delete("/wallpaper/{id}")
def delete_wallpaper(id:str):
    os.remove(os.path.join(WALLPAPER_DIR, id))
    update_wall()
