from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from settings import CACHE_DIR

import init
from color import colorRouter
from theme import themeRouter
from wallpaper import wallpaperRouter
from system import systemRouter

app = FastAPI(title="Pwy",
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init.setupFiles()

app.mount("/static", StaticFiles(directory=CACHE_DIR), name="static")
app.include_router(colorRouter)
app.include_router(themeRouter)
app.include_router(wallpaperRouter)
app.include_router(systemRouter)
