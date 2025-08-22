import pytest
from sqlalchemy.exc import NoResultFound
from db.entities.models import Status
from exceptions.status_exceptions import StatusNotFoundException
from .factories import StatusDbModelFactory, UpdateStatusModelFactory

def test_status_creation_service(create_status_service, mock_session):
    create_status_service(status_name="тест")

    status = mock_session.query(Status).filter_by(name="тест").one_or_none()
    assert status is not None
    assert status.name == "тест"

def test_status_search_with_incorrect_id(search_status_service):
    with pytest.raises(StatusNotFoundException):
        search_status_service.find_status_by_id(status_id=0)

def test_status_search_with_correct_id(search_status_service, mock_session):
    status = StatusDbModelFactory()
    mock_session.add(status)
    mock_session.commit()

    found_status = search_status_service.find_status_by_id(status_id=status.id)
    assert found_status.id == status.id
    assert found_status.name == status.name

def test_status_search_with_empty_base(search_status_service):
    statuses = search_status_service.get_all_statuses()
    assert len(statuses) == 0

def test_get_all_statuses(search_status_service, mock_session):
    status = StatusDbModelFactory()
    second_status = StatusDbModelFactory(id=2, name="Второй")
    mock_session.add(status)
    mock_session.add(second_status)
    mock_session.commit()

    statuses = search_status_service.get_all_statuses()
    assert len(statuses) == 2

def test_update_service_with_nonexisting_status(update_status_service):
    update = UpdateStatusModelFactory(id=0)
    with pytest.raises(StatusNotFoundException):
        update_status_service(update)

def test_update_service_with_correct_updated(update_status_service, mock_session):
    status = StatusDbModelFactory()
    mock_session.add(status)
    mock_session.commit()

    update = UpdateStatusModelFactory()
    update_status_service(update)

    updated_status = mock_session.query(Status).filter_by(id=1).one_or_none()
    assert updated_status is not None
    assert updated_status.id == 1
    assert updated_status.name == "update"

def test_status_delete_service_with_non_existing_status(delete_status_service):
    with pytest.raises(StatusNotFoundException):
        delete_status_service(0)

def test_status_delete_service_with_correct_task(delete_status_service, mock_session):
    status = StatusDbModelFactory()
    mock_session.add(status)
    mock_session.commit()

    delete_status_service(status.id)

    with pytest.raises(NoResultFound):
        mock_session.get_one(Status, status.id)