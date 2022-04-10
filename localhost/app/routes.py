import pywal
import json
import os
from app import app
from flask import render_template
from flask import request
import shutil

HOME = pywal.settings.HOME
CACHE_DIR =pywal.settings.CACHE_DIR
MODULE_DIR =pywal.settings.MODULE_DIR
CONF_DIR = pywal.settings.CONF_DIR

shutil.copy(os.path.join(CACHE_DIR,"colors.json"), "backup.json")

def updateColor(colors):
    pywal.export.every(colors)
    pywal.sequences.send(colors)
    pywal.reload.xrdb()


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/theme",methods=["GET"])
def theme():
    dark_themes = os.listdir(os.path.join(MODULE_DIR, "colorschemes", "dark"))
    dark_themes  = [theme.split('.')[0] for theme in dark_themes]

    light_themes = os.listdir(os.path.join(MODULE_DIR, "colorschemes", "light"))
    light_themes  = [theme.split('.')[0] for theme in light_themes]

    return json.dumps(
        {
            "dark":dark_themes,
            "light":light_themes
        }
    ) 

@app.route("/theme",methods=["POST"])
def changeTheme():
    theme = json.loads(request.data)
    os.system("wal --theme " + theme)  
    colors = pywal.colors.file(os.path.join(CACHE_DIR,"colors.json"))
    updateColor(colors)
    return json.dumps({"sucess": True, "message": "colors has been update"})


@app.route("/all", methods=["GET"])
def getAll():
    info = pywal.colors.file(os.path.join(CACHE_DIR,"colors.json"))
    return json.dumps(info)

@app.route("/color", methods=[ "POST"])
def changeColor():
    if request.method == "POST":
        colors = json.loads(request.data)
        updateColor(colors)

        return json.dumps({"sucess": True, "message": "colors has been update"})


@app.route("/reset", methods=["GET"])
def reset():
    backup = open("backup.json")
    colors = json.load(backup)

    updateColor(colors)
    return json.dumps({"sucess": True, "message": "colors has been update"})


@app.route("/wallpaper", methods=["GET"])
def getWallpaper():
    wallpapers = os.listdir("./app/static/wallpapers")
    return json.dumps(wallpapers)


@app.route("/wallpaper", methods=["POST"])
def changeWallpaper():
    wallpaper = json.loads(request.data)
    path = os.path.join("./app/static/wallpapers", wallpaper)
    print(path)
    image = pywal.image.get(path)
    print(image)
    pywal.wallpaper.change(image)

    return json.dumps(wallpaper)

