from typing import List, Literal
from . import BaseModel


class CreateModule(BaseModel):
    name: str
    creator_id: int
    course_id: int