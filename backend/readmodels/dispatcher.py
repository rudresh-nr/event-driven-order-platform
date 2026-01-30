from .consumers import handle_order_created, handle_order_cancelled

def dispatch_event(event):
    if event["event_type"] == "OrderCreated":
        handle_order_created(event)
    elif event["event_type"] == "OrderCancelled":
        handle_order_cancelled(event)