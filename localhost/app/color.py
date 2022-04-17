import os
from flask_restful import Api, Resource
from .settings import CACHE_DIR,WALLPAPER_DIR,MODULE_DIR,BACKUP_FILE,DATA

class colorRoutes(Resource):
    def get(self):
        return DATA["color"]
    def post(self):
        if request.method == "POST":
            DATA['color'] = request.get_json()
            reload(data)
            return {"success": True, "message": "colors has been update"}

