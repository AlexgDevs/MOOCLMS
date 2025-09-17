from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from ..utils import CustomExeptions
from ..schemas import UserResponse, DetailUserResponse
from ..db import db_manager, User

user_app = APIRouter(prefix='/users', tags=['Users'])


@user_app.get('/',
            response_model=List[UserResponse],
            summary='get all users',
            description='endpoint for getting all users')
async def all_users_info(
        session=Depends(db_manager.db_session)):
    users = await session.scalars(
        select(User)
    )

    return users.all()


@user_app.get('/{user_id}',
            response_model=UserResponse,
            summary='get user info',
            description='endpoint for getting one user info')
async def user_info(
        user_id: int,
        session=Depends(db_manager.db_session)):
    user = await session.scalar(
        select(User)
        .where(User.id == user_id)
    )

    if not user:
        await CustomExeptions.user_not_found()

    return user


@user_app.get('/detail/{user_id}',
            response_model=DetailUserResponse,
            summary='get detail user',
            description='endpoint for getting detail info user for admin')
async def detail_user_info(
    user_id: int,
    session=Depends(db_manager.db_session)):

    user = await session.scalar(
        select(User)
        .options(
            selectinload(User.created_courses),
            selectinload(User.created_modules),
            selectinload(User.created_lessons)
        )
        .where(User.id == user_id)
    )

    if not user:
        await CustomExeptions.user_not_found()

    return user
