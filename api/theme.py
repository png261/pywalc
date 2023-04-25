import os
import json
import pywal
from fastapi import APIRouter
from settings import MODULE_DIR

dark_themes = [
    theme.name.replace(".json", "") for theme in pywal.theme.list_themes()
]
light_themes = [
    theme.name.replace(".json", "")
    for theme in pywal.theme.list_themes(dark=False)
]

THEME = {"dark": dark_themes, "light": light_themes}


themeRouter = APIRouter()


@themeRouter.get("/theme", tags=["theme"])
def get_themes():
    return THEME


@themeRouter.get("/theme/{category}/{name}", tags=["theme"])
def set_theme(name, category):
    themes_path = os.path.join(
        MODULE_DIR, "colorschemes", category, name + ".json"
    )
    with open(themes_path) as file:
        themes = json.loads(file.read())
    return themes["colors"]
