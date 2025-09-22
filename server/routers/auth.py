from fastapi import APIRouter, status, Response, Depends, Request
from passlib.context import CryptContext
from sqlalchemy import select

from ..schemas import (
    RegisterUser,
    LoginUser
)

from ..db import db_manager, User
from ..utils import JWTConfig, CustomExeptions

auth_app = APIRouter(prefix='/auth', tags=['Auth'])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@auth_app.post('/register',
            status_code=status.HTTP_201_CREATED,
            summary='create user',
            description='endpoint for creating user')
async def create_user(
    response: Response, 
    user: RegisterUser, 
    session=Depends(db_manager.db_session_begin),
    logined = Depends(JWTConfig.not_auth_required)):

    user_data = user.model_dump()
    user_data['password'] = pwd_context.hash(user.password)
    new_user = User(**user_data)
    session.add(new_user)
    await session.flush()

    sub_data = {
        'id': new_user.id,
        'name': new_user.name,
        'role': new_user.role
    }

    access_token = await JWTConfig.create_access_token(sub_data)
    refresh_token = await JWTConfig.create_refresh_token(sub_data)
    await JWTConfig.set_custom_cookies(response, access_token, refresh_token)

    return {
        'message': 'created',
        'tokens': {
            'access': access_token,
            'refresh': refresh_token
        }
    }


@auth_app.post('/token',
            summary='login user',
            description='enpoind for etrens in account')
async def get_token(
    response: Response, 
    user: LoginUser, 
    session=Depends(db_manager.db_session),
    logined = Depends(JWTConfig.not_auth_required)):

    user_output = await session.scalar(
        select(User)
        .where(User.name == user.name)
    )

    if not user_output:
        await CustomExeptions.user_not_found()

    if not pwd_context.verify(user.password, user_output.password):
        await CustomExeptions.invalid_password()

    sub_data = {
        'id': user_output.id,
        'name': user_output.name,
        'role': user_output.role
    }

    access_token = await JWTConfig.create_access_token(sub_data)
    refresh_token = await JWTConfig.create_refresh_token(sub_data)
    await JWTConfig.set_custom_cookies(response, access_token, refresh_token)

    return {
        'message': 'logined',
        'tokens': {
            'access': access_token,
            'refresh': refresh_token
        }
    }


@auth_app.get('/refresh',
            summary='refresh access token',
            description='endpoint for refreshing access token')
async def refresh(request: Request, response: Response):
    refresh_token = await request.cookies.get('refresh_token')
    if not refresh_token:
        await CustomExeptions.token_not_found()

    new_access_token = await JWTConfig.refresh_access_token(refresh_token)

    response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=3600,
            path="/",
        )
    
    return {'tokens': {
            'new_access_token': new_access_token}
        }


@auth_app.delete('/logout',
                summary='logout',
                description='enpoint for deleted tokens and logout as system')
async def logout(
    response: Response,
    user: dict = Depends(JWTConfig.auth_required),
):
    response.delete_cookie(
        key="access_token",
        path="/"
    )
    
    response.delete_cookie(
        key="refresh_token",
        path="/"
    )

    return {'status': 'tokens deleted'}