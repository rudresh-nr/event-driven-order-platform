import json

from django.http import JsonResponse
from django.views import View
from orders.models import Order
from outbox.models import OutboxEvent
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)


# Need to remove this in production
@method_decorator(csrf_exempt, name="dispatch")
class OrderCreateView(View):

    def post(self, request):
        data = json.loads(request.body)

        order = Order.objects.create(
            user_id = data["user_id"],
            total_amount = data["total_amount"],
            currency = data.get("currency", "INR"),
        )

        logger.info(
            "Order Created",
            extra={
                "order_id": str(order.id),
                "user_id": str(order.user_id),
                "amount": float(order.total_amount),
                "currency": order.currency,
            },
        )

        OutboxEvent.objects.create(
            aggregate_type = "Order",
            aggregate_id = order.id,
            event_type = "OrderCreated",

            payload = {
                "order_id": str(order.id),
                "user_id": str(order.user_id),
                "total_amount": float(order.total_amount),
                "currency": order.currency,
            },
            schema_version = 2  
        )
        return JsonResponse(
            {
                "order_id": str(order.id),
                "status": order.status,
            },
            status=201,
        )