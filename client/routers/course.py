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
                'price': None,
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
                'type': 'premium',
                'price': int(form.price.data)
            }

            async with session.post('/courses', json=course_data) as response:
                if response.status == 201:
                    flash('Курс успешно создан, вы можете посмотреть созданные курсы в профиле', 'info')
                    return redirect(url_for('create_course_pages'))
                flash('Не удалось создать курс', 'error')
                return redirect(url_for('create_course_pages'))
    return render_template('create_premium_course.html', form=form, course_type='premium')


@app.get('/course/<int:course_id>')
@app.get('/course/<int:course_id>/lesson/<int:lesson_id>')
@AauthClient.auth_required
async def current_course(course_id, lesson_id=None):
    async with ClientSession(API_URL) as session:
        user = AauthClient.get_current_user()
        async with session.get(f'/courses/detail/{course_id}/{user.get('id')}') as response:
            if response.status == 200:
                course_data = await response.json()
            else:
                return render_template('__404.html')
        
        if not course_data:
            return render_template('__404.html')

        all_lessons = []
        for module in course_data.get('modules', []):
            for lesson in module.get('lessons', []):
                lesson['module_id'] = module['id']
                lesson['module_name'] = module['name']
                all_lessons.append(lesson)
        
        selected_lesson = None
        prev_lesson = None
        next_lesson = None
        current_lesson_index = 0
        lesson_content = None
        
        if all_lessons:
            if lesson_id:
                selected_lesson = next((lesson for lesson in all_lessons if lesson['id'] == lesson_id), None)
            
            if not selected_lesson:
                selected_lesson = all_lessons[0]
            
            if selected_lesson:
                async with session.get(f'/lessons/{selected_lesson["id"]}') as lesson_response:
                    if lesson_response.status == 200:
                        lesson_data = await lesson_response.json()
                        lesson_content = lesson_data.get('content')
                        lesson_photo = lesson_data.get('img')
                        selected_lesson['content'] = lesson_content
                        selected_lesson['photo'] = lesson_photo
                    else:
                        selected_lesson['content'] = "Content not available"
            
            current_lesson_index = all_lessons.index(selected_lesson) + 1
            
            if current_lesson_index > 1:
                prev_lesson = all_lessons[current_lesson_index - 2]
            if current_lesson_index < len(all_lessons):
                next_lesson = all_lessons[current_lesson_index]
        
        return render_template('course.html', 
                                course=course_data,
                                selected_lesson=selected_lesson,
                                prev_lesson=prev_lesson,
                                next_lesson=next_lesson,
                                current_lesson_index=current_lesson_index,
                                total_lessons=len(all_lessons),
                                lesson_content=lesson_content,
                                user=user)


@app.get('/course/<course_id>/edit')
@AauthClient.auth_required
async def redact_course(course_id):
    user = AauthClient.get_current_user()
    async with ClientSession(API_URL) as session:
        async with session.get(f'/courses/detail/{course_id}/{user.get('id')}') as response:
            if response.status == 200:
                course=await response.json()
                if user.get('id') == course.get('creator_id'):
                    return render_template('edit_course.html', course=course, user=user)
                return render_template('__404.html')


