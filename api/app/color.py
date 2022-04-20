import os
import pywal
from flask import request
from flask_restful import Api, Resource
from .data import WAL,COLOR,update_color
from .action import reload

class colorRoutes(Resource):
    def get(self):
        update_color()
        return COLOR
    def post(self):
        COLOR = request.get_json()
        reload()
        return {"success": True, "message": "colors has been update"}

