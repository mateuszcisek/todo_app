from django.urls import reverse


def test_homepage(client):
    """
    When we visit the homepage
    Then we are redirected to the list with tasks.
    """
    response = client.get(reverse("homepage"))

    assert response.status_code == 301
    assert response["Location"] == reverse("todo:task-list")
