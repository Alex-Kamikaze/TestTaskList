from typing import List
from sqlalchemy.exc import OperationalError, NoResultFound
from services.base_service import Service
from schemas.models import TaskCreationModel, TaskModel, TaskModificationModel
from db.entities.models import Task, Status
from exceptions.task_exceptions import TaskCreationException, TaskNotFoundException
from exceptions.status_exceptions import StatusNotFoundException


class TaskCreationService(Service):
    def __call__(self, task_model: TaskCreationModel):
        self.__create_task(task_model)

    def __create_task(self, task_model: TaskCreationModel):
        try:
            self.session.get_one(Status, task_model.status)
        except NoResultFound:
            raise StatusNotFoundException()

        try:
            self.session.add(
                Task(
                    name=task_model.name,
                    text=task_model.text,
                    status_id=task_model.status,
                )
            )
            self.session.flush()
            self.session.commit()
        except OperationalError:
            raise TaskCreationException()


class TaskSearchService(Service):
    def find_task_by_id(self, task_id: str) -> TaskModel:
        # TODO: Починить поиск статуса по id
        try:
            task = self.session.get_one(Task, ident=task_id)
            status = (
                self.session.query(Status).filter_by(id=task.status_id).one_or_none()
            )
            if status is None:
                raise StatusNotFoundException()
            else:
                model = TaskModel(
                    id=task.id.hex, name=task.name, text=task.text, status=status.name
                )
                return model
        except NoResultFound:
            raise TaskNotFoundException()

    def get_all_tasks(self) -> List[TaskModel]:
        result = []
        tasks: List[Task] = self.session.query(Task).all()
        for task in tasks:
            status: Status = (
                self.session.query(Status).filter_by(id=task.status_id).one_or_none()
            )
            if status is None:
                raise StatusNotFoundException()
            else:
                result.append(
                    TaskModel(
                        id=task.id.hex,
                        name=task.name,
                        text=task.text,
                        status=status.name,
                    )
                )

        return result


class TaskModificationService(Service):
    def __call__(self, task_modification_model: TaskModificationModel):
        self.__update_task(task_modification_model)

    def __update_task(self, task_modification_model: TaskModificationModel):
        task = None
        try:
            task = self.session.get_one(Task, task_modification_model.id)
        except NoResultFound:
            raise TaskNotFoundException()

        if task_modification_model.status:
            try:
                self.session.get_one(Status, task_modification_model.status)
            except NoResultFound:
                raise StatusNotFoundException()

        if task:
            task.name = (
                task_modification_model.name
                if task_modification_model.name
                else task.name
            )
            task.text = (
                task_modification_model.text
                if task_modification_model.text
                else task.text
            )
            task.status_id = (
                task_modification_model.status
                if task_modification_model.status
                else task.status
            )

            self.session.add(task)
            self.session.commit()


class TaskDeleteService(Service):
    def __call__(self, task_id: str):
        self.__delete_task(task_id)

    def __delete_task(self, task_id: str):
        try:
            task = self.session.get_one(Task, task_id)
            self.session.delete(task)
            self.session.commit()
        except NoResultFound:
            raise TaskNotFoundException()
