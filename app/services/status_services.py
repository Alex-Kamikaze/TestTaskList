from typing import List
from sqlalchemy.exc import NoResultFound
from db.entities.models import Status
from exceptions.status_exceptions import StatusNotFoundException
from services.base_service import Service
from schemas.models import StatusModel, StatusModification


class CreateStatusService(Service):
    def __call__(self, status_name: str):
        self.__create_status(status_name)

    def __create_status(self, status_name: str):
        status = Status(name=status_name)
        self.session.add(status)
        self.session.commit()


class SearchStatusService(Service):
    def find_status_by_id(self, status_id: int) -> StatusModel:
        try:
            status = self.session.get_one(Status, status_id)
            return StatusModel(id=status.id, name=status.name)
        except NoResultFound:
            raise StatusNotFoundException()

    def get_all_statuses(self) -> List[StatusModel]:
        statuses = self.session.query(Status).all()
        result = []
        for status in statuses:
            result.append(StatusModel(id=status.id, name=status.name))

        return result


class UpdateStatusService(Service):
    def __call__(self, status_modification_model: StatusModification):
        self.__update_status(status_modification_model)

    def __update_status(self, status_modification_model: StatusModification):
        status = None
        try:
            status = self.session.get_one(Status, status_modification_model.id)
        except NoResultFound:
            raise StatusNotFoundException()

        status.name = (
            status_modification_model.name
            if status_modification_model.name
            else status.name
        )
        self.session.add(status)
        self.session.commit()


class DeleteStatusService(Service):
    def __call__(self, status_id: int):
        self.__delete_status(status_id)

    def __delete_status(self, status_id: int):
        try:
            status = self.session.get_one(Status, status_id)
            self.session.delete(status)
            self.session.commit()
        except NoResultFound:
            raise StatusNotFoundException()