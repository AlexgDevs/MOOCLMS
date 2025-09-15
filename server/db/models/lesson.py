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


class Lesson(Base):
    __tablename__='lessons'
    name: Mapped[str] = mapped_column(String(255)),
    content: Mapped[str] = mapped_column(String(8096))
    img: Mapped[str]

    creator_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    creator: Mapped['User'] = relationship('User', back_populates='created_lessons', uselist=False) 

    module_id:Mapped[int] = mapped_column(ForeignKey('modules.id'))
    module: Mapped['Module'] = relationship('Module', back_populates='lessons', uselist=False)