from todo_app.todo.views.create import TaskCreateView
from todo_app.todo.views.edit import TaskEditView
from todo_app.todo.views.list import TaskListView
from todo_app.todo.views.mark_as_active import mark_as_active_view
from todo_app.todo.views.mark_as_finished import mark_as_finished_view

__all__ = [
    "mark_as_finished_view",
    "mark_as_active_view",
    "TaskCreateView",
    "TaskEditView",
    "TaskListView",
]
