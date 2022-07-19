import pywal
from settings import WAL
from fastapi import Request
from app import app
from wallpaper import WALLPAPER

COLOR = WAL["colors"]


@app.get("/color", tags=["color"])
def get_colors():
    return COLOR


@app.put("/color", tags=["color"])
async def set_color(colors: Request):
    COLOR.update(await colors.json())
    return COLOR


@app.get("/color/load", tags=["color"])
def load_colors():
    colors = []
    for name in COLOR:
        colors.append(COLOR[name])
    data = pywal.colors.colors_to_dict(colors, WALLPAPER["current"])
    pywal.export.every(data)
    pywal.sequences.send(data)
    pywal.reload.env()
    return COLOR
