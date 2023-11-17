import sys
import time

from django.core.management.base import BaseCommand
from django.db import connection
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Wait until the database is ready to be used.

    If it's not available for the number of seconds defined in the timeout variable
    then the command fails.
    """

    help = "Pause execution until database is available."
    requires_system_checks = []

    def add_arguments(self, parser):  # noqa: D102
        parser.add_argument(
            "--timeout",
            help=(
                "The amount of time to wait for the database connection in seconds."
                " Default: 120."
            ),
            metavar="value",
            default=120,
            type=float,
        )

    def handle(self, *args, **options):  # noqa: D102
        is_connected = None
        start_time = time.perf_counter()
        self.stdout.write(self.style.WARNING("Waiting for the database..."))

        while (
            not is_connected and time.perf_counter() - start_time <= options["timeout"]
        ):
            try:
                connection.ensure_connection()
                is_connected = True
            except OperationalError:
                self.stdout.write(
                    self.style.WARNING("Database unavailable, waiting 1 second...")
                )
                time.sleep(1)

        if is_connected:
            self.stdout.write(self.style.SUCCESS("Database available!"))
        else:
            self.stderr.write(self.style.ERROR("Database connection failed!"))
            sys.exit(1)
