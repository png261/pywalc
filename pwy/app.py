from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .settings import CACHE_DIR
from .colors import colorRouter
from .theme import themeRouter
from .wallpaper import wallpaperRouter
from .system import systemRouter

server = FastAPI(title="Pwy",
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

server.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

server.mount("/static", StaticFiles(directory=CACHE_DIR), name="static")
server.include_router(colorRouter)
server.include_router(themeRouter)
server.include_router(wallpaperRouter)
server.include_router(systemRouter)
