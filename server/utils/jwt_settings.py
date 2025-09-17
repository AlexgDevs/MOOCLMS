from os import getenv
from datetime import (
    timedelta,
    datetime,
    timezone
)

from fastapi import (
    Request,
    Response
)


from jose import (
    jwt,
    JWTError,
)

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from .custom_exeptions import CustomExeptions

load_dotenv()

JWT_SECRET = getenv('JWT_SECRET')
ACCESS_EXPIRE = int(getenv('ACCESS_EXPIRE'))
REFRESH_EXPIRE = int(getenv('REFRESH_EXPIRE'))
ALGORITHM = getenv('ALGORITHM')


outh2_scheme = OAuth2PasswordBearer(tokenUrl='/token')


class JWTConfig:
    '''creating access token'''
    @staticmethod
    async def create_access_token(user_data: dict) -> str:
        exp = datetime.now(timezone.utc) + timedelta(hours=ACCESS_EXPIRE)
        return jwt.encode(
            {
                'sub': str(user_data.get('id')),
                'exp': exp,
                'user_data': user_data,
                'type': 'access'
            },
            JWT_SECRET,
            algorithm=ALGORITHM
        )

    '''creating refresh token'''
    @staticmethod
    async def create_refresh_token(user_data: dict) -> str:
        exp = datetime.now(timezone.utc) + timedelta(days=REFRESH_EXPIRE)
        return jwt.encode(
            {
                'sub': str(user_data.get('id')),
                'exp': exp,
                'user_data': user_data,
                'type': 'refresh'
            },
            JWT_SECRET,
            algorithm=ALGORITHM
        )

    '''creating access token by refresh'''
    @staticmethod
    async def refresh_access_token(token: str) -> str:
        try:
            if token:
                payload = jwt.decode(
                    token,
                    JWT_SECRET,
                    algorithms=[ALGORITHM]
                )

                if payload.get('type') != 'refresh':
                    await CustomExeptions.invalid_token_type()

                user_data = payload.get('user_data')
                return await JWTConfig.create_access_token(user_data)

            await CustomExeptions.token_not_found()

        except JWTError:
            await CustomExeptions.invalid_token()

    '''get user data'''
    @staticmethod
    async def current_user(request: Request, is_admin: bool = False):
        token = request.cookies.get('access_token')
        if token:
            try:
                payload = jwt.decode(
                    token,
                    JWT_SECRET,
                    algorithms=[ALGORITHM]
                )

                if payload.get('type') != 'access':
                    await CustomExeptions.invalid_token_type()

                if is_admin:
                    if payload.get('user_data').get('role') == 'admin':
                        return payload.get('user_data')
                    await CustomExeptions.you_not_admin()

                return payload.get('user_data')

            except JWTError:
                await CustomExeptions.invalid_token()

        await CustomExeptions.token_not_found()

    '''checked tokens'''
    @staticmethod
    async def is_token(request: Request):
        access_token = request.cookies.get('access_token')
        refresh_token = request.cookies.get('refresh_token')
        if access_token or refresh_token:
            await CustomExeptions.alredy_logined()

        pass

    '''
    Dependencies auth_required - made for users who already
    not_auth_required - for users who not already
    '''
    @staticmethod
    async def auth_required(request: Request):
        return await JWTConfig.current_user(request)

    @staticmethod
    async def not_auth_required(request: Request):
        return await JWTConfig.is_token(request)

    @staticmethod
    async def admin_required(request: Request):
        return await JWTConfig.current_user(request, True)

    '''set custom cookie with httponly'''
    @staticmethod
    async def set_custom_cookies(
            response: Response,
            access_token: str,
            refresh_token: str):

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=3600,
            path="/",
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False,
            samesite="lax",
            max_age=604800,
            path="/",
        )