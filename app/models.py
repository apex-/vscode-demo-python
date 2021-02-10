from typing import Optional, List
from pydantic import BaseModel

class TaskCreateInput(BaseModel):
    title: str
    description: Optional[str]
    done: bool = False

class TaskUpdateInput(BaseModel):
    title: Optional[str]
    description: Optional[str]
    done: Optional[bool]

class Task(TaskCreateInput):
    id: int
    title: str
    description: Optional[str]
    done: bool
