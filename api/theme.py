import os
import json
import pywal
from app import app
from fastapi import Request
from settings import MODULE_DIR

dark_themes = [theme.name.replace(".json", "")
               for theme in pywal.theme.list_themes()]
light_themes = [theme.name.replace(".json", "")
               for theme in pywal.theme.list_themes(dark=False)]
THEME = {
    "isDark": True,
    "dark": dark_themes,
    "light": light_themes
}

@app.get("/theme", tags=["theme"])
def get_themes():
    return THEME

@app.put("/theme", tags=["theme"])
async def set_theme(request: Request):
    data = await request.json()
    THEME["isDark"] = data["theme"]
    dark = "dark" if data["isDark"] else "light"
    file = open (os.path.join(MODULE_DIR, "colorschemes", dark, data["theme"] + ".json"), "r")
    theme_file = json.loads(file.read())
    return theme_file["colors"]
