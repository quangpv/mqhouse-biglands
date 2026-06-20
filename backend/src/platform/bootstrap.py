import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.platform.config import settings


def module(app: FastAPI):
    os.makedirs(settings.upload_dir, exist_ok=True)
    os.makedirs(settings.log_dir, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")
