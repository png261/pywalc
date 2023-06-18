import os
import socket

from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import List
from uvicorn import run
from pycloudflared import try_cloudflare

from .settings import CACHE_DIR, MODULE_DIR, OS
from .colors import Color
from .theme import Theme
from .wallpaper import Wallpaper
from . import util


class Server:
    def __init__(self, port):
        self.port = port
        self.wallpaper = Wallpaper()
        self.theme = Theme()
        self.color = Color()
        self.server = FastAPI(
            title="Pywalc",
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
            docs_url="/api",
        )

        self.server.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.server.mount("/cache", StaticFiles(directory=CACHE_DIR), name="cache")
        self.server.mount(
            "/static",
            StaticFiles(directory=os.path.join(MODULE_DIR, "static")),
            name="static",
        )

        self.templates = Jinja2Templates(
            directory=os.path.join(MODULE_DIR, "templates")
        )

        self._setup_routes()

    def _setup_routes(self):
        @self.server.get("/", response_class=HTMLResponse)
        async def home_page(request: Request):
            return self.templates.TemplateResponse("index.html", {"request": request})

        @self.server.get("/wallpaper", tags=["wallpaper"])
        def get_wallpapers():
            return self.wallpaper.get()

        @self.server.put("/wallpaper/{id}", tags=["wallpaper"])
        def set_wallpaper(id: str):
            return self.wallpaper.set(id)

        @self.server.get("/wallpaper/{id}/color", tags=["wallpaper"])
        def get_wallpaper_colors(id):
            return self.wallpaper.get_colors(id)

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
        def get_system_info():
            return {"os": OS, "name": socket.gethostname()}

        @self.server.get("/reset", tags=["system"])
        def reset():
            self.color.reset()
            self.wallpaper.reset()

    def _start_localhost(self):
        print(" * Localhost: http://127.0.0.1:{port}".format(port=self.port))
        run(self.server, host="127.0.0.1", port=self.port, log_level="error")

    def _start_cloudfare_tunnel(self):
        self.online_site = try_cloudflare(port=self.port, verbose=False).tunnel
        print(" * Online: {url}".format(url=self.online_site))
        util.show_ascii_qrcode(self.online_site)

    def run(self):
        self._start_cloudfare_tunnel()
        self._start_localhost()
