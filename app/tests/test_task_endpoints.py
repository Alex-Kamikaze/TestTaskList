import uuid
import json
import pytest
from sqlalchemy.exc import NoResultFound
from .factories import StatusDbModelFactory, TaskDbModelFactory
from db.entities.models import Task

def test_create_task_endpoint_with_incorrect_status(api_client):
    resp = api_client.put("/tasks/create", json={"name": "test", "text": "test", "status": "-5"})
    assert resp.status_code == 404

def test_create_task_endpoint_with_correct_status(api_client, mock_session):
    status = StatusDbModelFactory()
    mock_session.add(status)
    mock_session.commit()

    resp = api_client.put("/tasks/create", json={"name": "test", "text": "test", "status": "1"})
    task = mock_session.query(Task).filter_by(name="test").one_or_none()
    assert resp.status_code == 201
    assert task is not None
    assert task.name == "test"
    assert task.text == "test"

def test_search_endpoint_with_incorrect_id(api_client):
    fake_uuid = uuid.uuid4()

    resp = api_client.get(f"/tasks/get?task_id={fake_uuid.hex}")
    assert resp.status_code == 404

def test_search_endpoint_with_correct_id(api_client, mock_session):
    task = TaskDbModelFactory()
    status = StatusDbModelFactory()
    mock_session.add(status)
    mock_session.add(task)
    mock_session.commit()

    resp = api_client.get(f"/tasks/get?task_id={str(task.id)}")
    found_task = json.loads(resp.text)
    assert resp.status_code == 200
    assert found_task.get("id") == task.id.hex
    assert found_task.get("name") == task.name
    assert found_task.get("text") == task.text
    assert found_task.get("status") == status.name

def test_list_endpoint_with_empty_base(api_client):
    
    resp = api_client.get("/tasks/get_list")
    result = json.loads(resp.text)
    assert resp.status_code == 200
    assert result == []

def test_list_endpoint_with_existing_tasks(api_client, mock_session):
    task = TaskDbModelFactory()
    another_task = TaskDbModelFactory(id = uuid.uuid4(), name="Тест 2")
    status = StatusDbModelFactory()

    mock_session.add(status)
    mock_session.add(task)
    mock_session.add(another_task)

    resp = api_client.get("/tasks/get_list")
    tasks = json.loads(resp.text)
    assert resp.status_code == 200
    assert len(tasks) == 2

def test_update_endpoint_with_nonexisting_task(api_client):
    task = TaskDbModelFactory()

    resp = api_client.patch("/tasks/update", json={"id": str(task.id), "name": task.name, "text": task.text, "status": task.status_id})
    assert resp.status_code == 404

def test_update_endpoint_with_correct_task(api_client, mock_session):
    task = TaskDbModelFactory()
    status = StatusDbModelFactory()

    mock_session.add(status)
    mock_session.add(task)
    mock_session.commit()

    resp = api_client.patch("/tasks/update", json={"id": str(task.id), "name": "update", "text": "update", "status": task.status_id})
    
    assert resp.status_code == 200

    updated_task = mock_session.query(Task).filter_by(name="update").one_or_none()
    assert updated_task is not None
    assert updated_task.name == "update"
    assert updated_task.text == "update"

def test_delete_endpoint_with_nonexisting_id(api_client):
    fake_uuid = uuid.uuid4()

    resp = api_client.delete(f"/tasks/delete?task_id={fake_uuid.hex}")
    assert resp.status_code == 404

def test_delete_endpoint_with_correct_task(api_client, mock_session):
    task = TaskDbModelFactory()
    status = StatusDbModelFactory()

    mock_session.add(status)
    mock_session.add(task)
    mock_session.commit()

    resp = api_client.delete(f"/tasks/delete?task_id={task.id.hex}")
    assert resp.status_code == 200

    with pytest.raises(NoResultFound):
        mock_session.get_one(Task, task.id)