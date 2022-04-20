from app import app,api
from flask_restful import Resource
from app.theme import themeRoutes
from app.wallpaper import wallpaperRoutes
from app.color import colorRoutes
from app.sysinfo import sysRoutes

api.add_resource(wallpaperRoutes, '/wallpaper', '/wallpaper/<string:id>')
api.add_resource(themeRoutes, '/theme')
api.add_resource(colorRoutes, '/color')
api.add_resource(sysRoutes, '/sys')

