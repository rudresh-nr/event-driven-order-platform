from readmodels.consumers import readmodel_handle_order_created
from outbox.services.saga import (saga_handle_order_created, saga_handle_payment_succeeded, saga_handle_payment_failed)

def dispatch_event(event):
    event_type = event["event_type"]

     #🔥  saga orchestration
    if event_type == "OrderCreated":
        saga_handle_order_created(event)
        readmodel_handle_order_created(event)
    elif event_type == "PaymentSucceeded":
        saga_handle_payment_succeeded(event)
    elif event_type == "PaymentFailed":
        saga_handle_payment_failed(event)
    # 📈 read model projection 
    elif event_type == "OrderCreated":
        readmodel_handle_order_created(event)