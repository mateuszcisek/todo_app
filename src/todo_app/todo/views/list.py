from typing import Any

from django.db.models.query import QuerySet
from django.views.generic import ListView

from todo_app.todo.models import Task


class TaskListView(ListView):
    """Return a view with a list of Task entries."""

    template_name = "task/list.html"

    def get_queryset(self) -> QuerySet[Any]:
        """Return the list of Task objects"""
        return Task.objects.all()

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """Add additional context to the view.

        We want to be able to distinguish between active and finished tasks. Both those
        collections will be available as separate variables in the view so it's easier
        to display them.
        """
        result = super().get_context_data(**kwargs)

        all_tasks = self.get_queryset()
        result["active_tasks"] = all_tasks.filter(marked_as_done_at="").order_by(
            "-created_at"
        )
        result["finished_tasks"] = all_tasks.filter(marked_as_done_at__ne="").order_by(
            "-marked_as_done_at"
        )

        return result
