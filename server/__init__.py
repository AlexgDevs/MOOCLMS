from os import getenv
from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from .db import db_manager
from .routers import (
    auth_app, 
    user_app, 
    course_app, 
    module_app, 
    lesson_app,
    payment_app
)

load_dotenv()

API_URL = 'http://localhost:8000'

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[getenv('CLIENT_URL')],
    allow_credentials=True,  
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_app)
app.include_router(user_app)
app.include_router(course_app)
app.include_router(lesson_app)
app.include_router(module_app)
app.include_router(payment_app)


from .tests import (
    test_integrations
)