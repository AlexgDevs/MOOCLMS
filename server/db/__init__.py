from os import getenv
from dotenv import load_dotenv

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column
)

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)

load_dotenv()

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "mooc.db"
DB_URL = getenv("DB_URL", f"sqlite+aiosqlite:///{DB_PATH}")


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)


class DBManager():
    def __init__(self, db_url: str, echo: bool = True):
        self.db_url=db_url
        self.echo = echo

        self.engine = create_async_engine(
            url=self.db_url,
            echo=self.echo
        ) 

        self.Session = async_sessionmaker(
            self.engine
        )


    async def up(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


    async def drop(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


    async def db_session(self):
        async with self.Session() as session:
            yield session


    async def db_session_begin(self):
        async with self.Session.begin() as session:
            yield session


    async def migrate(self):
        await self.drop()
        await self.up()


db_manager = DBManager(
    db_url=DB_URL,
    echo=True
)


from .models import (
    Course,
    RecordCourse,
    User,
    Module,
    Lesson
)