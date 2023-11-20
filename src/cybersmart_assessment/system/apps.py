from django.apps import AppConfig


class SystemConfig(AppConfig):
    """System app configuration."""

    name = "cybersmart_assessment.system"

    def ready(self):
        """Import the Celery signals."""
        import cybersmart_assessment.system.celery.signals  # noqa: F401
