import os
import pywal
from flask_restful import Api, Resource
from .settings import CACHE_DIR,MODULE_DIR
from .data import THEME, COLOR, WALLPAPER
from .action import reload

class themeRoutes(Resource):
    def get(self):
        return THEME
    def put(self):
        theme = request.get_json()
        option = "" if theme['dark'] else "-l"
        os.system("wal -q " + option + " --theme " + theme['name'])  
        newData = pywal.colors.file(os.path.join(CACHE_DIR,"colors.json"))
        COLOR = newData["colors"]
        WALLPAPER["current"] = newData["wallpaper"]
        reload()
        return {"success": True, "message": "colors has been update"}

