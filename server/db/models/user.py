from typing import (
    List,
    Literal
)

from . import (
    Mapped,
    mapped_column,
    relationship,

    String
)

from .. import Base


class User(Base):
    __tablename__='users'
    name: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(512))
    role: Mapped[Literal['user', 'admin', 'moderator']] = mapped_column(String(255), default='user')

    created_courses: Mapped[List['Course']] = relationship('Course', back_populates='creator')
    created_modules: Mapped[List['Module']] = relationship('Module', back_populates='creator')
    created_lessons: Mapped[List['Lesson']] = relationship('Lesson', back_populates='creator')

    record_courses: Mapped[List['RecordCourse']] = relationship('RecordCourse', back_populates='user')