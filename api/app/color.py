import os
import pywal
from flask import request
from flask_restful import Resource
from .data import WAL, COLOR, update_color

class colorRoutes(Resource):
    def get(self):
        update_color()
        return COLOR
    def put(self):
        COLOR = request.get_json()
        data = pywal.colors.colors_to_dict(COLOR, WAL["wallpaper"])
        pywal.export.every(data)
        pywal.sequences.send(data)
        pywal.reload.xrdb()
        return {"colors has been update"}

