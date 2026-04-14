from django.core.management.base import BaseCommand
from orders.models import Order
from outbox.models import OutboxEvent
import uuid
from decimal import Decimal

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user_id = uuid.uuid4()
        #user_id = "user-1"
        order_id = uuid.uuid4()

        order = Order.objects.create(
            id= order_id,
            user_id=user_id,
            total_amount=Decimal("100.00"),
            status=Order.STATUS_CREATED,
        )

        OutboxEvent.objects.create(
            aggregate_type="order",
            aggregate_id=order_id,
            event_type="OrderCreated",
            schema_version=2,
            payload={
                "order_id": str(order_id),
                "user_id": str(user_id),
                "total_amount": "100.00",
            },
            published = False,
            consumed = False,
            failed = False,
        )

        self.stdout.write(self.style.SUCCESS(f"Created order {order_id} and corresponding outbox event"))