import os
import pywal

from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

from wallpaper import *
from theme import *
from color import *
from sys import *

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
