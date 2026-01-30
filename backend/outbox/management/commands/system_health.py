from django.core.management.base import BaseCommand
from django.db import connection

def classify(value, warn, critical):
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

            # Outbox backlog
            cursor.execute("""
                SELECT count(*) FROM 
                outbox_outboxevent WHERE published = false
            """)
            outbox_backlog = cursor.fetchone()[0]

            # Max publish lag
            cursor.execute("""
                SELECT MAX(NOW() - created_at)
                FROM outbox_outboxevent WHERE published = false
            """)
            publish_lag = cursor.fetchone()[0]

            # Read model lag
            cursor.execute("""SELECT GREATEST(
                           EXTRACT(EPOCH FROM (MAX(o.created_at) - MAX(r.created_at))),0)
                           FROM orders_order o 
                           LEFT JOIN
                           readmodels_ordersbyuser r
                           ON o.id = r.order_id
                           """)
            read_model_lag_seconds = cursor.fetchone()[0]

            if read_model_lag_seconds is None:
                read_model_status = "OK"
            else:
                read_model_status = classify(read_model_lag_seconds, warn=30, critical=120,)
            

        # -- Outbox backlog status(count) not time --
        backlog_status = "OK" if outbox_backlog == 0 else "WARN"

        #--- Publish lag
        if outbox_backlog == 0:
            publish_lag_status = "OK"
        elif publish_lag is None:
            publish_lag_status = "BROKEN"
        else:
            publish_lag_seconds = publish_lag.total_seconds()
            publish_lag_status = classify(publish_lag_seconds, warn=30, critical=120,)


        # -- Read model lag status (timedelta -> seconds) --
        if read_model_lag_seconds is None:
            read_model_status = "OK"
        else:
            read_model_status = classify(read_model_lag_seconds, warn=30, critical=120,)

        self.stdout.write("SYSTEM HEALTH METRICS")
        self.stdout.write("----------------------")
        self.stdout.write(f"Outbox Backlog: {outbox_backlog} [{backlog_status}]")
        
        self.stdout.write(f"Publish Lag: {publish_lag} [{publish_lag_status}]")
        
        self.stdout.write(f"Read Model Lag: {read_model_lag_seconds} [{read_model_status}]")