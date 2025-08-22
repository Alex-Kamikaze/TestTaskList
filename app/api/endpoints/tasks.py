from typing import List
import uuid
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from ..deps.db_dependency import get_db
from schemas.models import TaskCreationModel, TaskModel, TaskModificationModel
from services.tasks_services import (
    TaskCreationService,
    TaskSearchService,
    TaskModificationService,
    TaskDeleteService,
)
from exceptions.task_exceptions import TaskCreationException, TaskNotFoundException, IncorrectUUIDPassed
from exceptions.status_exceptions import StatusNotFoundException

router = APIRouter()


@router.put("/create", status_code=201)
async def create_task(
    task_model: TaskCreationModel, session: Session = Depends(get_db)
):
    service = TaskCreationService(session)
    try:
        service(task_model)
        return {"result": "ok"}
    except TaskCreationException:
        raise HTTPException(
            status_code=400, detail="Произошла ошибка при создании задачи"
        )
    except StatusNotFoundException:
        raise HTTPException(status_code=404, detail="Не найдено статуса с таким id")


@router.get("/get", status_code=200, response_model=TaskModel)
async def get_task(task_id: str, session: Session = Depends(get_db)) -> TaskModel:
    service = TaskSearchService(session)
    try:
        task_id = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Неправильный формат UUID")

    try:
        return service.find_task_by_id(task_id)
    except TaskNotFoundException:
        raise HTTPException(status_code=404, detail="Не найдено задачи с таким id")
    except StatusNotFoundException:
        raise HTTPException(status_code=404, detail="Не найдено статуса с таким id")


@router.get("/get_list", status_code=200, response_model=List[TaskModel])
async def get_task_list(session: Session = Depends(get_db)):
    service = TaskSearchService(session)
    tasks = service.get_all_tasks()
    return tasks


@router.patch("/update", status_code=200)
async def update_task(
    task_modification_model: TaskModificationModel, session: Session = Depends(get_db)
):
    service = TaskModificationService(session)

    try:
        service(task_modification_model)
    except IncorrectUUIDPassed:
        raise HTTPException(status_code=400, detail="Указан неправильный UUID задачи")
    except TaskNotFoundException:
        raise HTTPException(status_code=404, detail="Указанной задачи не найдено!")
    except StatusNotFoundException:
        raise HTTPException(status_code=404, detail="Указанный статус не найден")


@router.delete("/delete", status_code=200)
async def delete_task(task_id: str, session: Session = Depends(get_db)):
    service = TaskDeleteService(session)
    try:
        task_id = uuid.UUID(task_id)
    except ValueError:
        raise HTTPException(status_code=400, detail="Неправильный формат id задачи")

    try:
        service(task_id)
    except TaskNotFoundException:
        raise HTTPException(status_code=404, detail="Указаной задачи не найдено")
