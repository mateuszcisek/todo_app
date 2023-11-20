import os

from django.conf import settings
from mongoengine import connect


class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.

    Credits: https://refactoring.guru/design-patterns/singleton/python/example
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class DocumentStoreConnection(metaclass=SingletonMeta):
    """Document store connection handler.

    It's implemented as a singleton to make sure only one document store connection is
    active.
    """

    def __init__(self):
        kwargs = {"serverSelectionTimeoutMS": 1000}

        if os.getenv("TODO_TEST_SESSION", "False") == "True":
            # We set TODO_TEST_SESSION when we run the tests with pytest.
            # If that value is True then we use a mock MongoClient class.
            import mongomock

            kwargs["mongo_client_class"] = mongomock.MongoClient

        self.client = connect(
            host="mongodb://%s:%s@%s:%d/%s?authSource=admin"
            % (
                settings.DOCUMENT_STORE_USER,
                settings.DOCUMENT_STORE_PASSWORD,
                settings.DOCUMENT_STORE_HOST,
                settings.DOCUMENT_STORE_PORT,
                settings.DOCUMENT_STORE_NAME,
            ),
            **kwargs,
        )
