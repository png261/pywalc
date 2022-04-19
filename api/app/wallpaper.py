import os
import pywal
import uuid
from flask import request
from flask_restful import Api, Resource
from .settings import CACHE_DIR,DATA

class wallpaperRoutes(Resource):
    def get(self):
        return DATA["wallpaper"]["list"]
    def put(self):
        wallpaper = request.get_json()
        path = os.path.join(WALLPAPER_DIR, wallpaper)
        image = pywal.image.get(path)
        pywal.wallpaper.change(image)
        return wallpaper
    def post(self):
        print("upload")
        files = request.files.getlist("images")
        newUrl = []
        for file in files:
            filename = str(uuid.uuid4())
            path = os.path.join(WALLPAPER_DIR,filename)
            file.save(path)
            newUrl.append(filename)
        DATA["wallpaper"]["list"]
        return {"success": True, "newUrl": newUrl}
    def delete(self,id):
        path=os.path.join(WALLPAPER_DIR, id)
        os.remove(path)
        return {"success": True, "message": "img has been removed"}

