from aiohttp import ClientSession
from flask import (
    make_response,
    flash, 
    redirect, 
    url_for, 
    render_template, 
)

from sqlalchemy import select
from passlib.context import CryptContext

from .. import app, API_URL
from ..db import db_manager, User
from ..schemas import (
    LoginForm,
    RegisterForm
)

from ..utils import AauthClient

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.get('/register-page')
@AauthClient.guest_required
async def register_page():
    form = RegisterForm()
    return render_template('register.html', form=form)


@app.get('/login-page')
@AauthClient.guest_required
async def login_page():
    form = LoginForm()
    return render_template('login.html', form=form)


@app.get('/logout-page')
@AauthClient.auth_required
async def logout_page():
    return render_template('logout.html')


@app.post('/register')
@AauthClient.guest_required
async def register():
    form = RegisterForm()
    if form.validate_on_submit():
        async with db_manager.Session() as session:
            user = await session.scalar(
                select(User)
                .where(User.name == form.name.data)
            )

            if user:
                flash('Имя пользователя занято', 'error')
                return render_template('register.html', form=form)

        async with ClientSession(API_URL) as http_session:

            user_data = {
                'name': form.name.data,
                'password': form.password.data
            }

            async with http_session.post('/auth/register', json=user_data) as response:
                if response.status == 201:
                    tokens = await response.json()
                    response = make_response(
                        redirect(url_for('home')))

                    response.set_cookie(
                        'access_token',
                        value=tokens.get('tokens').get('access'),
                        httponly=True,
                        secure=True,
                        samesite='Strict',
                        max_age=3600,
                        path='/'
                    )

                    response.set_cookie(
                        'refresh_token',
                        value=tokens.get('tokens').get('refresh'),
                        httponly=True,
                        secure=True,
                        samesite='Strict',
                        max_age=604800,
                        path='/'
                    )

                    flash('Вы успешно зарегестрировались', 'info')
                    return response
                return render_template('register.html', form=form)
    return render_template('register.html', form=form)


@app.post('/login')
@AauthClient.guest_required
async def login():
    form = LoginForm()
    if form.validate_on_submit():
        async with db_manager.Session() as session:
            user = await session.scalar(select(User).where(User.name == form.name.data))
            if not user:
                flash('Пользователя не существует', 'error')
                return render_template('login.html', form=form)

            if not pwd_context.verify(form.password.data, user.password):
                flash('Неверный пароль', 'error')
                return render_template('login.html', form=form)

        async with ClientSession(API_URL) as session:
            user_data = {
                'name': form.name.data,
                'password': form.password.data
            }

            async with session.post('/auth/token', json=user_data) as response:
                if response.status == 200:
                    tokens = await response.json()
                    response = make_response(redirect(url_for('home')))

                    response.set_cookie(
                        'access_token',
                        value=tokens.get('tokens').get('access'),
                        httponly=True,
                        secure=True,
                        samesite='Strict',
                        max_age=3600
                    )

                    response.set_cookie(
                        'refresh_token',
                        value=tokens.get('tokens').get('refresh'),
                        httponly=True,
                        secure=True,
                        samesite='Strict',
                        max_age=604800
                    )

                    flash('Вы успешно авторизовались', 'info')
                    return response

                return render_template('login.html', form=form)
    return render_template('login.html', form=form)


@app.get('/logout/accept')
@AauthClient.auth_required
async def logout_accept():
    async with ClientSession(API_URL) as session:
        async with session.delete('/auth/logout') as response:
            if response.status == 200:
                response_obj = redirect(url_for('login_page'))

                response_obj.set_cookie(
                    'access_token',
                    value='',
                    expires=0,
                    httponly=True,
                    secure=True,
                    samesite='Strict',
                    path='/'
                )

                response_obj.set_cookie(
                    'refresh_token',
                    value='',
                    expires=0,
                    httponly=True,
                    secure=True,
                    samesite='Strict',
                    path='/'
                )

                flash('Вы успешно вышли из аккаунта', 'info')
                return response_obj

        flash('Не удалось выйти из аккаунта', 'error')
        return redirect(url_for('home'))


@app.get('/logout/cancel')
@AauthClient.auth_required
async def logout_cancel():
    return redirect(url_for('home'))
