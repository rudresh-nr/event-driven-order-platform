import random
from outbox.models import OutboxEvent
from orders.models import Order

def saga_handle_order_created(event):
    order_id = event["payload"]["order_id"]
    success = random.choice([True,False])
    
    if success:
        OutboxEvent.objects.create(
            aggregate_type = "Order",
            aggregate_id = order_id,
            event_type = "PaymentSucceeded",
            payload = {"order_id": order_id},
            Schema_version = 1,
        )
    else:
        OutboxEvent.objects.create(
            aggregate_type="Order",
            aggregate_id=order_id,
            event_type="PaymentFailed",
            payload={"order_id":order_id},
            schema_version=1,
        )

def saga_handle_payment_succeeded(event):
    order_id = event["payload"]["order_id"]
    Order.objects.filter(id=order_id).update(status=Order.STATUS_CONFIRMED)


def saga_handle_payment_failed(event):
    order_id = event["payload"]["order_id"]
    Order.objects.filter(id=order_id).update(status=Order.STATUS_CANCELLED)