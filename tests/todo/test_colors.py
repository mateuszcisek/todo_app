import pytest
from cybersmart_assessment.todo.colors import get_task_css_classes
from cybersmart_assessment.todo.models import Location, Task, Weather


def _get_task(temperature: float, main: str) -> Task:
    return Task(
        content="sample task",
        location=Location(lat=0, lon=0, label="sample location"),
        weather=Weather(temperature=temperature, main=main)
        if temperature is not None or main is not None
        else None,
    )


@pytest.mark.parametrize(
    "task, expected_result",
    (
        (_get_task(None, None), "border"),
        (_get_task(-10, "Rain"), "border-indigo bg-indigo-100"),
        (_get_task(-10, "Clouds"), "border-indigo bg-indigo-100"),
        (_get_task(-10, "Clear"), "border-indigo bg-indigo-100"),
        (_get_task(0, "Rain"), "border-indigo bg-indigo-100"),
        (_get_task(0, "Clouds"), "border-orange bg-orange-100"),
        (_get_task(0, "Clear"), "border-orange bg-orange-100"),
        (_get_task(10, "Rain"), "border-indigo bg-indigo-100"),
        (_get_task(10, "Clouds"), "border-orange bg-orange-100"),
        (_get_task(10, "Clear"), "border-orange bg-orange-100"),
        (_get_task(20, "Rain"), "border-indigo bg-indigo-100"),
        (_get_task(20, "Clouds"), "border-orange bg-orange-100"),
        (_get_task(20, "Clear"), "border-red bg-red-100"),
    ),
)
def test_get_task_css_classes(task, expected_result):
    """
    Given task with (or without) weather data
    When we get CSS classes for that task using function get_task_css_classes
    Then we get a correct result.
    """
    assert get_task_css_classes(task) == expected_result
