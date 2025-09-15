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


class Module(Base):
    __tablename__='modules'
    name: Mapped[str] = mapped_column(String(255))

    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    creator: Mapped['User'] = relationship('User', back_populates='created_modules', uselist=False)

    course_id: Mapped[int] = mapped_column(ForeignKey('courses.id'))
    course: Mapped['Course'] = relationship('Course', back_populates='modules', uselist=False)

    lessons: Mapped[List['Lesson']] = relationship('Lesson', back_populates='module')
