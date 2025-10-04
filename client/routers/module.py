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
from ..schemas import CreateModuleForm


@app.get('/create/module/<course_id>')
@AauthClient.auth_required
async def create_module_page(course_id):
    form = CreateModuleForm()
    user = AauthClient.get_current_user()
    async with ClientSession(API_URL) as session:
        async with session.get(f'/courses/{course_id}/{user.get('id')}') as response:
            if response.status == 200:
                course = await response.json()
                return course

        return render_template('create_module.html', course_id=course_id, form=form)


@app.post('/create/module')
@AauthClient.auth_required
async def create_module():
    form = CreateModuleForm()
    if form.validate_on_submit():

        user = AauthClient.get_current_user()
        async with ClientSession(API_URL) as session:

            module_data = {
                'creator_id': int(user.get('id')),
                'course_id': int(request.form.get('course_id')),
                'name': form.name.data
            }

            async with session.post('/modules', json=module_data) as response:
                if response.status == 201:
                    flash('Вы успешно создали курс', 'info')
                    return redirect(url_for('redact_course', course_id=request.form.get('course_id')))

    flash('Не удалось создать модуль курса', 'error')
    return render_template('creted_module.html', course_id=request.form.get('course_id'), form=form)