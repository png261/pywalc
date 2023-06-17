import os

from fastapi import FastAPI, Request
from fastapi import Request
from fastapi import File, UploadFile
from typing import List
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from uvicorn import run

from pycloudflared import try_cloudflare

from .settings import CACHE_DIR
from .colors import Color
from .theme import Theme
from .wallpaper import Wallpaper
from .system import System

class Server:
    def __init__(self):
        self.wallpaper = Wallpaper();
        self.color = Color();
        self.theme = Theme();
        self.system = System();

        self.api_url = None
        self.server = FastAPI(title="Pywalc",
                      description="Control your pywal",
                      contact={
                          "name": "Phuong Nguyen",
                          "url": "https://png261.github.io",
                          "email": "nhphuong.code@gmail.com",
                      },
                      openapi_tags=[
                          {
                              "name": "wallpaper",
                          },
                          {
                              "name": "theme",
                          },
                          {
                              "name": "color",
                          },
                          {
                              "name": "system",
                          },
                      ],
                      redoc_url=None,
                      docs_url="/api")

        self.server.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.server.mount("/cache", StaticFiles(directory=CACHE_DIR), name="cache")

        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
        self.server.mount("/static", StaticFiles(directory=static_dir), name="static")

        templates_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
        self.templates = Jinja2Templates(directory=templates_dir)

        self._setup_routes();

    def _setup_routes(self):
        @self.server.get("/", response_class=HTMLResponse)
        async def home_page(request: Request):
            return self.templates.TemplateResponse("index.html", {"request": request})

        @self.server.get("/wallpaper/{id}/color", tags=["wallpaper"])
        def get_wallpaper_colors(id):
            return self.wallpaper.get_colors(id)

        @self.server.get("/wallpaper", tags=["wallpaper"])
        def get_wallpapers():
            return self.wallpaper.get()

        @self.server.put("/wallpaper/{id}", tags=["wallpaper"])
        def set_wallpaper(id: str):
            return self.wallpaper.set(id)

        @self.server.post("/wallpaper", tags=["wallpaper"])
        async def upload_wallpaper(files: List[UploadFile] = File(...)):
            return await self.wallpaper.upload(files)

        @self.server.get("/wallpaper/load", tags=["wallpaper"])
        def load_wallpaper():
            return self.wallpaper.load()

        @self.server.get("/color", tags=["color"])
        def get_colors():
            return self.color.get()

        @self.server.put("/color", tags=["color"])
        async def update_color(colors: Request):
            return await self.color.update(colors)

        @self.server.get("/color/load", tags=["color"])
        def load_colors():
            return self.color.load(self.wallpaper.get_current())

        @self.server.get("/theme", tags=["theme"])
        def get_themes():
            return self.theme.get()

        @self.server.get("/theme/{category}/{name}", tags=["theme"])
        def set_theme(name, category):
            return self.theme.set(name, category)

        @self.server.get("/sys", tags=["system"])
        def system_get_info():
            return self.system.get()

        @self.server.get("/reset", tags=["system"])
        def system_reset():
            return self.system.reset(self.color, self. wallpaper)

    def _start_localhost(self):
        run(self.server, host='127.0.0.1', port=8080)

    def _start_cloudfare_tunnel(self):
        self.api_url = try_cloudflare(port=8080).tunnel

    def run(self):
        self._start_cloudfare_tunnel()
        self._start_localhost()
