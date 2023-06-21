"""
Server
"""

import os
import socket

from typing import List
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from uvicorn import run
from pycloudflared import try_cloudflare

from .settings import CACHE_DIR, MODULE_DIR, OS
from .colors import Color
from .theme import Theme
from .wallpaper import Wallpaper
from . import util


class Server:
    """Server"""

    def __init__(self, port):
        """Initialize server"""
        self.port = port
        self.wallpaper = Wallpaper()
        self.theme = Theme()
        self.color = Color()
        self.online_site = None

    def setup(self):
        """Setup server"""
        self._setup_api()
        self._setup_routes()

    def _setup_api(self):
        """Setup FastAPI"""
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

        self.server.mount(
            "/cache", StaticFiles(directory=CACHE_DIR), name="cache"
        )
        self.server.mount(
            "/static",
            StaticFiles(directory=os.path.join(MODULE_DIR, "static")),
            name="static",
        )

        self.templates = Jinja2Templates(
            directory=os.path.join(MODULE_DIR, "templates")
        )

    def _setup_routes(self):
        """Set FastAPI routes"""

        @self.server.get("/", response_class=HTMLResponse)
        async def home_page(request: Request):
            return self.templates.TemplateResponse(
                "index.html", {"request": request}
            )

        @self.server.get("/wallpaper", tags=["wallpaper"])
        def get_wallpapers():
            return self.wallpaper.get()

        @self.server.put("/wallpaper/{wallpaper_id}", tags=["wallpaper"])
        def set_wallpaper(wallpaper_id: str):
            return self.wallpaper.set(wallpaper_id)

        @self.server.get("/wallpaper/{wallpaper_id}/color", tags=["wallpaper"])
        def get_wallpaper_colors(wallpaper_id):
            return self.wallpaper.get_colors(wallpaper_id)

        @self.server.post("/wallpaper", tags=["wallpaper"])
        async def upload_wallpapers(files: List[UploadFile] = File(...)):
            return await self.wallpaper.upload(files)

        @self.server.get("/wallpaper/apply", tags=["wallpaper"])
        def apply_wallpaper():
            return self.wallpaper.apply()

        @self.server.get("/color", tags=["color"])
        def get_colors():
            return self.color.get()

        @self.server.put("/color", tags=["color"])
        async def update_color(colors: Request):
            return await self.color.update(colors)

        @self.server.get("/color/apply", tags=["color"])
        def apply_color():
            return self.color.apply(self.wallpaper.get_current())

        @self.server.get("/theme", tags=["theme"])
        def get_themes():
            return self.theme.get()

        @self.server.get("/theme/{category}/{name}", tags=["theme"])
        def get_theme_color(category, name):
            return self.theme.get_color(category, name)

        @self.server.get("/sys", tags=["system"])
        def get_system_info():
            return {"os": OS, "name": socket.gethostname()}

        @self.server.get("/reset", tags=["system"])
        def reset():
            self.color.reset()
            self.wallpaper.reset()

    def _start_localhost(self):
        """Start FastAPI localhost server"""
        print(f" * Localhost: http://127.0.0.1:{self.port}")
        run(self.server, host="127.0.0.1", port=self.port, log_level="error")

    def _start_cloudflare_tunnel(self):
        """Start Cloudflare tunnel"""
        self.online_site = try_cloudflare(port=self.port, verbose=False).tunnel
        self._show_cloudfare_tunnel_url()

    def _show_cloudfare_tunnel_url(self):
        """Display the online URL with QR code"""
        print(f" * Online: {self.online_site}")
        util.show_ascii_qrcode(self.online_site)

    def run(self):
        """Run server"""
        self._start_cloudflare_tunnel()
        self._start_localhost()
