from prometheus_client import Counter

orders_created_total = Counter(
    "orders_created_total",
    "Total number of successfully created orders",
)