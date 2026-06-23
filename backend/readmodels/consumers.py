import logging
import traceback
from .models import OrdersByUser
from outbox.metrics import events_consumed_total

logger = logging.getLogger(__name__)

def readmodel_handle_order_created(event):

    print("====== ORDER CREATED HANDLER START ======")
    print(event)

    payload = event["payload"]
    logger.info(
        "Processing event", 
        extra={
            "order_id" : event["payload"].get("order_id"),
            "schema_version" : event["schema_version"],
            "created_at" : event["created_at"], # optional but useful
            "correlation_id": payload.get("correlation_id"),
        }
    )


    version = event.get("schema_version", 1)

 
    logger.info(
    "consuming_order_created_event",
    extra={
        "event_id": str(event["id"]),
        "version": version,
        "currency": payload.get("currency"),
        "order_id": payload.get("order_id"),
        "user_id": payload.get("user_id"),
        "correlation_id": payload.get("correlation_id"),
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
    
    print("order_id =", order_id)
    print("user_id =", user_id)
    print("total_amount =", total_amount)
    print("currency =", currency)

    try:
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

        events_consumed_total.inc()
    except Exception as e:
        print("READMODEL ERROR: ", e)
        traceback.print_exc()
        raise

    logger.info(
    "consume_metric_incremented",
    extra={
        "event_id": str(event["id"])
    }
    )

def readmodel_handle_order_cancelled(event):
    print("===== ORDER CANCELLED HANDLER =====")
    payload = event["payload"]
    print("PAYLOAD =", payload)

    logger.info(
        "payment_succeeded_event",
        extra={
            "order_id": payload.get("order_id"),
            "correlation_id": payload.get("correlation_id"),
        },
    )

    obj, created = OrdersByUser.objects.update_or_create(
        order_id = payload["order_id"],
        defaults={
            "status": "CANCELLED"
        }
    )

    print("ROW ID =", obj.id)
    print("CREATED =", created)
    print("STATUS =", obj.status)
    

def readmodel_handle_payment_succeeded(event):
    order_id = event["payload"]["order_id"]
    payload = event["payload"]

    logger.info(
        "payment_failed_event",
        extra={
            "order_id": payload.get("order_id"),
            "correlation_id": payload.get("correlation_id"),
        },
    )

    OrdersByUser.objects.filter(order_id=order_id).update(status="CONFIRMED")

def readmodel_handle_payment_failed(event):
    order_id = event["payload"]["order_id"]

    OrdersByUser.objects.filter(order_id=order_id).update(status="CANCELLED")
