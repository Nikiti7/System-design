import time
from locust import HttpUser, task, constant


class KafkaUser(HttpUser):
    wait_time = constant(1)

    @task
    def send_data(self):
        self.client.post(
            "/events",
            json={
                "user_id": "nikol",
                "event_type": "click",
                "item_id": "item_123",
                "timestamp": str(int(time.time())),
            },
        )
