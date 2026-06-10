from decimal import Decimal
from uuid import uuid4

from django.test import TestCase

from orders.models import Order
from outbox.models import OutboxEvent


# Create your tests here.


class OrderCreationTest(TestCase):
    def test_order_and_outbox_event_created(self):

        user_id = uuid4()

        order = Order.objects.create(
            user_id = user_id,
            total_amount = Decimal("100.00"),
            currency = "INR",
        )

        event = OutboxEvent.objects.create(
            aggregate_type = "Order",
            aggregate_id = order.id,
            event_type = "OrderCreated",
            payload={
                "order_id": str(order.id),
                "user_id": str(user_id),
            },

            schema_version=1,

        )

        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OutboxEvent.objects.count(), 1)

        self.assertEqual(event.event_type, "OrderCreated")
        self.assertEqual(event.aggregate_id, order.id)