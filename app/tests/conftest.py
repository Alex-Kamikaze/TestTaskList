import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.tasks_services import TaskCreationService, TaskSearchService, TaskModificationService, TaskDeleteService
from services.status_services import CreateStatusService, SearchStatusService, UpdateStatusService, DeleteStatusService
from db.entities.models import Base

@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:", echo=False)

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