from pydantic import BaseModel
from typing import Optional

class TaskModel(BaseModel):
    id: str
    name: str
    text: str
    status: str


class TaskCreationModel(BaseModel):
    name: str
    text: str
    status: int  # ID статуса задачи


class TaskModificationModel(BaseModel):
    id: str
    name: Optional[str]
    text: Optional[str]
    status: Optional[int]

class StatusModel(BaseModel):

    id: int
    name: str

class StatusModification(BaseModel):

    id: int
    name: Optional[str]
