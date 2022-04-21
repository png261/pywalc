import os
import pywal
from flask import request
from flask_restful import Resource
from .data import THEME, update_color

class themeRoutes(Resource):
    def get(self):
        return THEME
    def put(self):
        data = request.get_json()
        THEME["isDark"] = data["isDark"]
        option = "" if THEME['isDark'] else "-l"
        os.system("wal -q " + option + " --theme " + data['name'])  
        update_color() 
        return {"success": True, "message": "Theme has been set"}

