import os
import pywal
from flask import request
from flask_restful import Resource
from .data import WAL, COLOR, update_color

def reload():
    colors = []
    for color_name in COLOR:
        colors.append(COLOR[color_name])

    data = pywal.colors.colors_to_dict(colors, WAL["wallpaper"])
    pywal.export.every(data)
    pywal.sequences.send(data)
    pywal.reload.xrdb()

class colorRoutes(Resource):
    def get(self):
        update_color()
        return COLOR
    def put(self):
        COLOR.update(request.get_json())
        reload()
        return {"message": "colors has been update"}

