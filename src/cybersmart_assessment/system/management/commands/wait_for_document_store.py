import sys
import time

from django.conf import settings
from django.core.management.base import BaseCommand
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


class Command(BaseCommand):
    """Wait until the document store is ready to be used.

    If it's not available for the number of seconds defined in the timeout variable
    then the command fails.
    """

    help = "Pause execution until document store is available."
    requires_system_checks = []

    def add_arguments(self, parser):  # noqa: D102
        parser.add_argument(
            "--timeout",
            help=(
                "The amount of time to wait for the document store connection"
                " in seconds. Default: 120."
            ),
            metavar="value",
            default=120,
            type=float,
        )

    def handle(self, *args, **options):  # noqa: D102
        is_connected = None
        start_time = time.perf_counter()
        self.stdout.write(self.style.WARNING("Waiting for the document store..."))

        while (
            not is_connected and time.perf_counter() - start_time <= options["timeout"]
        ):
            try:
                client = MongoClient(
                    "mongodb://%s:%s@%s:%d/%s?authSource=admin"
                    % (
                        settings.DOCUMENT_STORE_USER,
                        settings.DOCUMENT_STORE_PASSWORD,
                        settings.DOCUMENT_STORE_HOST,
                        settings.DOCUMENT_STORE_PORT,
                        settings.DOCUMENT_STORE_NAME,
                    ),
                    serverSelectionTimeoutMS=1000,
                )
                client.server_info()
                is_connected = True
            except ServerSelectionTimeoutError:
                self.stdout.write(
                    self.style.WARNING(
                        "Document store unavailable, waiting 1 second..."
                    )
                )
                time.sleep(1)

        if is_connected:
            self.stdout.write(self.style.SUCCESS("Document store available!"))
        else:
            self.stderr.write(self.style.ERROR("Document store connection failed!"))
            sys.exit(1)
