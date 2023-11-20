from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from mongoengine.errors import ValidationError

from todo_app.todo.models import Task


@require_http_methods(["GET"])
def mark_as_active_view(request: HttpRequest, task_id: str) -> HttpResponseRedirect:
    """View for marking a task with given ID as active.

    Whether the operation succeeds or fails, the user will be redirected to the view
    with the list of tasks.

    Args:
        request (HttpRequest): The request to process.
        task_id (str): The ID of the task to mark as active.

    Returns:
        HttpResponseRedirect: Redirection to the view with the list of tasks.
    """
    response = HttpResponseRedirect(reverse("todo:task-list"))

    try:
        task = Task.objects.get(id=task_id)
    except (ValidationError, Task.DoesNotExist):
        return response

    task.marked_as_done_at = None
    task.save()

    return response
