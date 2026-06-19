from outbox.models import DeadLetterEvent, OutboxEvent


def replay_dead_letter_event(event_id):
    dlq_event = DeadLetterEvent.objects.get(event_id=event_id)

    outbox_event = OutboxEvent.objects.get(id=event_id)

    outbox_event.failed = False
    outbox_event.retry_count = 0
    outbox_event.consumed = False

    outbox_event.save()

    return outbox_event.id