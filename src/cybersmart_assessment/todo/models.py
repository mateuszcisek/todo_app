from django.utils import timezone
from mongoengine import (
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    FloatField,
    StringField,
)

from cybersmart_assessment.system.document_store import DocumentStoreConnection
from cybersmart_assessment.todo.colors import get_task_css_classes

DocumentStoreConnection()


class Location(EmbeddedDocument):
    """Location data document.

    It's supposed to be used as an embedded document in the Task document.
    """

    lat = FloatField(required=True)
    lon = FloatField(required=True)
    label = StringField(required=True)


class Weather(EmbeddedDocument):
    """Weather information document.

    It's supposed to be used as an embedded document in the Task document.
    """

    main = StringField(required=True)
    temperature = FloatField(required=True)


class Task(Document):
    """Todo item document model."""

    content = StringField(required=True)
    location = EmbeddedDocumentField(Location, required=True)
    weather = EmbeddedDocumentField(Weather)
    created_at = DateTimeField()
    marked_as_done_at = DateTimeField()

    @property
    def css_classes(self) -> str:
        """CSS classes for the task."""
        return get_task_css_classes(self)

    def save(self, *args, **kwargs):
        """Update the created_at datetime if it's not yet set."""
        if not self.created_at:
            self.created_at = timezone.now()

        return super().save(*args, **kwargs)
