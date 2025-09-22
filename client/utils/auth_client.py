import asyncio
from functools import wraps
from aiohttp import ClientSession

from flask import (
    Response,
    Request,
    redirect,
    url_for,
    request,
    g
)

from jose import (
    jwt, 
    JOSEError, 
    JWSError
)

from . import (
    ALGORITHM,
    JWT_SECRET
)

from .. import API_URL

class AauthClient:
    @staticmethod
    def auth_required(f):
        @wraps(f)
        async def decorated(*args, **kwargs):
            access_token = request.cookies.get('access_token')
            if access_token:
                try:
                    payload = await asyncio.to_thread(
                        jwt.decode, access_token, JWT_SECRET, algorithms=[
                            ALGORITHM]
                    )
                    g.user = payload.get('user_data')
                    return await f(*args, **kwargs)

                except jwt.ExpiredSignatureError:
                    return await AauthClient.try_refresh_token(f, *args, **kwargs)
                
                except JWSError:
                    pass
            return redirect(url_for('login_page'))
        return decorated


    @staticmethod
    def guest_required(f):
        @wraps(f)
        async def decorated(*args, **kwargs):
            access_token = request.cookies.get('access_token')
            if access_token:
                try:
                    await asyncio.to_thread(
                        jwt.decode, access_token, JWT_SECRET, algorithms=[
                            ALGORITHM]
                    )
                    return redirect(url_for('home'))
                except:
                    pass
            return await f(*args, **kwargs)

        return decorated


    @staticmethod
    async def try_refresh_token(f, *args, **kwargs):
        refresh_token = request.cookies.get('refresh_token')

        if not refresh_token:
            return redirect(url_for('login_page'))

        try:
            async with ClientSession(API_URL) as session:
                async with session.get('/auth/refresh') as response:

                    if response.status == 200:
                        data = await response.json()
                        new_access_token = data['tokens']['new_access_token']

                        response = await f(*args, **kwargs)
                        response.set_cookie(
                            'access_token', new_access_token,
                            httponly=True, secure=False, samesite='Lax'
                        )
                        return response

        except Exception:
            pass

        return redirect(url_for('login_page'))


    @staticmethod
    def get_current_user():
        if hasattr(g, 'user'):
            return g.user
        return None