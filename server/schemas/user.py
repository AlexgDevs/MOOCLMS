from typing import List, Literal
from . import BaseModel


class RegisterUser(BaseModel):
    name: str
    password: str


class LoginUser(BaseModel):
    name: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    role: Literal['user', 'admin', 'moderator']


class UserCreatedCourses(BaseModel):
    id: int
    name: str 
    description: str
    creator_id: int


class UserCreatedModules(BaseModel):
    id: int
    name: str 
    creator_id: int


class UserCreatedLessons(BaseModel):
    id: int 
    name: str 
    creator_id: int


class UserRecordCourse(BaseModel):
    id: int 
    name: str 
    description: str 
    creator_id: int
    price: int
    cover_url: str | None 
    type: str


class RecordCourse(BaseModel):
    course: UserRecordCourse 

    class Config:
        from_attributes = True


class DetailUserResponse(BaseModel):
    id: int
    name: str
    role: Literal['user', 'admin', 'moderator']
    created_courses: List[UserCreatedCourses]
    created_modules: List[UserCreatedModules]
    created_lessons: List[UserCreatedLessons]
    record_courses: List[RecordCourse]

    class Config:
        from_attributes = True