from typing import Any

from django.conf import settings
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView
from mongoengine.errors import ValidationError

from todo_app.todo.forms import TaskEditForm
from todo_app.todo.models import Task
from todo_app.todo.utils import get_location_from_string


class TaskEditView(FormView):
    """Return a view with a form for editing Task entries."""

    form_class = TaskEditForm
    template_name = "task/edit.html"

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        """Validate the task ID and perform the request if it's correct."""
        try:
            Task.objects.get(id=self.kwargs["task_id"])
        except (ValidationError, Task.DoesNotExist):
            return HttpResponseRedirect(reverse("todo:task-list"))

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add te Weather API key to the view context."""
        task = Task.objects.get(id=self.kwargs["task_id"])
        result = super().get_context_data(**kwargs)
        result["form"].initial = {"content": task.content, "task_id": task.id}
        result["default_location"] = task.location.to_json()
        result["api_key"] = settings.WEATHER_API_KEY
        return result

    def form_valid(self, form: BaseModelForm) -> HttpResponseRedirect:
        """Update the task and redirect the user to the list of tasks."""
        task = Task.objects.get(id=form["task_id"].value())
        task.content = form["content"].value()
        task.location = get_location_from_string(form["location"].value())
        task.save()

        return HttpResponseRedirect(reverse("todo:task-list"))
