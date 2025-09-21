from aiohttp import ClientSession
from flask import make_response, jsonify, flash, redirect, url_for, render_template

from .. import app, API_URL
from ..schemas import (
    LoginForm,
    RegisterForm
)

@app.get('/register-page')
async def register_page():
    pass


@app.get('/login-page')
async def login_page():
    pass


@app.get('/logout-page')
async def logout_page():
    pass


@app.post('/register')
async def register():
    form = RegisterForm()
    if form.validate_on_submit():
        async with ClientSession(API_URL) as session:

            user_data = {
                'name': form.name.data,
                'password': form.password.data
            }

            async with session.post('/auth/register', json=user_data) as response:
                if response.status == 201:
                    tokens = await response.json()
                    response = make_response(jsonify({'message': 'registered'}))

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

                    flash('Вы успешно зарегестрировались', 'info')
                    return redirect(url_for('home'))
    pass


@app.post('/login')
async def login():
    form = LoginForm()
    if form.validate_on_submit():
        async with ClientSession(API_URL) as session:

            user_data = {
                'name': form.name.data,
                'password': form.password.data
            }

            async with session.post('/auth/token', json=user_data) as response:
                if response.status == 201:
                    tokens = await response.json()
                    response = make_response(jsonify({'message': 'loggined'}))

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

    pass 

@app.post('/logout/accept')
async def logout_accept():
    pass


@app.post('/logout/cancel')
async def logout_cancel():
    pass