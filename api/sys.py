import os
import socket
from settings import WALLPAPER_DIR, OS 
from app import app

@app.get("/sys")
def get_sysinfo():
    name = socket.gethostname() 
    return { "os":OS, "name":name }
