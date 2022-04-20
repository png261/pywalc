import os
import pywal
import uuid
from flask import request
from flask_restful import Api, Resource
from .settings import CACHE_DIR,WALLPAPER_DIR
from .data import WAL, COLOR, WALLPAPER, THEME, update_wall


class wallpaperRoutes(Resource):
    def get(self):
        update_wall()
        return WALLPAPER
    def put(self):
        id = request.get_json()
        image = pywal.image.get(os.path.join(WALLPAPER_DIR, id))
        pywal.wallpaper.change(image)
        WALLPAPER["current"] = id;
        return {"success": True, "message": "img has been removed"}

    def post(self):
        files = request.files.getlist("images")
        newUrl = []
        for file in files:
            filename = str(uuid.uuid4())
            path = os.path.join(WALLPAPER_DIR,filename)
            file.save(path)
            newUrl.append(filename)
        update_wall()
        return {"success": True, "newUrl": newUrl}

    def delete(self,id):
        os.remove(os.path.join(WALLPAPER_DIR, id))
        update_wall()
        return {"success": True, "message": "img has been removed"}

