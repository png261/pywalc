import os
import json
import pywal
from app import app
from settings import MODULE_DIR

dark_themes = [
    theme.name.replace(".json", "") for theme in pywal.theme.list_themes()
]
light_themes = [
    theme.name.replace(".json", "")
    for theme in pywal.theme.list_themes(dark=False)
]

THEME = {"dark": dark_themes, "light": light_themes}


@app.get("/theme", tags=["theme"])
def get_themes():
    return THEME


@app.get("/theme/{name}", tags=["theme"])
async def set_theme(name, dark=True):
    dark = "dark" if dark else "light"
    file = open(os.path.join(MODULE_DIR, "colorschemes", dark, name + ".json"),
                "r")
    theme_data = json.loads(file.read())
    return theme_data["colors"]
