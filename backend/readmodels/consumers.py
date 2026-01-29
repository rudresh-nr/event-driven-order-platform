from asyncio.log import logger
from .models import OrdersByUser

def handle_order_created(event):

    logger.info(
        "Processing event", extra={
            "event_id" : event["id"],
            "schema_version" : event["schema_version"],
            "created_at" : event["created_at"], # optional but useful
        }
    )


    version = event.get("schema_version", 1)
    payload = event["payload"]
 
    print(
    "CONSUMING:",
    "version=", version,
    "currency=", payload.get("currency")
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
        currency = payload.get("currency", "Unknown") # ?? doubt
    
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
