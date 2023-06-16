import multiprocessing
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from uvicorn import run

from pycloudflared import try_cloudflare

from .settings import CACHE_DIR, SERVER_URL_TXT
from .colors import colorRouter
from .theme import themeRouter
from .wallpaper import wallpaperRouter
from .system import systemRouter
from . import util

class Server:
    def __init__(self):
        self.port=2004
        self.server_url = ""
        self.process = None

        self.server = FastAPI(title="Pwy",
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
                      docs_url="/")

        self.server.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.server.mount("/static", StaticFiles(directory=CACHE_DIR), name="static")
        self.server.include_router(colorRouter)
        self.server.include_router(themeRouter)
        self.server.include_router(wallpaperRouter)
        self.server.include_router(systemRouter)


    def run(self):
        self._start_cloudfare_tunnel()
        util.save_file(self.server_url, SERVER_URL_TXT)
        
        self._start_localhost()

    def _start_localhost(self):
        run(self.server, host="127.0.0.1", port=self.port)

    def _start_cloudfare_tunnel(self):
        self.server_url = try_cloudflare(port=self.port).tunnel

    def stop(self):
        print("todo: stop")

    def getUrl(self):
        return util.read_file(SERVER_URL_TXT)
