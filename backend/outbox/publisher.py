import logging
from outbox.metrics import events_published_total

logger = logging.getLogger(__name__)


def publish_event(event):

    """
    Boundary function responsible for publishing an event
    to an external message broker.

    At this stage, this is intentionally a stub.
    """

    # Placeholder for Kafka / message broker

    event_dict = {
        "id": str(event.id),
        "event_type": event.event_type,
        "payload": event.payload,
        "created_at": str(event.created_at),
    }

    logger.info(
        "publishing_outbox_event",
        extra={
            "event_id": event_dict["id"],
            "event_type": event.event_type,
            "aggregate_id": str(event.aggregate_id),
        },
    )

    logger.info(
    "publish_metric_incremented",
    extra={
        "counter_value": events_published_total._value.get(),
    },
)
