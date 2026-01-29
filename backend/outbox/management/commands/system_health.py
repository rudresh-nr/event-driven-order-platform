from django.core.management.base import BaseCommand
from django.db import connection

def classify(label, value, warn, critical):
    if value is None:
        return "BROKEN"
    if value > critical:
        return "CRITICAL"
    if value > warn:
        return "WARN"
    return "OK"



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

        backlog_status = classify(
            "publish_lag",
            backlog,
            warn=10,
            critical=100,
        )

        lag_seconds = lag.total_seconds() if lag else None
        lag_status = classify(
            "outbox_backlog",
            lag_seconds,
            warn=30,
            critical=120,
        )

        self.stdout.write(f"Outbox backlog: {backlog}[{backlog_status}]")
        self.stdout.write(f"Max publish lag: {lag}[{lag_status}]")