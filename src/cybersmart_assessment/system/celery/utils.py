from typing import Any


def get_task_id(**kwargs) -> str:
    """Retrieve and return the uuid from celery task."""
    headers = kwargs.get("headers", {})
    task_id = headers.get("id")

    if task_id:
        return task_id

    sender = kwargs.get("sender")

    try:
        return sender.request.root_id or sender.request.id
    except AttributeError:
        return sender


def get_task_name(sender) -> str:
    """Return the actual task name without any prefix."""
    if not sender:
        return None

    if isinstance(sender, str):
        return sender.split(".")[-1]

    try:
        return sender.name.split(".")[-1]
    except AttributeError:
        return sender


def get_log_prefix(task, *, task_name: Any = None, task_id: Any = None):
    """Return a prefix for the log message.

    The format of the messages logged by the tasks should be consistent. This function
    returns the prefix for the messages, which contains task name and task ID.
    """
    _task_name = task_name if task_name else get_task_name(sender=task)
    _task_id = task_id if task_id else get_task_id(sender=task)

    return f"Task name: {_task_name}, task ID: {_task_id}"
