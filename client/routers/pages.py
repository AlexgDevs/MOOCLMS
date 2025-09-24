from flask import (
    make_response, 
    jsonify, flash, 
    redirect, 
    url_for, 
    render_template
)

from aiohttp import ClientSession

from .. import app, API_URL 
from ..utils import AauthClient

@app.get('/')
@AauthClient.auth_required
async def home():
    user_client = AauthClient.get_current_user()
    async with ClientSession(API_URL) as session:
        async with session.get(f'/users/detail/{user_client.get('id')}') as response:
            if response.status == 200:
                user = await response.json()
                return render_template('profile.html', user=user)
            return redirect(url_for('login_page'))


@app.get('/courses')
@AauthClient.auth_required
async def courses():
    user = AauthClient.get_current_user()
    async with ClientSession(API_URL) as session:
        async with session.get(f'/courses') as response:
            if response.status == 200:
                courses = await response.json()
                return render_template('courses.html', courses=courses, user=user)
            flash('Не удалось открыть страницу курсов', 'error')
            return redirect(url_for('home'))


@app.get('/courses-teach')
@AauthClient.auth_required
async def teach_course():
    user = AauthClient.get_current_user()
    return render_template('creating_courses.html', user=user)