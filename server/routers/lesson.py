from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy import select

from ..db import db_manager, Lesson
from ..schemas import CreateLesson, LessonResponse
from ..utils import CustomExeptions

lesson_app = APIRouter(prefix='/lessons', tags=['Lessons'])


@lesson_app.get('/',
                response_model=List[LessonResponse],
                summary='get all lessons info',
                description='endpoin for getting all info by lessons')
async def all_lessons_info(
    session = Depends(db_manager.db_session)
    ):

    lessons = await session.scalars(
        select(Lesson)
    )

    return lessons


@lesson_app.post('/',
                status_code=status.HTTP_201_CREATED,
                summary='create lesson',
                description='endpoint for creating lesson for module')
async def create_lesson(
    lesson_data: CreateLesson, 
    session = Depends(db_manager.db_session_begin)):

    session.add(Lesson(**lesson_data.model_dump(exclude_unset=True)))
    return {'status': 'lesson created'}


@lesson_app.delete('/{lesson_id}',
                summary='delete lesson',
                description='endpoint for deleting lesson')
async def delete_lesson(
    lesson_id: int,
    session = Depends(db_manager.db_session_begin)
    ):

    lesson = await session.scalar(
        select(Lesson)
        .where(Lesson.id == lesson_id)
    )

    if not lesson:
        await CustomExeptions.lesson_not_found()

    await session.delete(lesson)
    return {'status': 'lesson deleted'}