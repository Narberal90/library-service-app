import time
from django.db import connection
from django.db.utils import OperationalError
from django.core.management import BaseCommand


class Command(BaseCommand):
    """Django command to pause execution until db is available"""
    def add_arguments(self, parser):
        parser.add_argument("--wait", type=int, default=5)

    def handle(self, *args, **options):
        time_to_wait = options["wait"]

        for attempt in range(10):
            try:
                if time_to_wait:
                    time.sleep(time_to_wait)
                connection.ensure_connection()
            except OperationalError:
                self.stdout.write(f"Attempt: {attempt + 1}")
                time.sleep(2)
            else:
                self.stdout.write(self.style.SUCCESS("Database found!"))
                return

        self.stdout.write(self.style.ERROR("Failed to find database."))

