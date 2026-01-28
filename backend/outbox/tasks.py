from celery import shared_task
from django.db import transaction

from outbox.models import OutboxEvent
from outbox.publisher import publish_event
from readmodels.dispatcher import dispatch_event

# autoretry_for=(Exception,), retry_backoff=5) should be used cautiously in production
@shared_task
def publish_outbox_events(batch_size=100):
    """
    Publishes unpublished outbox events to the message broker.

    Delivery semantics:
    - At-least-once
    - Ordered by created_at
    - Retries on failure
    """
    events = (
        OutboxEvent.objects
        .filter(published=False)
        .order_by("created_at")[:batch_size]
    )

    for event in events:
        publish_event(event)

        # Mark as published only after successful publish
        event.published = True
        event.save(update_fields=["published"])


@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5)
def consume_published_events(self, batch_size=100):
    """
    Consumes already-published events and projects them
    into derived read models.

    This task is:
    - Idempotent
    - Replay-safe
    - Side-effect free for write models
    """
    events = (
        OutboxEvent.objects
        .filter(published=True)
        .order_by("created_at")[:batch_size]
    )

    for event in events:
        dispatch_event({
            "event_type": event.event_type,
            "payload": event.payload,
            "schema_version": event.schema_version,
            "created_at": event.created_at,
        })
