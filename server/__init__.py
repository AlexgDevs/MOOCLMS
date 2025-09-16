from fastapi import FastAPI
from .db import db_manager
from .routers import auth_app

app = FastAPI()
app.include_router(auth_app)
