# orders/dashboard_api.py
from django.http import JsonResponse
from orders.models import Order
from outbox.models import OutboxEvent

def dashboard_metrics(request):
    return JsonResponse({
        "orders_created": Order.objects.count(),
        "events_published": OutboxEvent.objects.filter(published=True).count(),
        "events_consumed": OutboxEvent.objects.filter(consumed=True).count(),
        "outbox_backlog": OutboxEvent.objects.filter(published=True, consumed=False).count(),

    })