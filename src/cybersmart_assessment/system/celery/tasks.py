import logging

import requests
from celery.schedules import crontab
from django.conf import settings

from cybersmart_assessment.system.celery.app import app

logger = logging.getLogger("celeryapp")


def update_weather_for_task(task) -> None:
    """Update the weather data for the specified task.

    Args:
        task (cybersmart_assessment.todo.models.Task): Task to update the weather for.
    """
    from cybersmart_assessment.todo.models import Weather

    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "lat": str(task.location.lat),
        "lon": str(task.location.lon),
        "appid": settings.WEATHER_API_KEY,
        "units": "metric",
    }
    response = requests.get(url, params=params)
    if response.status_code != 200:
        logger.error(
            "Weather for task %s has not been updated. The response with status code %d"
            "has been received.",
            str(task.id),
            response.status_code,
        )
        return

    data = response.json()
    # It is possible to meet more than one weather condition for a requested location.
    # The first weather condition in API respond is primary and this is what we use.
    task.weather = Weather(
        main=data["weather"][0]["main"],
        temperature=data["main"]["temp"],
    )
    task.save()


def update_weather_for_active_tasks() -> None:
    """Update the weather data for all active tasks."""
    from cybersmart_assessment.todo.models import Task

    for task in Task.objects.filter(marked_as_done_at=""):
        update_weather_for_task(task)


@app.task
def update_weather_for_active_tasks_task():
    """Celery task that updates the weather data for all active tasks."""
    update_weather_for_active_tasks()  # pragma: no cover


# This dictionary can be used to define scheduled tasks which will be
# automatically executed in defined time periods. Here is a sample definition:
#
#     SCHEDULED_TASKS = {
#         "task_name": (
#             interval_between_executions_in_seconds,
#             task_function,
#             arguments
#         )
#     }
#
# Parameter interval_between_executions_in_seconds can be replaced eg. by
# crontab, for example
#
#     SCHEDULED_TASKS = {
#         "task_name": (
#             crontab(hour=1, minute=30, day_of_week="*"),
#             task_function,
#             arguments
#         )
#     }
#
# The task above will be executed every day at 01:30 in the morning.
#
# Here is a sample task definition:
#
#     @app.task
#     def sample_task(arg):
#         logger.info("arg %s", str(arg))
#
# Given the task above, in order to execute it every 60 seconds with number `1`
# as the only parameter, the following entry can be added to SCHEDULED_TASKS:
#
#     SCHEDULED_TASKS = {
#         "sample_task": (60, sample_task, [1])
#     }
#
SCHEDULED_TASKS = {
    "update_weather_for_active_tasks_task": (
        crontab(),  # Execute every minute
        update_weather_for_active_tasks_task,
        [],
    ),
}
