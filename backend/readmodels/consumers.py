import logging
from .models import OrdersByUser


logger = logging.getLogger(__name__)

def readmodel_handle_order_created(event):

    logger.info(
        "Processing event", 
        extra={
            "order_id" : event["payload"].get("order_id"),
            "schema_version" : event["schema_version"],
            "created_at" : event["created_at"], # optional but useful
        }
    )


    version = event.get("schema_version", 1)
    payload = event["payload"]
 
    logger.info(
    "consuming_order_created_event",
    extra={
        "event_id": str(event["id"]),
        "version": version,
        "currency": payload.get("currency"),
        "order_id": payload.get("order_id"),
        "user_id": payload.get("user_id"),
    },
)


    if version == 1:
        order_id = payload['order_id']
        user_id = payload['user_id']
        total_amount = payload['total_amount']
        currency = "Unknown"

    elif version == 2:
        order_id = payload["order_id"]
        user_id = payload["user_id"]
        total_amount = payload["total_amount"]
        currency = payload.get("currency") 
    
    else:
        # Future-proofing
        raise ValueError(f"Unsupported OrderCreated version: {version}")

    OrdersByUser.objects.update_or_create(
        order_id= order_id,
        defaults={
            "user_id": user_id,
            "status": "CREATED",
            "total_amount": total_amount,
            "currency": currency,
            "created_at": event["created_at"],
        }
    )

def readmodel_handle_order_cancelled(event):
    raise RuntimeError("Simulated consumer failure")
    payload = event["payload"]

    OrdersByUser.objects.update_or_create(
        order_id = payload["order_id"],
        defaults={
            "status": "CANCELLED"
        }
    )

def readmodel_handle_payment_succeeded(event):
    order_id = event["payload"]["order_id"]

    OrdersByUser.objects.filter(order_id=order_id).update(status="CONFIRMED")

def readmodel_handle_payment_failed(event):
    order_id = event["payload"]["order_id"]

    OrdersByUser.objects.filter(order_id=order_id).update(status="CANCELLED")
