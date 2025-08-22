import uuid
import pytest
from sqlalchemy.exc import NoResultFound
from db.entities.models import Task
from exceptions.task_exceptions import TaskNotFoundException
from exceptions.status_exceptions import StatusNotFoundException
from .factories import (
    TaskCreationModelFactory,
    TaskWithNonExistingStatus,
    StatusDbModelFactory,
    TaskDbModelFactory,
    TaskUpdateModelFactory
)


def test_when_nonexisting_status_is_passed(task_creation_service):
    task = TaskWithNonExistingStatus()
    with pytest.raises(StatusNotFoundException):
        task_creation_service(task)


def test_correct_task_creation(task_creation_service, mock_session):
    status = StatusDbModelFactory()
    mock_session.add(status)
    mock_session.commit()
    task = TaskCreationModelFactory()
    task_creation_service(task)

    task_from_db = (
        mock_session.query(Task).filter_by(name="Тестовая задача").one_or_none()
    )
    assert task_from_db is not None
    assert task_from_db.name == "Тестовая задача"
    assert task_from_db.text == "Тестовая задача для проверки сервиса создания задач"


def test_task_search_with_nonexisting_task(task_search_service):
    fake_uuid = (
        uuid.uuid4()
    )  # т.к. в каждом тесте база по умолчанию пустая, там точно нет задачи с таким UUID
    with pytest.raises(TaskNotFoundException):
        task_search_service.find_task_by_id(fake_uuid)


def test_real_task_is_found_correctly(task_search_service, mock_session):
    status = StatusDbModelFactory()
    task = TaskDbModelFactory()
    mock_session.add(task)
    mock_session.add(status)
    mock_session.commit()

    found_task = task_search_service.find_task_by_id(task.id)
    assert uuid.UUID(found_task.id) == task.id
    assert found_task.name == task.name
    assert found_task.text == task.text

def test_task_search_service_returns_empty_list_with_no_tasks_found(task_search_service):
    tasks = task_search_service.get_all_tasks()
    assert len(tasks) == 0

def test_task_search_service_returns_correctly(task_search_service, mock_session):
    task = TaskDbModelFactory()
    status = StatusDbModelFactory()
    mock_session.add(status)
    mock_session.add(task)
    mock_session.commit()

    tasks = task_search_service.get_all_tasks()
    assert len(tasks) == 1

def test_modification_service_with_nonexisting_task(task_modification_service):
    fake_update = TaskUpdateModelFactory()

    with pytest.raises(TaskNotFoundException):
           task_modification_service(fake_update)

def test_modification_service_with_correct_task(task_modification_service, mock_session):
    status = StatusDbModelFactory()
    new_status = StatusDbModelFactory(id=2, name="update")
    task = TaskDbModelFactory()
    update = TaskUpdateModelFactory(id=str(task.id), status=new_status.id)
    mock_session.add(status)
    mock_session.add(task)
    mock_session.add(new_status)
    mock_session.commit()

    assert mock_session.query(Task).filter_by(id=task.id).one_or_none() is not None

    task_modification_service(update)

    updated_task = mock_session.get_one(Task, task.id)
    assert updated_task.name == "update"
    assert updated_task.text == "update"
    assert updated_task.status_id == 2

def test_delete_service_with_not_existing_task(task_delete_service):
    fake_uuid = uuid.uuid4()
    with pytest.raises(TaskNotFoundException):
        task_delete_service(fake_uuid)

def test_delete_service_with_correct_task(task_delete_service, mock_session):
    task = TaskDbModelFactory()
    status = StatusDbModelFactory()
    mock_session.add(status)
    mock_session.add(task)
    mock_session.commit()

    task_delete_service(task.id)
    with pytest.raises(NoResultFound):
        mock_session.get_one(Task, task.id)