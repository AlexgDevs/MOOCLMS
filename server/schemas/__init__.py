from pydantic import BaseModel

from .user import (
    RegisterUser,
    LoginUser,
    UserResponse,
    DetailUserResponse
)

from .course import (
    DetailCourseResponse, 
    CourseResponse, 
    CreateCourse
)

from .module import (
    CreateModule,
    DetailModuleResponse,
    ModuleResponse
)


from .lesson import (
    CreateLesson,
    LessonResponse
)
