from django.core.management.base import BaseCommand
from django.db import transaction
from orders.models import Order
from readmodels.models import OrdersByUser


class Command(BaseCommand):
    help = "Rebuild OrdersByUser read model from orders table"

    def handle(self, *args, **options):
        self.stdout.write("Deleting existing read model data...")
        OrdersByUser.objects.all().delete()

        orders = Order.objects.all()

        self.stdout.write(f"Rebuilding {orders.count()} orders...")

        bulk = []

        for order in orders:
            bulk.append(
                OrdersByUser(
                    order_id=order.id,
                    user_id=order.user_id,
                    status=order.status,
                    total_amount=order.total_amount,
                    created_at=order.created_at,
                    currency=order.currency,
                )
            )

        OrdersByUser.objects.bulk_create(bulk)

        self.stdout.write(self.style.SUCCESS("Read model rebuild complete."))