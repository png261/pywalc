import socket
from settings import OS 
from app import app

@app.get("/sys")
def get_colors():
    name=socket.gethostname() 
    return { "os":OS, "name":name }
