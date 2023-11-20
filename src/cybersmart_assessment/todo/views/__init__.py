from cybersmart_assessment.todo.views.create import TaskCreateView
from cybersmart_assessment.todo.views.edit import TaskEditView
from cybersmart_assessment.todo.views.list import TaskListView
from cybersmart_assessment.todo.views.mark_as_active import mark_as_active_view
from cybersmart_assessment.todo.views.mark_as_finished import mark_as_finished_view

__all__ = [
    "mark_as_finished_view",
    "mark_as_active_view",
    "TaskCreateView",
    "TaskEditView",
    "TaskListView",
]
