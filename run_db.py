from asyncio import run
from server import db_manager


async def main():
    await db_manager.up()

if __name__ == '__main__':
    run(main())
