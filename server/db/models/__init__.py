from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy import (
    ForeignKey,
    String,
    DateTime
)

from .course import Course, RecordCourse
from .user import User
from .lesson import Lesson
from .module import Module