from typing import List, Literal
from . import BaseModel


class CreateLesson(BaseModel):
    name: str
    content: str
    img: str | None = None
    lesson_type: str
    module_id: int
    creator_id: int 


class LessonResponse(BaseModel):
    id: int
    name: str
    img: str | None 
    content: str
    module_id: int
    creator_id: int
    lesson_type: str 