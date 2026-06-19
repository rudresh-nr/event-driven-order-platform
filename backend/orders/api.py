import json
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from orders.metrics import orders_created_total
from orders.services import create_order
import logging

logger = logging.getLogger(__name__)


# Need to remove this in production
@method_decorator(csrf_exempt, name="dispatch")
class OrderCreateView(View):

    def post(self, request):
        data = json.loads(request.body)

        order = create_order(
        user_id=data["user_id"],
        total_amount=data["total_amount"],
        currency=data.get("currency", "INR"),
    )

        orders_created_total.inc()

        logger.info(
            "Order Created",
            extra={
                "order_id": str(order.id),
                "user_id": str(order.user_id),
                "amount": float(order.total_amount),
                "currency": order.currency,
            },
        )
        return JsonResponse(
            {
                "order_id": str(order.id),
                "status": order.status,
            },
            status=201,
        )