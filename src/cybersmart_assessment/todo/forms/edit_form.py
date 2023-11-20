from django import forms
from mongoengine.errors import ValidationError

from cybersmart_assessment.todo.forms.create_form import TaskCreateForm
from cybersmart_assessment.todo.models import Task


def validate_task_id(value: str):
    """Validate the task ID.

    The task ID is considered valid if a task with that ID exists in the document store.

    Args:
        value (str): Value to validate.

    Raises:
        forms.ValidationError: If the value is not a valid task ID.
    """
    try:
        Task.objects.get(id=value)
    except (ValidationError, Task.DoesNotExist) as ex:
        raise forms.ValidationError(
            "The task with the given ID does not exist."
        ) from ex


class TaskEditForm(TaskCreateForm):
    """Form for editing task objects."""

    task_id = forms.CharField(
        required=True,
        widget=forms.HiddenInput(),
        validators=[validate_task_id],
    )
