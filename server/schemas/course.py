from typing import List, Literal
from . import BaseModel


class ModuleLessonResponse(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class ModuleCoureResponse(BaseModel):
    id: int
    name: str
    creator_id: int
    course_id: int
    lessons: List[ModuleLessonResponse]

    class Config:
        from_attributes = True


class RecordUser(BaseModel):
    id: int
    name: str
    role: Literal['user', 'admin', 'moderator']

    class Config:
        from_attributes = True


class RecordsCourse(BaseModel):
    user: RecordUser

    class Config:
        from_attributes = True


class CourseResponse(BaseModel):
    id: int 
    name: str 
    description: str 
    creator_id: int
    price: int
    cover_url: str | None 
    type: str
    record_users: List[RecordsCourse]

    class Config:
        from_attributes = True


class DetailCourseResponse(BaseModel):
    id: int 
    name: str 
    description: str 
    creator_id: int
    type: str
    cover_url: str | None 
    modules: List[ModuleCoureResponse]
    record_users: List[RecordsCourse]
    price: int

    class Config:
        from_attributes = True


class CreateCourse(BaseModel):
    name: str
    description: str
    cover_url: str | None = None 
    creator_id: int
    price: int | None 
    type: Literal['free', 'premium']


class EnrollUser(BaseModel):
    user_id: int