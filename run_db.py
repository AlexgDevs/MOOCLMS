from asyncio import run
from server import db_manager
from server.db import Course

async def main():
    await db_manager.migrate()

if __name__ == '__main__':
    run(main())
