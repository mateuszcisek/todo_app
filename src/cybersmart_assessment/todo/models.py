from mongoengine import (
    DateTimeField,
    Document,
    EmbeddedDocument,
    EmbeddedDocumentField,
    FloatField,
    StringField,
)

from cybersmart_assessment.system.document_store import DocumentStoreConnection

DocumentStoreConnection()


class Location(EmbeddedDocument):
    """Location data document.

    It's supposed to be used as an embedded document in the TodoItem document.
    """

    lat = FloatField(required=True)
    lon = FloatField(required=True)
    label = StringField(required=True)


class Weather(EmbeddedDocument):
    """Weather information document.

    It's supposed to be used as an embedded document in the TodoItem document.
    """

    main = StringField(required=True)
    code = FloatField(required=True)
    updated_at = DateTimeField()


class TodoItem(Document):
    """Todo item document model."""

    content = StringField(required=True)
    location = EmbeddedDocumentField(Location, required=True)
    weather = EmbeddedDocumentField(Weather)
    created_at = DateTimeField()
    marked_as_done_at = DateTimeField()
