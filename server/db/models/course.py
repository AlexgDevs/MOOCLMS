from typing import (
    List,
    Literal
)

from . import (
    Mapped,
    mapped_column,
    relationship,

    ForeignKey,
    String
)

from .. import Base


class Course(Base):
    __tablename__='courses'
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(1024))
    type: Mapped[Literal['free', 'premium']]
    price: Mapped[int] = mapped_column(default=0)
    cover_url: Mapped[str]

    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    creator: Mapped['User'] = relationship('User', back_populates='created_courses', uselist=False)

    modules: Mapped[List['Module']] = relationship('Module', back_populates='course')

    record_users: Mapped[List['RecordCourse']] = relationship('RecordCourse', back_populates='course')


class RecordCourse(Base):
    __tablename__='record_courses'
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'))

    user: Mapped['User'] = relationship('User', back_populates='record_courses', uselist=False)
    course: Mapped['Course'] = relationship('Course', back_populates='record_users', uselist=False)