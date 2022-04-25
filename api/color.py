import os
import pywal
from settings import WALLPAPER_DIR,OS, WAL, CACHE_DIR
from fastapi import Request
from app import app

COLOR = {}
def update_color():
    WAL = pywal.colors.file(os.path.join(CACHE_DIR,"colors.json"))
    COLOR.update(WAL["colors"])
update_color()

@app.get("/reload")
def reload():
    colors = []
    for color_name in COLOR:
        colors.append(COLOR[color_name])
    print(colors)

    data = pywal.colors.colors_to_dict(colors, WAL["wallpaper"])
    pywal.export.every(data)
    pywal.sequences.send(data)
    pywal.reload.xrdb()

update_color()
@app.get("/color",tags=["color"])
def get_colors():
    return COLOR

@app.put("/color",tags=["color"])
async def set_color(request: Request):
    colors = await request.json()
    COLOR.update(colors)
    print(COLOR)
