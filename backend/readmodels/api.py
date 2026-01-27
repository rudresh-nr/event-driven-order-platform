from rest_framework.views import APIView
from rest_framework.response import Response
from readmodels.models import OrdersByUser
from django.core.cache import cache
from django_redis.exceptions import ConnectionInterrupted
from redis.exceptions import TimeoutError, ConnectionError
CACHE_TTL = 60  # seconds

class OrdersByUserView(APIView):
    def get(self, request, user_id):
        cache_key = f"v1:user_orders:{user_id}"

        try:
            cached = cache.get(cache_key)
        except (ConnectionInterrupted, TimeoutError, ConnectionError):
            cached = None # Cache connection issue, proceed without cache
        
        if cached is not None:
            return Response(cached)

        # ORM query to fetch orders by user_id
        orders = (
            OrdersByUser.objects
            .filter(user_id=user_id)
            .order_by("-created_at")
        )

        data = [
            {
                "order_id": str(o.order_id),
                "status": o.status,
                "total_amount": str(o.total_amount),
                "created_at": o.created_at,
            }
            for o in orders
        ]
        try:
            cache.set(cache_key, data, timeout=CACHE_TTL)
        except (ConnectionInterrupted, TimeoutError, ConnectionError):
            pass  # Cache connection issue, skip caching

        return Response(data)
