import pywal
import json
import os
from app import app,api
from flask_restful import Resource
import shutil 

from .settings import CACHE_DIR,WALLPAPER_DIR,BACKUP_FILE,DATA
from app.theme import themeRoutes
from app.wallpaper import wallpaperRoutes
from app.color import colorRoutes
from app.sysinfo import sysRoutes


shutil.copy(os.path.join(CACHE_DIR,"colors.json"),BACKUP_FILE)

@app.route("/all", methods=["GET"])
def getall():
    return json.dumps(DATA)

@app.route("/reset", methods=["GET"])
def reset():
    file = open(BACKUP_FILE)
    backup = json.load(backup)
    DATA["color"] = backup["colors"]
    DATA["wallpaper"]["current"] = backup["wallpaper"]
    reload()
    return json.dumps({"success": True, "message": "colors has been update"})

@app.route("/color/wallpaper/<wallpaperId>", methods=["GET"])
def getWallpaperColors(wallpaperId):
    img = os.path.join(WALLPAPER_DIR, wallpaperId)
    return json.dumps(pywal.colors.get(img))

api.add_resource(wallpaperRoutes, '/wallpaper', '/wallpaper/<string:id>')
api.add_resource(themeRoutes, '/theme')
api.add_resource(colorRoutes, '/color')
api.add_resource(sysRoutes, '/sys')

