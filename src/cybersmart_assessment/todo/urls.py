from django.urls import re_path

from cybersmart_assessment.todo.views import TaskCreateView, TaskListView

urlpatterns = [
    re_path(r"^$", TaskListView.as_view(), name="task-list"),
    re_path(r"^create/$", TaskCreateView.as_view(), name="task-create"),
]
