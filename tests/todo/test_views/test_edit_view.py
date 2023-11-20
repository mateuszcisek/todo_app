import pytest
from cybersmart_assessment.todo.models import Task
from django.urls import reverse

URL_PATH = "todo:task-edit"


def test_task_updated_successfully(client, task):
    """
    Given an existing task
    And correct task data
    When we perform a POST request using the data and a valid URL
    Then the task is updated
    And the user is redirected to the list of tasks.
    """
    assert Task.objects.count() == 1

    url = reverse(URL_PATH, kwargs={"task_id": str(task.id)})

    response = client.post(
        url,
        data={
            "task_id": task.id,
            "content": "sample task",
            "location": "1.0::2.0::Sample location",
        },
    )

    assert response.status_code == 302
    assert response["Location"] == reverse("todo:task-list")

    updated_task = Task.objects.first()

    assert updated_task.id == task.id
    assert updated_task.content == "sample task"
    assert updated_task.location.lat == 1.0
    assert updated_task.location.lon == 2.0
    assert updated_task.location.label == "Sample location"


def test_with_no_content(client, task):
    """
    Given an existing task
    And task data without the content
    When we perform a POST request using the data and a valid URL
    Then the task is not updated
    And an appropriate error message is displayed.
    """
    assert Task.objects.count() == 1

    url = reverse(URL_PATH, kwargs={"task_id": str(task.id)})

    response = client.post(
        url,
        data={
            "task_id": task.id,
            "location": "1.0::2.0::Sample location",
        },
    )

    assert response.status_code == 200

    content = str(response.content)
    assert "Task content: This field is required." in content


def test_with_no_location(client, task):
    """
    Given an existing task
    And task data without the location
    When we perform a POST request using the data and a valid URL
    Then the task is not updated
    And an appropriate error message is displayed.
    """
    assert Task.objects.count() == 1

    url = reverse(URL_PATH, kwargs={"task_id": str(task.id)})

    response = client.post(
        url,
        data={
            "task_id": task.id,
            "content": "sample task",
        },
    )

    assert response.status_code == 200

    content = str(response.content)
    assert "Location: This field is required." in content


def test_with_no_task_id(client, task):
    """
    Given an existing task
    And task data without the task ID
    When we perform a POST request using the data and a valid URL
    Then the task is not updated
    And an appropriate error message is displayed.
    """
    assert Task.objects.count() == 1

    url = reverse(URL_PATH, kwargs={"task_id": str(task.id)})

    response = client.post(
        url,
        data={
            "content": "sample task",
            "location": "1.0::2.0::Sample location",
        },
    )

    assert response.status_code == 200

    content = str(response.content)
    assert "Task id: This field is required." in content


@pytest.mark.parametrize("value", ("1", "1::2", "a::b", "1::b::c"))
def test_with_incorrect_location(client, task, value):
    """
    Given an existing task
    And task data with incorrect location
    When we perform a POST request using the data and a valid URL
    Then the task is not updated
    And an appropriate error message is displayed.
    """
    assert Task.objects.count() == 1

    url = reverse(URL_PATH, kwargs={"task_id": str(task.id)})

    response = client.post(
        url,
        data={
            "task_id": task.id,
            "content": "sample content",
            "location": value,
        },
    )

    assert response.status_code == 200

    content = str(response.content)
    assert "Location: The value is incorrect." in content


def test_with_incorrect_task_id(client, task):
    """
    Given an existing task
    And task data with incorrect task ID
    When we perform a POST request using the data and a valid URL
    Then the task is not updated
    And an appropriate error message is displayed.
    """
    assert Task.objects.count() == 1

    url = reverse(URL_PATH, kwargs={"task_id": str(task.id)})

    response = client.post(
        url,
        data={
            "task_id": "incorrect-id",
            "content": "sample content",
            "location": "1.0::2.0::Sample location",
        },
    )

    assert response.status_code == 200

    content = str(response.content)
    assert "Task id: The task with the given ID does not exist." in content


def test_open_page_with_incorrect_task_id(client):
    """
    When we perform a GET request using a URL with an incorrect task ID.
    And the user is redirected to the list of tasks.
    """
    url = reverse(URL_PATH, kwargs={"task_id": "123456789012345678901234"})

    response = client.get(url)

    assert response.status_code == 302
    assert response["Location"] == reverse("todo:task-list")


def test_open_page_with_correct_task_id(client, task):
    """
    When we perform a GET request using a URL with a correct task ID.
    And the page is displayed.
    """
    url = reverse(URL_PATH, kwargs={"task_id": task.id})

    response = client.get(url)

    assert response.status_code == 200
