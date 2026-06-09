from django.contrib import admin
from .models import OutboxEvent, ProcessedEvent

# Register your models here.
admin.site.register(OutboxEvent)
admin.site.register(ProcessedEvent)