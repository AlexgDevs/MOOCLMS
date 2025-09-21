from typing import List, Literal
from . import BaseModel


class CreateLesson(BaseModel):
    name: str
    content: str
    img: str | None = None
    module_id: int
    creator_id: int 


class LessonResponse(BaseModel):
    id: int
    name: str
    content: str
    module_id: int
    creator_id: int 