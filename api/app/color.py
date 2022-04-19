import os
import pywal
from flask import request
from flask_restful import Api, Resource
from .settings import WALLPAPER_DIR,DATA

def reload():
    colors = DATA["color"]
    wallpaper = DATA["wallpaper"]["current"]
    img_path = os.path.join(WALLPAPER_DIR, wallpaper)

    data = pywal.colors.colors_to_dict(colors,img_path)
    pywal.export.every(data)
    pywal.sequences.send(data)
    pywal.reload.xrdb()

class colorRoutes(Resource):
    def get(self):
        return DATA["color"]
    def post(self):
        if request.method == "POST":
            DATA['color'] = request.get_json()
            reload()
            return {"success": True, "message": "colors has been update"}

