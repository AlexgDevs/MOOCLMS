from fastapi import FastAPI
from .db import db_manager
from .routers import auth_app, user_app

app = FastAPI()
app.include_router(auth_app)
app.include_router(user_app)