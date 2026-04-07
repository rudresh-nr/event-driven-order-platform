import uuid
from django.db import models

class OutboxEvent(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    aggregate_type = models.CharField(max_length=50)
    aggregate_id = models.UUIDField()

    event_type = models.CharField(max_length=100)
    payload = models.JSONField()
    schema_version = models.IntegerField()

    published = models.BooleanField(default=False)
    consumed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    retry_count = models.IntegerField(default=0)
    failed = models.BooleanField(default=False)

    class Meta:
        indexes = [
           models.Index(fields=["published", "consumed", "failed", "created_at"]),
           models.Index(fields=["aggregate_id"]),
        ]
    

        

