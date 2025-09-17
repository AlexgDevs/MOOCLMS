from fastapi import APIRouter, Depends, status

from ..db import db_manager, Lesson
from ..schemas import CreateLesson

lesson_app = APIRouter(prefix='/lessons', tags=['Lessons'])


@lesson_app.post('/',
                status_code=status.HTTP_201_CREATED,
                summary='create lesson',
                description='endpoint for creating lesson for module')
async def create_lesson(
    lesson_data: CreateLesson, 
    session = Depends(db_manager.db_session_begin)):

    session.add(Lesson(**lesson_data.model_dump(exclude_unset=True)))
    return {'status': 'lesson created'}