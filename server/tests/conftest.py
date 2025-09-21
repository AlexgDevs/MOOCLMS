from pytest_asyncio import fixture
from aiohttp import ClientSession

from .. import API_URL

@fixture
async def client_session():
    async with ClientSession(API_URL) as session:
        yield session


