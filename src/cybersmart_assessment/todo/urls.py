from django.urls import re_path

from cybersmart_assessment.todo.views import TodoListView

urlpatterns = [
    re_path(r"^$", TodoListView.as_view(), name="task-list"),
]
