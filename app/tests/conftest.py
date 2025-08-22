import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from main import app
from services.tasks_services import TaskCreationService, TaskSearchService, TaskModificationService, TaskDeleteService
from services.status_services import CreateStatusService, SearchStatusService, UpdateStatusService, DeleteStatusService
from api.deps.db_dependency import get_db
from db.entities.models import Base

@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:?check_same_thread=False", echo=False)

@pytest.fixture(scope="session")
def create_tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture
def mock_session(engine, create_tables):
    conn = engine.connect()
    transaction = conn.begin()
    Session = sessionmaker(bind=conn)
    session = Session()
    yield session
    session.close()
    transaction.rollback()
    conn.close()

@pytest.fixture
def task_creation_service(mock_session):
    return TaskCreationService(mock_session)

@pytest.fixture
def task_search_service(mock_session):
    return TaskSearchService(mock_session)

@pytest.fixture
def task_modification_service(mock_session):
    return TaskModificationService(mock_session)

@pytest.fixture
def task_delete_service(mock_session):
    return TaskDeleteService(mock_session)

@pytest.fixture
def create_status_service(mock_session):
    return CreateStatusService(mock_session)

@pytest.fixture
def search_status_service(mock_session):
    return SearchStatusService(mock_session)

@pytest.fixture
def update_status_service(mock_session):
    return UpdateStatusService(mock_session)

@pytest.fixture
def delete_status_service(mock_session):
    return DeleteStatusService(mock_session)

@pytest.fixture(scope="function")
def api_client(mock_session):

    def override_get_db():
        try:
            yield mock_session
        finally:
            mock_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client