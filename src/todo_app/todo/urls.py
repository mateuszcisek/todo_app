from django.urls import re_path

from todo_app.todo.views import (
    TaskCreateView,
    TaskEditView,
    TaskListView,
    mark_as_active_view,
    mark_as_finished_view,
)

urlpatterns = [
    re_path(r"^$", TaskListView.as_view(), name="task-list"),
    re_path(r"^create/$", TaskCreateView.as_view(), name="task-create"),
    re_path(
        r"^edit/(?P<task_id>[a-f0-9]{24})$", TaskEditView.as_view(), name="task-edit"
    ),
    re_path(
        r"^mark-as-active/(?P<task_id>[a-f0-9]{24})$",
        mark_as_active_view,
        name="mark-task-as-active",
    ),
    re_path(
        r"^mark-as-finished/(?P<task_id>[a-f0-9]{24})$",
        mark_as_finished_view,
        name="mark-task-as-finished",
    ),
]
