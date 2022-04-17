import os
from flask_restful import Api, Resource
from .settings import CACHE_DIR,WALLPAPER_DIR,MODULE_DIR,BACKUP_FILE,DATA

class themeRoutes(Resource):
    def get(self):
        dark_themes = os.listdir(os.path.join(MODULE_DIR, "colorschemes", "dark"))
        dark_themes  = [theme.split('.')[0] for theme in dark_themes]
        light_themes = os.listdir(os.path.join(MODULE_DIR, "colorschemes", "light"))
        light_themes  = [theme.split('.')[0] for theme in light_themes]
        return { "dark": dark_themes, "light": light_themes }
    def post(self):
        theme = request.get_json()
        option = "" if theme['dark'] else "-l"
        command = "wal -q " + option + " --theme " + theme['name']
        os.system(command)  
        newData = pywal.colors.file(os.path.join(CACHE_DIR,"colors.json"))
        DATA["color"] = newData["colors"]
        DATA["wallpaper"]["current"] = newData["wallpaper"]
        reload()
        return {"success": True, "message": "colors has been update"}

