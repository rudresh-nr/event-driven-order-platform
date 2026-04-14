from celery import shared_task
from django.db import transaction
from django.db.models import F
from outbox.dispatcher import dispatch_event
from outbox.models import OutboxEvent
from outbox.publisher import publish_event


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
        try:
            publish_event(event) # send to message broker
            
            # Line 31 is using the ORM's update method to mark the event as published without 
            # loading it into memory, which is more efficient than the approach in the commented-out 
            # code below at lines 34-35.
            OutboxEvent.objects.filter(id=event.id).update(published=True) 
            
            '''
            event.published = True
            event.save(update_fields=["published"]) 
            # Line 34 and 35 are using ORM methods to update the published status of the event.
            # Using the ORM's update method is more efficient than loading the event into memory 
            # and saving
            '''


        except Exception as e:
            # Log the error and let Celery handle the retry
            print(f"Error publishing event {event.id}: {e}")
            # raise self.retry(exc=e) # Uncomment if you want to use Celery's retry mechanism


def _consume_published_events(batch_size=100):
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
        .select_for_update(skip_locked=True)
        .filter(published=True, consumed=False, failed=False)
        .order_by("created_at")[:batch_size]
    )
    MAX_RETRIES = 3
    for event in events:
        try:
            dispatch_event({
                "event_type": event.event_type,
                "payload": event.payload,
                "schema_version": event.schema_version,
                "created_at": event.created_at,
            })
            OutboxEvent.objects.filter(id=event.id).update(consumed=True)

        except Exception as e:
            # retry increment persistently to avoid infinite retries on poison events
            OutboxEvent.objects.filter(id=event.id).update(retry_count=F('retry_count') + 1)
            event.refresh_from_db() # Refresh to get updated retry_count

            if event.retry_count >= MAX_RETRIES:
                OutboxEvent.objects.filter(id=event.id).update(failed=True)

            '''
             after marking the event as failed will cause Celery to retry even for failed events.
             Consider not retrying if the event is already marked as failed to avoid unnecessary retries.
            '''    
            #raise self.retry(exc=e)

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=5)
def consume_published_events(self, batch_size=100):
    with transaction.atomic():
        _consume_published_events(batch_size=batch_size)