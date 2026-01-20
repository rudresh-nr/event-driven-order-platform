def publish_event(event):
    """
    Boundary function responsible for publishing an event
    to an external message broker.

    At this stage, this is intentionally a stub.
    """

    # Placeholder for Kafka / message broker
    
    print(
        f"[PUBLISH] {event.event_type} | "
        f"aggregate={event.aggregate_type}:{event.aggregate_id}"
    )
