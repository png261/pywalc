import os
import pywal

from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from settings import DATA_DIR

import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static" , StaticFiles(directory=DATA_DIR), name="static")

from wallpaper import *
from theme import *
from color import *
from sysinfo import *

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8080,log_level="info", reload=True)
