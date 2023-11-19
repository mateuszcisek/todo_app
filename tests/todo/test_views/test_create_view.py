import pytest
from cybersmart_assessment.todo.models import Task
from django.urls import reverse

URL = reverse("todo:task-create")


def test_task_created_successfully(client):
    """
    Given correct task data
    When we perform a POST request using the data and a valid URL
    Then a new task is created
    And the user is redirected to the list of tasks.
    """
    assert not Task.objects.all()

    response = client.post(
        URL,
        data={
            "content": "sample task",
            "location": "1.0::2.0::Sample location",
        },
    )

    assert response.status_code == 302
    assert response["Location"] == reverse("todo:task-list")

    task = Task.objects.first()

    assert task is not None
    assert task.content == "sample task"
    assert task.location.lat == 1.0
    assert task.location.lon == 2.0
    assert task.location.label == "Sample location"


def test_with_no_content(client):
    """
    Given task data without the content
    When we perform a POST request using the data and a valid URL
    Then a new task is not created
    And an appropriate error message is displayed.
    """
    assert not Task.objects.all()

    response = client.post(
        URL,
        data={
            "content": "",
            "location": "1.0::2.0::Sample location",
        },
    )

    assert not Task.objects.all()
    assert response.status_code == 200

    content = str(response.content)
    assert "Task content: This field is required." in content


def test_with_no_location(client):
    """
    Given task data without the location
    When we perform a POST request using the data and a valid URL
    Then a new task is not created
    And an appropriate error message is displayed.
    """
    assert not Task.objects.all()

    response = client.post(
        URL,
        data={
            "content": "sample content",
            "location": "",
        },
    )

    assert not Task.objects.all()
    assert response.status_code == 200

    content = str(response.content)
    assert "Location: This field is required." in content


@pytest.mark.parametrize("value", ("1", "1::2", "a::b", "1::b::c"))
def test_with_incorrect_location(client, value):
    """
    Given task data with incorrect location
    When we perform a POST request using the data and a valid URL
    Then a new task is not created
    And an appropriate error message is displayed.
    """
    assert not Task.objects.all()

    response = client.post(
        URL,
        data={
            "content": "sample content",
            "location": value,
        },
    )

    assert not Task.objects.all()
    assert response.status_code == 200

    content = str(response.content)
    assert "Location: The value is incorrect." in content
