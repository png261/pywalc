import os
import pywal
from data import THEME
from app import app

@app.get("/theme")
def get_themes():
    return THEME

@app.put("/theme")
def set_theme():
    data = Request.get_json()
    THEME["isDark"] = data["isDark"]
    option = "" if THEME['isDark'] else "-l"
    os.system("wal -q " + option + " --theme " + data['name'])  
    update_color() 
