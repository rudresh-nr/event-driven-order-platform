from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = "Print system health metrics"

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT count(*) FROM outbox_outboxevent WHERE published = false
            """)
            backlog = cursor.fetchone()[0]

            cursor.execute("""
                SELECT MAX(NOW() - created_at)
                FROM outbox_outboxevent WHERE published = false
            """)
            lag = cursor.fetchone()[0]

        self.stdout.write(f"Outbox backlog: {backlog}")
        self.stdout.write(f"Max publish lag: {lag}")
