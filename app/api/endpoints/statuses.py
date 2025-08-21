from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from ..deps.db_dependency import get_db
from services.status_services import (
    CreateStatusService,
    SearchStatusService,
    UpdateStatusService,
    DeleteStatusService,
)
from schemas.models import StatusModel, StatusModification
from exceptions.status_exceptions import StatusNotFoundException

router = APIRouter()


@router.put("/create", status_code=201)
async def create_status(status_name: str, session: Session = Depends(get_db)):
    service = CreateStatusService(session)
    service(status_name)


@router.get("/get", status_code=200)
async def get_status_by_id(status_id: int, session: Session = Depends(get_db)) -> StatusModel:
    service = SearchStatusService(session)
    try:
        return service.find_status_by_id(status_id)
    except StatusNotFoundException:
        raise HTTPException(status_code=404, detail="Указанного статуса не найдено")


@router.get("/get_all_statuses", status_code=200)
async def get_all_statuses(session: Session = Depends(get_db)) -> List[StatusModel]:
    service = SearchStatusService(session)
    statuses = service.get_all_statuses()
    return statuses


@router.patch("/update", status_code=200)
async def update_status(status_modification_model: StatusModification, session: Session = Depends(get_db)):
    service = UpdateStatusService(session)
    try:
        service(status_modification_model)
    except StatusNotFoundException:
        raise HTTPException(status_code=404, detail="Указанный статус не найден")


@router.delete("/delete", status_code=200)
async def delete_status(status_id: int, session: Session = Depends(get_db)):
    service = DeleteStatusService(session)
    try:
        service(status_id)
    except StatusNotFoundException:
        raise HTTPException(status_code=404, detail="Указанный статус не найден")