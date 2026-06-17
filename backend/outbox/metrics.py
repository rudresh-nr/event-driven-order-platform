from prometheus_client import Counter

events_published_total = Counter(
    "events_published_total",
    "Total number of published outbox events",

)

events_consumed_total = Counter(
    "events_consumed_total",
    "Total number of consumed outbox events",
)