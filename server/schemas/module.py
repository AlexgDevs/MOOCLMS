from typing import List, Literal
from . import BaseModel


class CreateModule(BaseModel):
    name: str
    creator_id: int
    course_id: int


class ModuleResponse(BaseModel):
    id: int
    name: str
    creator_id: int
    course_id: int


class ModuleLesson(BaseModel):
    id: int
    title: str
    content: str
    module_id: int
    creator_id: int 


class DetailModuleResponse(BaseModel):
    id: int
    name: str
    creator_id: int
    course_id: int
    lessons: List[ModuleLesson]