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


class DetailUserResponse(BaseModel):
    id: int
    name: str
    role: Literal['user', 'admin', 'moderator']
    created_courses: List[UserCreatedCourses]
    created_modules: List[UserCreatedModules]
    created_lessons: List[UserCreatedLessons]

    class Config:
        from_attributes = True