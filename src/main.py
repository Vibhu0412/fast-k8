# src/main.py

from fastapi import FastAPI
from src.fastapi_admin import app as admin_app

from src.router import book_router

app = FastAPI()

app.include_router(book_router)
app.mount("/admin", admin_app)
__all__ = ["app"]
