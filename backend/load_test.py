from orders.models import Order
from outbox.models import OutboxEvent
import uuid
from decimal import Decimal

orders = []
events = []

def load_test_data(n=10000) -> tuple[int, int]:

    for _ in range(n):
        user_id = uuid.uuid4()
        order_id = uuid.uuid4()

        orders.append(Order(
            id=order_id,
            user_id=user_id,
            status=Order.STATUS_CREATED,
            total_amount=Decimal("100.00")))
        
        events.append(OutboxEvent(
            aggregate_type="order",
            aggregate_id=order_id,
            event_type="OrderCreated",
            schema_version=1,
            payload={
                "order_id": str(order_id),
                "user_id": str(user_id),
                "total_amount": "100.00",
            },
            published = False,
            consumed = False,
            failed = False,
        ))
    # Bulk create orders and events
    Order.objects.bulk_create(orders, batch_size=1000)
    OutboxEvent.objects.bulk_create(events, batch_size=1000)
    return (len(orders), len(events))

