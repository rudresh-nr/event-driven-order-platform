from .models import OrdersByUser

def handle_order_created(event):
    OrdersByUser.objects.update_or_create(
        order_id=event["order_id"],
        defaults={
            "user_id": event["user_id"],
            "status": "CREATED",
            "total_amount": event["total_amount"],
            "created_at": event["created_at"],
        }
    )
