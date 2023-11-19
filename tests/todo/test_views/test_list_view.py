import pytest
from django.urls import reverse

URL = reverse("todo:task-list")


@pytest.mark.usefixtures("create_active_tasks")
@pytest.mark.usefixtures("create_finished_tasks")
def test_with_active_and_finished_tasks(client):
    """
    Given active and finished tasks exist
    When we get a response from the task list view
    Then the response contains correct data.
    """
    response = client.get(URL)

    assert response.status_code == 200
    content = str(response.content)

    assert "No tasks to display" not in content

    assert "Active tasks" in content
    assert len(response.context_data["active_tasks"]) == 5
    assert all(
        task.marked_as_done_at is None for task in response.context_data["active_tasks"]
    )

    assert "Finished tasks" in content
    assert len(response.context_data["finished_tasks"]) == 5
    assert all(
        task.marked_as_done_at is not None
        for task in response.context_data["finished_tasks"]
    )


@pytest.mark.usefixtures("create_active_tasks")
def test_with_active_tasks(client):
    """
    Given active tasks exist
    When we get a response from the task list view
    Then the response contains correct data.
    """
    response = client.get(URL)

    assert response.status_code == 200
    content = str(response.content)

    assert "No tasks to display" not in content

    assert "Active tasks" in content
    assert len(response.context_data["active_tasks"]) == 5
    assert all(
        task.marked_as_done_at is None for task in response.context_data["active_tasks"]
    )

    assert "Finished tasks" not in content
    assert not response.context_data["finished_tasks"]


@pytest.mark.usefixtures("create_finished_tasks")
def test_with_finished_tasks(client):
    """
    Given finished tasks exist
    When we get a response from the task list view
    Then the response contains correct data.
    """
    response = client.get(URL)

    assert response.status_code == 200
    content = str(response.content)

    assert "No tasks to display" not in content

    assert "Active tasks" not in content
    assert not response.context_data["active_tasks"]

    assert "Finished tasks" in content
    assert len(response.context_data["finished_tasks"]) == 5
    assert all(
        task.marked_as_done_at is not None
        for task in response.context_data["finished_tasks"]
    )


def test_without_tasks(client):
    """
    Given no tasks exist
    When we get a response from the task list view
    Then the response does not contain information about any tasks.
    """
    response = client.get(URL)

    assert response.status_code == 200
    content = str(response.content)

    assert "No tasks to display" in content

    assert "Active tasks" not in content
    assert not response.context_data["active_tasks"]

    assert "Finished tasks" not in content
    assert not response.context_data["finished_tasks"]
