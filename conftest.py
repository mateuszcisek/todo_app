import pytest
from cybersmart_assessment.system.document_store import DocumentStoreConnection
from cybersmart_assessment.todo.models import Location, Task, Weather
from django.utils import timezone


@pytest.fixture(autouse=True)
def clear_document_store():
    """Remove all collections from the document store before each test."""
    db = DocumentStoreConnection().client.get_database()
    for name in db.list_collection_names():
        db.drop_collection(name)


@pytest.fixture(name="task")
def task_fixture():
    """Create and return a sample task."""
    return Task.objects.create(
        content="Sample task",
        location=Location(lat=10, lon=20, label="Sample location"),
        weather=Weather(main="Snow", temperature=0.0),
    )


@pytest.fixture
def create_active_tasks():
    """Create sample active tasks."""
    for index in range(5):
        Task.objects.create(
            content=f"Sample task {index}",
            location=Location(lat=index, lon=index, label=f"Location {index}"),
            weather=Weather(main="Snow", temperature=0.0),
        )


@pytest.fixture
def create_finished_tasks():
    """Create sample active tasks."""
    for index in range(5):
        Task.objects.create(
            content=f"Finished task {index}",
            marked_as_done_at=timezone.now(),
            location=Location(lat=index, lon=index, label=f"Location {index}"),
            weather=Weather(main="Snow", temperature=0.0),
        )
