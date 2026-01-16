import uuid
from django.db import transaction
from orders.models import Order
from outbox.models import OutboxEvent

@transaction.atomic
def create_order(user_id, total_amount):
    order = Order.objects.create(
        user_id=user_id,
        status=Order.STATUS_CREATED,
        total_amount=total_amount,
    )

    raise Exception("Simulated failure after order creation")

    OutboxEvent.objects.create(
        aggregate_type="Order",
        aggregate_id=order.id,
        event_type="OrderCreated",
        schema_version=1,
        payload={
            "order_id": str(order.id),
            "user_id": str(user_id),
            "total_amount": str(total_amount),
        },
    )

    return order
