import pytest
import json
from sqlalchemy.exc import NoResultFound
from db.entities.models import Status
from .factories import StatusDbModelFactory

def test_status_creation_endpoint(api_client, mock_session):
    resp = api_client.put("/status/create?status_name=test")
    assert resp.status_code == 201

    status = mock_session.query(Status).filter_by(name="test").one_or_none()
    assert status is not None
    assert status.name == "test"

def test_search_endpoint_with_incorrect_id(api_client):
    resp = api_client.get("/status/get?status_id=0")
    assert resp.status_code == 404

def test_search_endpoint_with_correct_id(api_client, mock_session):
    status = StatusDbModelFactory(id=1)
    mock_session.add(status)
    mock_session.commit()

    resp = api_client.get("/status/get?status_id=1")
    text = json.loads(resp.text)

    assert resp.status_code == 200
    assert text.get("id") == 1
    assert text.get("name") == "В работе"

def test_list_endpoint_with_empty_base(api_client):

    resp = api_client.get("/status/get_all_statuses")
    text = json.loads(resp.text)

    assert resp.status_code == 200
    assert text == []

def test_list_endpoint_with_correct_statuses(api_client, mock_session):
    status = StatusDbModelFactory()

    mock_session.add(status)
    mock_session.commit()

    resp = api_client.get("/status/get_all_statuses")
    text = json.loads(resp.text)

    assert resp.status_code == 200
    assert len(text) == 1

def test_update_endpoint_with_incorrect_status(api_client):
    resp = api_client.patch("/status/update", json={"id": 0, "name": "test"})

    assert resp.status_code == 404

def test_update_endpoint_with_correct_status(api_client, mock_session):
    status = StatusDbModelFactory()
    
    mock_session.add(status)
    mock_session.commit()

    resp = api_client.patch("/status/update", json={"id": status.id, "name": "update"})

    updated_status = mock_session.query(Status).filter_by(id=1).one_or_none()

    assert resp.status_code == 200
    assert updated_status is not None
    assert updated_status.name == "update"

def test_delete_endpoint_with_incorrect_id(api_client):

    resp = api_client.delete("/status/delete?status_id=0")
    assert resp.status_code == 404

def test_delete_endpoint_with_correct_status(api_client, mock_session):
    status = StatusDbModelFactory()
    mock_session.add(status)
    mock_session.commit()

    resp = api_client.delete(f"/status/delete?status_id={status.id}")
    assert resp.status_code == 200

    with pytest.raises(NoResultFound):
        mock_session.get_one(Status, 1)