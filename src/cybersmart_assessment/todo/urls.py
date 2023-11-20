from django.urls import re_path

from cybersmart_assessment.todo.views import TaskCreateView, TaskEditView, TaskListView

urlpatterns = [
    re_path(r"^$", TaskListView.as_view(), name="task-list"),
    re_path(r"^create/$", TaskCreateView.as_view(), name="task-create"),
    re_path(
        r"^edit/(?P<task_id>[a-f0-9]{24})$", TaskEditView.as_view(), name="task-edit"
    ),
]
