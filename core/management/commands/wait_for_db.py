import time

from django.db                   import connection
from django.db.utils             import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('-t', required=False, default=30, type=int)

    def handle(self, *args, **options):
        started_time = time.time()
        timeout      = False
        db_conn      = None

        self.stdout.write(self.style.NOTICE('Waiting for database...'))

        while not db_conn and not timeout:
            try:
                connection.ensure_connection()
                db_conn = True

            except OperationalError:
                self.stdout.write(self.style.NOTICE('Database unavailable, waiting 1 second...'))
                time.sleep(1)

            if time.time() - started_time > options['t']:
                timeout = True

        if db_conn:
            self.stdout.write(self.style.SUCCESS('Database available!'))
        else:
            self.stdout.write(self.style.ERROR('Database connection failed! - timeout'))