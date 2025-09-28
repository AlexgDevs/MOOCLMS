from typing import List, Literal
from . import BaseModel

class CourseResponse(BaseModel):
    id: int 
    name: str 
    description: str 
    creator_id: int
    price: int
    type: str


class ModuleLessonResponse(BaseModel):
    id: int
    name: str


class ModuleCoureResponse(BaseModel):
    id: int
    name: str
    creator_id: int
    course_id: int
    lessons: List[ModuleLessonResponse]

class RecordUser(BaseModel):
    id: int
    name: str
    role: Literal['user', 'admin', 'moderator']


class RecordsCourse(BaseModel):
    user: List[RecordUser]


class DetailCourseResponse(BaseModel):
    id: int 
    name: str 
    description: str 
    creator_id: int
    type: str 
    modules: List[ModuleCoureResponse]
    record_users: List[RecordsCourse]
    price: int

    class Config:
        from_attributes = True


class CreateCourse(BaseModel):
    name: str
    description: str 
    creator_id: int
    price: int | None 
    type: Literal['free', 'premium']