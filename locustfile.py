from locust import HttpUser, task, between
import uuid


class OrderUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def create_order(self):
        self.client.post(
            "/orders/",
            json={
                "user_id": str(uuid.uuid4()),
                "total_amount": 100,
                "currency": "INR"
            }
        )