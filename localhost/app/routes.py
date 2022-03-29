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
    light_themes = os.listdir(os.path.join(MODULE_DIR, "colorschemes", "light"))
    return json.dumps(
        {
            "dark":dark_themes,
            "light":light_themes
        }
    ) 


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


# @app.route('/colors',methods = ['GET'])
# def getColors():
#     info = pywal.colors.file("/home/png/.cache/wal/colors.json")
#     return json.dumps(info["colors"])

# @app.route('/wallpaper',methods = ['GET'])
# def getWallpaper():
#     info = pywal.colors.file("/home/png/.cache/wal/colors.json")
#     return json.dumps(info["wallpaper"])

# @app.route('/specials',methods = ['GET'])
# def getSpecial():
#     info = pywal.colors.file("/home/png/.cache/wal/colors.json")
#     return json.dumps(info["special"])
