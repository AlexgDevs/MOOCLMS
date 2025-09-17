from pydantic import BaseModel

from .user import (
    RegisterUser,
    LoginUser,
    UserResponse,
    DetailUserResponse
)

from .course import DetailCourseResponse, CourseResponse, CreateCourse
from .module import CreateModule
from .lesson import CreateLesson
