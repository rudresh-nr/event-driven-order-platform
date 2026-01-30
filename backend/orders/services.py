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

    #raise Exception("Simulated failure after order creation")

    OutboxEvent.objects.create(
        aggregate_type="Order",
        aggregate_id=order.id,
        event_type="OrderCreated",
        schema_version=2,
        payload={
            "order_id": str(order.id),
            "user_id": str(user_id),
            "total_amount": str(total_amount),
            "currency": "INR",
            "source": "web",
        },
    )

    return order

@transaction.atomic
def cancel_order(order_id):
    order = Order.objects.select_for_update().get(id=order_id)

    if order.status != Order.STATUS_CREATED:
        raise ValueError("Only orders in CREATED status can be cancelled.")
    order.status = Order.STATUS_CANCELLED
    order.save()
    OutboxEvent.objects.create(aggregate_id = order.id,
                                aggregate_type="Order",
                                event_type="OrderCancelled",
                                schema_version=1,
                                payload = {
                                    "order_id": str(order.id),
                                    "user_id": str(order.user_id),
                                    "total_amount": str(order.total_amount),
                                },
                                
                                )
    
