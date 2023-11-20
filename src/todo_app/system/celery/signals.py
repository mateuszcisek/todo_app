import logging

from celery.signals import (
    setup_logging,
    task_failure,
    task_success,
)
from django.conf import settings

from todo_app.system.celery.app import app
from todo_app.system.celery.tasks import SCHEDULED_TASKS
from todo_app.system.celery.utils import get_log_prefix

logger = logging.getLogger("celeryapp")


@setup_logging.connect
def setup_loggers(*args, **kwargs):  # pragma: no cover
    """Configure the loggers."""
    logging.config.dictConfig(settings.LOGGING)


@task_failure.connect
def on_task_failure(sender, **kwargs):  # pragma: no cover
    """Handle failed tasks."""
    logger.debug("%s - Failed", get_log_prefix(sender))
    exception = kwargs.get("exception")
    if exception:
        logger.exception(exception)


@task_success.connect
def on_task_success(sender, **kwargs):  # pragma: no cover
    """Handle successfully finished tasks."""
    logger.debug("%s - Success", get_log_prefix(sender))


@app.on_after_finalize.connect
def setup_scheduled_tasks(sender, **kwargs):  # pragma: no cover
    """Register celery periodic tasks."""
    try:
        for key, (delay, func, args) in SCHEDULED_TASKS.items():
            sender.add_periodic_task(delay, func.s(*args), name=key)
            logger.debug('Periodic task "%s" has been registered', key)
    except Exception as ex:
        logger.exception(ex)
