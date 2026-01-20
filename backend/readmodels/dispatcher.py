from .consumers import handle_order_created

def dispatch_event(event):
    if event["event_type"] == "OrderCreated":
        handle_order_created(event)
