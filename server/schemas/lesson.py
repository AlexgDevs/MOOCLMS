from typing import List, Literal
from . import BaseModel


class CreateLesson(BaseModel):
    title: str
    content: str
    img: str | None = None
    module_id: int
    creator_id: int 


class LessonResponse(BaseModel):
    id: int
    title: str
    content: str
    module_id: int
    creator_id: int 