import pywal
from .settings import WAL
from fastapi import Request, APIRouter
from .wallpaper import WALLPAPER

COLOR = WAL["colors"]

colorRouter = APIRouter()


@colorRouter.get("/color", tags=["color"])
def get_colors():
    return COLOR


@colorRouter.put("/color", tags=["color"])
async def set_color(colors: Request):
    COLOR.update(await colors.json())
    return COLOR


@colorRouter.get("/color/load", tags=["color"])
def load_colors():
    colors = [COLOR[name] for name in COLOR]
    data = pywal.colors.colors_to_dict(colors, WALLPAPER["current"])
    pywal.export.every(data)
    pywal.sequences.send(data)
    pywal.reload.env()
    return COLOR
