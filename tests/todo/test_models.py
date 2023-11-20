import pytest
from cybersmart_assessment.todo.models import Location, Task, Weather
from mongoengine.errors import ValidationError


def test_creating_task():
    """
    Given a task content, location and weather defined
    When we create a task using that data
    Then the task with correct data is created.
    """
    task = Task.objects.create(
        content="sample task",
        location=Location(lat=0, lon=0, label="sample location"),
        weather=Weather(main="Snow", temperature=0.0),
    )

    assert task.id is not None

    new_task = Task.objects.get(id=task.id)

    assert new_task.content == "sample task"
    assert new_task.created_at is not None
    assert new_task.location.lat == 0
    assert new_task.location.lon == 0
    assert new_task.location.label == "sample location"
    assert new_task.weather.main == "Snow"


def test_creating_task_without_location():
    """
    Given a task data without location
    When we create a task using that data
    Then a ValidationError is raised.
    """
    with pytest.raises(ValidationError):
        Task.objects.create(
            content="sample task",
            weather=Weather(main="Snow", temperature=0.0),
        )


def test_creating_task_without_weather():
    """
    Given a task content and location defined
    When we create a task using that data
    Then the task with correct data is created
    And the weather is not defined in the task.
    """
    task = Task.objects.create(
        content="sample task",
        location=Location(lat=0, lon=0, label="sample location"),
    )

    assert task.id is not None

    new_task = Task.objects.get(id=task.id)

    assert new_task.content == "sample task"
    assert new_task.created_at is not None
    assert new_task.location.lat == 0
    assert new_task.location.lon == 0
    assert new_task.location.label == "sample location"
    assert new_task.weather is None


def test_task_created_at_changes_only_once():
    """
    Given a task
    When we update the task
    Then the created_at datetime does not change.
    """
    task = Task.objects.create(
        content="sample task",
        location=Location(lat=0, lon=0, label="sample location"),
    )

    created_at = task.created_at

    task.content = "another task"
    task.save()

    assert task.created_at == created_at
