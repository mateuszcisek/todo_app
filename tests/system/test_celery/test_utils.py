from unittest.mock import Mock

import pytest
from cybersmart_assessment.system.celery.utils import (
    get_log_prefix,
    get_task_id,
    get_task_name,
)


def _get_mock_sender() -> Mock:
    """Return a mock Celery task."""
    result = Mock()
    result.name = "sample.task.name"
    return result


@pytest.mark.parametrize(
    "kwargs, expected_result",
    (
        (
            {
                "headers": {
                    "id": "sample-task-id",
                },
            },
            "sample-task-id",
        ),
        (
            {"sender": "sample-id"},
            "sample-id",
        ),
        (
            {"sender": Mock(request=Mock(root_id=None, id="id"))},
            "id",
        ),
        (
            {"sender": Mock(request=Mock(id=None, root_id="root-id"))},
            "root-id",
        ),
    ),
)
def test_get_task_id(kwargs, expected_result):
    """
    Given Celery task parameters
    When we call function get_task_id
    Then we get a correct task ID.
    """
    assert get_task_id(**kwargs) == expected_result


@pytest.mark.parametrize(
    "sender, expected_result",
    (
        (None, None),
        ("sample.task.name", "name"),
        (_get_mock_sender(), "name"),
        ({"task"}, {"task"}),
    ),
)
def test_get_task_name(sender, expected_result):
    """
    Given Celery task object
    When we call function get_task_name
    Then we get a correct task name.
    """
    assert get_task_name(sender) == expected_result


@pytest.mark.parametrize(
    "task, task_name, task_id, expected_task_name, expected_task_id",
    (
        (None, "sample_name", "sample_id", "sample_name", "sample_id"),
        ("sample.task.name", None, "sample_id", "name", "sample_id"),
        (_get_mock_sender(), None, "sample_id", "name", "sample_id"),
        (
            Mock(request=Mock(id=None, root_id="root-id")),
            "sample_name",
            None,
            "sample_name",
            "root-id",
        ),
        (
            Mock(request=Mock(root_id=None, id="id")),
            "sample_name",
            None,
            "sample_name",
            "id",
        ),
    ),
)
def test_get_log_prefix(task, task_name, task_id, expected_task_name, expected_task_id):
    """
    Given a task object, task name, and task ID
    When we call get_log_prefix
    Then we get a correct result.
    """
    result = get_log_prefix(task, task_name=task_name, task_id=task_id)

    assert result == f"Task name: {expected_task_name}, task ID: {expected_task_id}"
