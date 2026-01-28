from django.db import models

from django.db import models

class OrdersByUser(models.Model):
    user_id = models.UUIDField()
    order_id = models.UUIDField(unique=True)
    status = models.CharField(max_length=20)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField()
    currency = models.CharField(max_length=10, default="Unknown")

    class Meta:
        indexes = [
            models.Index(fields=["user_id", "-created_at"]),
        ]

