from flask import (
    make_response, 
    jsonify, flash, 
    redirect, 
    url_for, 
    render_template,
    request
)

from aiohttp import ClientSession
from base64 import b64encode

from .. import app, API_URL 
from ..utils import AauthClient
from ..schemas import CreateLessonForm


@app.get('/create/lesson/<course_id>/<module_id>')
@AauthClient.auth_required
async def create_lesson_page(course_id, module_id):
    form = CreateLessonForm()
    user = AauthClient.get_current_user()
    async with ClientSession(API_URL) as session:
        async with session.get(f'/courses/{course_id}/{user.get('id')}') as response:
            if response.status == 200:
                return render_template('create_lesson.html', form=form, module_id=module_id, course_id=course_id, user_id=user.get('id'))
            return 'nezya', 403


@app.post('/create/lesson')
@AauthClient.auth_required
async def create_lesson():
    form = CreateLessonForm()
    if form.validate_on_submit():
        if form.image.data:
            file = form.image.data
            file_bs64 = b64encode(file.read()).decode()

        else:
            file_bs64 = None 
        
        async with ClientSession(API_URL) as session:

            lesson_data = {
                'name': form.name.data,
                'content': form.content.data,
                'img': file_bs64,
                'creator_id': int(request.form.get('user_id')),
                'module_id': int(request.form.get('module_id')),
                'lesson_type': form.lesson_type.data
            }

            async with session.post('/lessons', json=lesson_data) as response:
                if response.status == 201:
                    flash('Вы успешно создали урок', 'info')
                    return redirect(url_for('redact_course', course_id=request.form.get('course_id')))
                flash('Не удалось создать курс', 'error')
                return render_template('create_lesson.html', form=form, module_id=request.form.get('module_id'), course_id=request.form.get('course_id'))
    return render_template('create_lesson.html', form=form, module_id=request.form.get('module_id'), course_id=request.form.get('course_id'))
