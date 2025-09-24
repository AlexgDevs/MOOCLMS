from flask import (
    make_response, 
    jsonify, flash, 
    redirect, 
    url_for, 
    render_template,
    request
)

from aiohttp import ClientSession

from .. import app, API_URL 
from ..utils import AauthClient
from ..schemas import CreateFreeCourseForm, CreatePremiumCourseForm


@app.get('/courses/create')
@AauthClient.auth_required
async def create_course_pages():
    user = AauthClient.get_current_user()
    course_type = request.args.get('type')
    match course_type:
        case 'free':
            form = CreateFreeCourseForm()
            return render_template('create_free_course.html', form=form, course_type=course_type)
        case 'premium':
            form = CreatePremiumCourseForm()
            return render_template('create_premium_course.html', form=form, course_type=course_type)
        case _:
            return redirect(url_for('home'))


@app.post('/courses/create-free')
@AauthClient.auth_required
async def create_free_course():
    form = CreateFreeCourseForm()
    user = AauthClient.get_current_user()
    if form.validate_on_submit():
        async with ClientSession(API_URL) as session:

            course_data = {
                'creator_id': int(user.get('id')),
                'name': form.name.data,
                'description': form.description.data,
                'type': 'free'
            }

            async with session.post('/courses', json=course_data) as response:
                if response.status == 201:
                    flash('Курс успешно создан, вы можете посмотреть созданные курсы в профиле', 'info')
                    return redirect(url_for('create_course_pages'))
                flash('Не удалось создать курс', 'error')
                return redirect(url_for('create_course_pages'))
    return render_template('create_free_course.html', form=form, course_type='free')


@app.post('/courses/create-premium')
@AauthClient.auth_required
async def create_premium_course():
    form = CreatePremiumCourseForm()
    user = AauthClient.get_current_user()
    if form.validate_on_submit():
        async with ClientSession(API_URL) as session:

            course_data = {
                'creator_id': int(user.get('id')),
                'name': form.name.data,
                'description': form.description.data,
                'type': 'premium'
            }

            async with session.post('/courses', json=course_data) as response:
                if response.status == 201:
                    flash('Курс успешно создан, вы можете посмотреть созданные курсы в профиле', 'info')
                    return redirect(url_for('create_course_pages'))
                flash('Не удалось создать курс', 'error')
                return redirect(url_for('create_course_pages'))
    return render_template('create_premium_course.html', form=form, course_type='premium')