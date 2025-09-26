from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from ..utils import CustomExeptions
from ..db import db_manager, Course, Lesson, Module, RecordCourse
from ..schemas import (
    DetailCourseResponse, 
    CourseResponse, 
    CreateCourse
)

course_app = APIRouter(prefix='/courses', tags=['Courses'])


@course_app.get('/',
                response_model=List[CourseResponse],
                summary='get all courses info',
                description='ebpoint for getting all info courses')
async def all_courses_info(session=Depends(db_manager.db_session)):
    courses = await session.scalars(
        select(Course)
    )

    return courses.all()


@course_app.get('/{course_id}',
                response_model=CourseResponse,
                summary='get info course',
                description='endpoint for getting info course')
async def course_info(course_id: int, session=Depends(db_manager.db_session)):
    course = await session.scalar(
        select(Course)
        .where(Course.id == course_id)
    )

    if not course:
        await CustomExeptions.course_not_found()

    return course


@course_app.get('/detail/{course_id}/{user_id}',
                response_model=DetailCourseResponse,
                summary='get detail info course',
                description='endpoint for getting detailing info course')
async def detail_course_info(
    course_id: int,
    user_id: int,
    session=Depends(db_manager.db_session)):

    # record = await session.scalar(
    #     select(
    #         RecordCourse
    #     )
    #     .where(RecordCourse.user_id == user_id, RecordCourse.course_id == course_id)
    # )

    # if record:
    course = await session.scalar(
        select(Course)
        .options(
            selectinload(Course.modules).selectinload(Module.lessons),
            selectinload(Course.record_users)
        )
        .where(Course.id == course_id)
    )

    if not course:
        await CustomExeptions.course_not_found()

    # else:
    #     await CustomExeptions.course_not_found()

    return course


@course_app.post('/',
                status_code=status.HTTP_201_CREATED,
                summary='create course',
                description='endpoint for creating courses')
async def create_course(
        course_data: CreateCourse,
        session=Depends(db_manager.db_session_begin)):

    session.add(Course(**course_data.model_dump()))
    return {'status': 'course created'}


@course_app.delete('/{course_id}/{user_id}',
                summary='delete course',
                description='enpoind for deleting course')
async def delete_course(
    course_id: int,
    user_id: int,
    session=Depends(db_manager.db_session_begin)):

    course = await session.scalar(
        select(Course)
        .where(Course.id == course_id, Course.creator_id == user_id)
    )

    if not course:
        await CustomExeptions.course_not_found()

    await session.delete(course)
    return {'status': 'course deleted'}