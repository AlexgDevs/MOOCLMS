from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload

from ..utils import CustomExeptions
from ..db import db_manager, Course, Lesson, Module, RecordCourse
from ..schemas import (
    DetailCourseResponse, 
    CourseResponse, 
    CreateCourse,
    EnrollUser
)

course_app = APIRouter(prefix='/courses', tags=['Courses'])


@course_app.get('/',
                response_model=List[CourseResponse],
                summary='get all courses info',
                description='ebpoint for getting all info courses')
async def all_courses_info(
    session=Depends(db_manager.db_session)):
    courses = await session.scalars(
        select(Course)
        .options(
            selectinload(Course.record_users).selectinload(RecordCourse.user)
        )
    )

    return courses.all()


@course_app.get('/{user_id}/all',
                response_model=List[CourseResponse],
                summary='get all courses info by user_id',
                description='endpoint for getting all courses by user where the current user is not registered')
async def all_courses_info(
    user_id: int,
    session=Depends(db_manager.db_session)):
    
    subquery = select(RecordCourse.course_id).where(
        RecordCourse.user_id == user_id
    ).scalar_subquery()
    
    courses = await session.scalars(
        select(Course)
        .options(
            selectinload(Course.record_users).selectinload(RecordCourse.user)
        )
        .where(Course.id.not_in(subquery))
    )
    
    return courses.all()


@course_app.get('/{course_id}/{user_id}',
                response_model=CourseResponse,
                summary='get info course',
                description='endpoint for getting info course')
async def course_info(course_id: int, user_id: int, session=Depends(db_manager.db_session)):

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
            selectinload(Course.record_users).selectinload(RecordCourse.user)
        )
        .where(Course.id == course_id)
    )

    # else:
    #     await CustomExeptions.course_not_found()

    if not course:
        await CustomExeptions.course_not_found()

    return course


@course_app.post('/{course_id}/enroll',
                status_code=status.HTTP_201_CREATED)
async def enroll_on_course(
    course_id: int, 
    user: EnrollUser,
    session = Depends(db_manager.db_session_begin)):

    record = await session.scalar(
        select(RecordCourse)
        .where(RecordCourse.course_id == course_id, RecordCourse.user_id == user.user_id)
    )

    if record:
        raise HTTPException(
            status_code=400,
            detail='enrolled'
        )

    session.add(RecordCourse(course_id=course_id, user_id=user.user_id))
    return {'status', 'enrolled'}


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
            selectinload(Course.record_users).selectinload(RecordCourse.user)
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

    session.add(Course(**course_data.model_dump(exclude_unset=True)))
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