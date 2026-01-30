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
def cancel_order(order_id: str, reason: str="User requested cancellation"):
    order = Order.objects.select_for_update().get(id=order_id)

    if not order.can_transition_to("CANCELLED"):
        raise ValueError(f" Order {order.id} cannot be cancelled from status {order.status}.")
    
    order.status = "CANCELLED"
    order.save(update_fields=["status"])

    OutboxEvent.objects.create(
        aggregate_type = "Order",
        aggregate_id = order.id,
        event_type = "OrderCancelled",
        schema_version = 1,
        payload = {
            "order_id": str(order.id),
            "reason": reason,
        }
    )
