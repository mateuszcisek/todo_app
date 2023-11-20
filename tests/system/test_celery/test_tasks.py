from unittest.mock import Mock, patch

import pytest
from django.conf import settings
from todo_app.system.celery.tasks import (
    update_weather_for_active_tasks,
    update_weather_for_task,
)
from todo_app.todo.models import Task

MODULE_PATH = "todo_app.system.celery.tasks"


def _mock_response(status_code: int, data: dict) -> Mock:
    """Return a mock HTTP response."""
    result = Mock(status_code=status_code)
    result.json.return_value = data
    return result


@patch(f"{MODULE_PATH}.requests.get")
def test_update_weather_for_task(mock_get, task):
    """
    Given an active task
    When we call update_weather_for_task for that task
    And we get a correct response
    Then the weather is updated for the task.
    """
    task.weather = None
    task.marked_as_done_at = None
    task.save()

    mock_get.return_value = _mock_response(
        200,
        {
            "weather": [{"main": "Snow"}],
            "main": {"temp": 10.0},
        },
    )

    update_weather_for_task(task)

    mock_get.assert_called_once_with(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "lat": str(task.location.lat),
            "lon": str(task.location.lon),
            "appid": settings.WEATHER_API_KEY,
            "units": "metric",
        },
    )

    updated_task = Task.objects.get(id=task.id)
    assert updated_task.weather.main == "Snow"
    assert updated_task.weather.temperature == 10.0


@patch(f"{MODULE_PATH}.requests.get")
def test_update_weather_for_task_with_incorrect_response(mock_get, task):
    """
    Given an active task
    When we call update_weather_for_task for that task
    And we get a wrong response
    Then the weather is not updated for the task.
    """
    task.weather = None
    task.marked_as_done_at = None
    task.save()

    mock_get.return_value = _mock_response(400, {})

    update_weather_for_task(task)

    mock_get.assert_called_once_with(
        "https://api.openweathermap.org/data/2.5/weather",
        params={
            "lat": str(task.location.lat),
            "lon": str(task.location.lon),
            "appid": settings.WEATHER_API_KEY,
            "units": "metric",
        },
    )

    not_updated_task = Task.objects.get(id=task.id)
    assert not_updated_task.weather is None


@pytest.mark.usefixtures("create_active_tasks")
@pytest.mark.usefixtures("create_finished_tasks")
@patch(f"{MODULE_PATH}.requests.get")
def test_update_weather_for_active_tasks(mock_get):
    """
    Given active and finished tasks
    When we call update_weather_for_active_tasks
    And we get a correct response
    Then the weather is updated for active tasks only.
    """
    for task in Task.objects.all():
        task.weather = None
        task.save()

    mock_get.return_value = _mock_response(
        200,
        {
            "weather": [{"main": "Snow"}],
            "main": {"temp": 10.0},
        },
    )

    update_weather_for_active_tasks()

    # Check if all active tasks have the weather updated
    assert all(
        task.weather is not None for task in Task.objects.filter(marked_as_done_at="")
    )

    # Check if all finished tasks have the weather not updated
    assert all(
        task.weather is None for task in Task.objects.filter(marked_as_done_at__ne="")
    )


@pytest.mark.usefixtures("create_active_tasks")
@pytest.mark.usefixtures("create_finished_tasks")
@patch(f"{MODULE_PATH}.requests.get")
def test_update_weather_for_active_tasks_with_incorrect_response(mock_get):
    """
    Given active and finished tasks
    When we call update_weather_for_active_tasks
    And we get a wrong response
    Then the weather is not updated for any task.
    """
    for task in Task.objects.all():
        task.weather = None
        task.save()

    mock_get.return_value = _mock_response(400, {})

    update_weather_for_active_tasks()

    assert all(task.weather is None for task in Task.objects.all())
