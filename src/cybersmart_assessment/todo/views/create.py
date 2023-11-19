from typing import Any

from django.conf import settings
from django.forms.models import BaseModelForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView

from cybersmart_assessment.todo.forms import TaskCreateForm
from cybersmart_assessment.todo.models import Task
from cybersmart_assessment.todo.utils import get_location_from_string


class TaskCreateView(FormView):
    """Return a view with a list of Task entries."""

    form_class = TaskCreateForm
    template_name = "task/create.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add te Weather API key to the view context."""
        result = super().get_context_data(**kwargs)
        result["api_key"] = settings.WEATHER_API_KEY
        return result

    def form_valid(self, form: BaseModelForm) -> HttpResponseRedirect:
        """Add a new task  and redirect the user to the list of tasks."""
        location = get_location_from_string(form["location"].value())
        Task.objects.create(content=form["content"].value(), location=location)

        return HttpResponseRedirect(reverse("todo:task-list"))
