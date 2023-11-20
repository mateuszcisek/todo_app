import pytest
from cybersmart_assessment.todo.models import Task
from django.urls import reverse

URL_PATH = "todo:mark-task-as-finished"


def test_task_marked_as_finished_successfully(client, task):
    """
    Given a correct task ID
    When we perform a GET request using the ID and a valid URL
    Then the task is marked as finished
    And the user is redirected to the list of tasks.
    """
    task.marked_as_done_at = None
    task.save()

    url = reverse(URL_PATH, kwargs={"task_id": task.id})

    response = client.get(url)

    assert response.status_code == 302
    assert response["Location"] == reverse("todo:task-list")

    updated_task = Task.objects.get(id=task.id)

    assert updated_task.marked_as_done_at is not None


def test_with_incorrect_task_id(client):
    """
    Given an incorrect task ID
    When we perform a GET request using the ID and a valid URL
    And the user is redirected to the list of tasks.
    """
    url = reverse(URL_PATH, kwargs={"task_id": "123456789012345678901234"})

    response = client.get(url)

    assert response.status_code == 302
    assert response["Location"] == reverse("todo:task-list")


@pytest.mark.parametrize("method", ("post", "put", "patch", "delete"))
def test_with_incorrect_http_method(client, task, method):
    """
    Given an incorrect task ID
    When we perform a request using the ID and a valid URL
    And the HTTP method of the request is incorrect
    And the user is redirected to the list of tasks.
    """
    task.marked_as_done_at = None
    task.save()

    url = reverse(URL_PATH, kwargs={"task_id": task.id})

    response = client.request(method=method, url=url)

    assert response.status_code == 301
    assert response["Location"] == reverse("todo:task-list")

    not_updated_task = Task.objects.get(id=task.id)

    assert not_updated_task.marked_as_done_at is None
