import stripe as stp

from os import getenv
from math import ceil

from typing import List
from fastapi import APIRouter, Depends, Request, status, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import selectinload, joinedload
from dotenv import load_dotenv

from ..utils import CustomExeptions
from ..db import db_manager, Course, Lesson, Module, RecordCourse
from ..schemas import (
    DetailCourseResponse, 
    CourseResponse, 
    CreateCourse,
    EnrollUser,
    OrderResponse
)

payment_app = APIRouter(prefix='/payments', tags=['Payments'])


load_dotenv()

STRIP_SECRET_KEY = getenv('STRIP_SECRET_KEY')

stp.api_key = STRIP_SECRET_KEY

@payment_app.post('/order/{course_id}/{user_id}',
                status_code=status.HTTP_201_CREATED,
                summary='buy course')
async def payment_ycs(course_id: int, user_id: int, order: OrderResponse, session = Depends(db_manager.db_session_begin)):
    record = await session.scalar(
        select(RecordCourse)
        .where(RecordCourse.user_id == user_id, RecordCourse.course_id == course_id)
    )

    if not record:
        session.add(RecordCourse(
            user_id=user_id,
            course_id=course_id
        ))
        return {'status': 'purchased'}

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail='the course has already been purchased'
    )