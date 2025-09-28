from pytest import mark
from faker import Faker
from .conftest import client_session

faq = Faker()

#200
@mark.asyncio
async def test_success_modules_output(client_session):
    async with client_session.get('/modules') as response:
        assert response.status == 200


@mark.asyncio
async def test_success_lessons_output(client_session):
    async with client_session.get('/lessons') as response:
        assert response.status == 200


@mark.asyncio
async def test_success_users_output(client_session):
    async with client_session.get('/users') as response:
        assert response.status == 200


@mark.asyncio
async def test_success_courses_output(client_session):
    async with client_session.get('/courses') as response:
        assert response.status == 200


#404
@mark.asyncio 
async def test_404_user_output(client_session):
    async with client_session.get(f'/users/{1489}') as response:
        assert response.status == 404


@mark.asyncio
async def test_404_user_detail_output(client_session):
    async with client_session.get(f'/users/detail/{1489}') as response:
        assert response.status == 404


@mark.asyncio
async def test_404_course_output(client_session):
    async with client_session.get(f'/courses/{1489}') as response:
        assert response.status == 404


@mark.asyncio
async def test_404_course_output(client_session):
    async with client_session.get(f'/courses/detail/{1489}') as response:
        assert response.status == 404


@mark.asyncio
async def test_create_module(client_session):

    module_data = {
        'creator_id': 8,
        'course_id': 3,
        'name': faq.name()
    }

    async with client_session.post('/modules', json=module_data) as response:
        assert response.status == 201


@mark.asyncio
async def test_create_lsson(client_session):

    lesson_data = {
        'creator_id': 1,
        'module_id': 2,
        'name': faq.name(),
        'content': faq.text(max_nb_chars=255)
    }

    async with client_session.post('/lessons', json=lesson_data) as response:
        assert response.status == 201