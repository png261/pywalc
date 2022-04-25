import socket
from settings import OS 
from app import app
from settings import WAL
from color import COLOR
from wallpaper import WALLPAPER

@app.get("/reload", tags=["system"])
def load_changes():
    colors = []
    for color_name in COLOR:
        colors.append(COLOR[color_name])

    data = pywal.colors.colors_to_dict(colors, WAL["wallpaper"])
    pywal.export.every(data)
    pywal.sequences.send(data)
    pywal.reload.xrdb()

@app.get("/sys",tags=["system"])
def get_system_info():
    name=socket.gethostname() 
    return { "os":OS, "name":name }
