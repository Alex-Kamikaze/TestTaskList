import uuid
import factory
from schemas.models import TaskCreationModel, StatusModel, TaskModificationModel, StatusModification
from db.entities.models import Status, Task

class StatusCreationFactory(factory.Factory):
    """ Создание модели статуса на уровне бизнес-логики"""
    class Meta:
        model = StatusModel

    id = 1
    name = "В работе"

class StatusDbModelFactory(factory.Factory):
    class Meta:
        model = Status

    id = 1
    name = "В работе"

class TaskCreationModelFactory(factory.Factory):
    class Meta:
        model = TaskCreationModel

    name = "Тестовая задача"
    text = "Тестовая задача для проверки сервиса создания задач"
    status = 1

class TaskWithNonExistingStatus(factory.Factory):
    class Meta:
        model = TaskCreationModel

    name = "Тестовая задача"
    text = "Тестовая задача для проверки сервиса создания задач"
    status = -1

class TaskDbModelFactory(factory.Factory):
    class Meta:
        model = Task

    id = uuid.uuid4()
    name = "test"
    text = "test"
    status_id = 1

class TaskUpdateModelFactory(factory.Factory):
    class Meta:
        model = TaskModificationModel

    id = str(uuid.uuid4())
    name = "update"
    text = "update"
    status = 1

class UpdateStatusModelFactory(factory.Factory):
    class Meta:
        model = StatusModification

    id = 1
    name = "update"