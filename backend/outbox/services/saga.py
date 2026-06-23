import random
from outbox.models import OutboxEvent
from orders.models import Order

def saga_handle_order_created(event):
    order_id = event["payload"]["order_id"]
    success = random.choice([True,False])
    correlation_id = event["payload"].get("correlation_id")

    if success:
        OutboxEvent.objects.create(
            aggregate_type = "Order",
            aggregate_id = order_id,
            event_type = "PaymentSucceeded",
            payload = {"order_id": order_id, "correlation_id": correlation_id,},
            schema_version = 1,
        )
    else:
        OutboxEvent.objects.create(
            aggregate_type="Order",
            aggregate_id=order_id,
            event_type="PaymentFailed",
            payload={"order_id":order_id, "correlation_id": correlation_id,},
            schema_version=1,
        )

def saga_handle_payment_succeeded(event):
    order_id = event["payload"]["order_id"]
    Order.objects.filter(id=order_id).update(status=Order.STATUS_CONFIRMED)


def saga_handle_payment_failed(event):
    order_id = event["payload"]["order_id"]
    Order.objects.filter(id=order_id).update(status=Order.STATUS_CANCELLED)

def saga_handle_order_cancelled(event):
    pass