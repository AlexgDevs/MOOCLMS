from fastapi import FastAPI
from .db import db_manager
from .routers import (
    auth_app, 
    user_app, 
    course_app, 
    module_app, 
    lesson_app
)

API_URL = 'http://localhost:8000'

app = FastAPI()
app.include_router(auth_app)
app.include_router(user_app)
app.include_router(course_app)
app.include_router(lesson_app)
app.include_router(module_app)


from .tests import (
    test_integrations
)