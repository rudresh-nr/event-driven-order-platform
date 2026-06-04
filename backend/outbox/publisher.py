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

    print(
        "PUBLISHING EVENT_ID:", event_dict["id"]
    )

    # instead of just printing, send the structured event forward to the message broker here
    print("PUBLISHING EVENT_ID:", event.id)
