from django.apps import AppConfig


class SystemConfig(AppConfig):
    """System app configuration."""

    name = "todo_app.system"

    def ready(self):
        """Import the Celery signals."""
        import todo_app.system.celery.signals  # noqa: F401
