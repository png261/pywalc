import os
import socket
from flask_restful import Api, Resource
from .settings import CACHE_DIR,MODULE_DIR,DATA,OS

class sysRoutes(Resource):
    def get(self):
        name=socket.gethostname() 
        return { "os":OS, "name":name }
