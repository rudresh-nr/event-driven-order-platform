import traceback

from readmodels.consumers import readmodel_handle_order_created, readmodel_handle_payment_succeeded, readmodel_handle_payment_failed
from outbox.services.saga import (saga_handle_order_created, saga_handle_payment_succeeded, saga_handle_payment_failed)
from outbox.models import ProcessedEvent

def dispatch_event(event):

    event_id = event["id"]
    if ProcessedEvent.objects.filter(event_id=event_id).exists():
        print(f"Skipping duplicate event {event_id}")
        return


    try:
        event_type = event["event_type"]
        #🔥  saga orchestration
        if event_type == "OrderCreated":
            saga_handle_order_created(event)
            readmodel_handle_order_created(event)

        elif event_type == "PaymentSucceeded":
            saga_handle_payment_succeeded(event)
            readmodel_handle_payment_succeeded(event)

        elif event_type == "PaymentFailed":
            saga_handle_payment_failed(event)
            readmodel_handle_payment_failed(event)

        # Mark event as processed to ensure idempotency
        ProcessedEvent.objects.get_or_create(event_id=event_id)

    except Exception as e:
        print(f"Error processing event {event_id}: {e}")
        traceback.print_exc()
        raise e