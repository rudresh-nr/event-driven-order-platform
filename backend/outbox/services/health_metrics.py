from outbox.models import OutboxEvent
from django.db.models import Count, Q

def get_outbox_distribution():
    return OutboxEvent.objects.aggregate(total_events=Count("id"),
                                         published_events = Count("id", filter=Q(published=True)),
                                         not_published_events =Count("id", filter=Q(published=False)),
                                         consumed_events = Count("id", filter=Q(consumed=True)),
                                         not_consumed_events = Count("id", filter=Q(consumed= False)),
                                         ready_to_consume_events = Count("id", filter=Q(published=True, consumed=False))
                                         )