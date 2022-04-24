import os
import pywal
from data import COLOR,update_color
from settings import WALLPAPER_DIR,OS 
from fastapi import Request
from data import WAL

from app import app

def reload():
    colors = []
    for color_name in COLOR:
        colors.append(COLOR[color_name])

    data = pywal.colors.colors_to_dict(colors, WAL["wallpaper"])
    pywal.export.every(data)
    pywal.sequences.send(data)
    pywal.reload.xrdb()

@app.get("/color")
def get_colors():
    update_color()
    return COLOR

@app.put("/color")
async def set_color(request: Request):
    colors = await request.json()
    COLOR.update(colors)
    reload()
