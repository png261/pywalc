import os
from flask_restful import Api, Resource
from .settings import CACHE_DIR,MODULE_DIR,DATA

class themeRoutes(Resource):
    def get(self):
        return DATA["theme"]["list"]
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

