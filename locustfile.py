from locust import HttpUser, task, between

class ShortenerUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def create_short_link(self):
        self.client.post("/api/links", json={
            "target_url": "https://example.com"
        })

    @task
    def redirect(self):
        self.client.get("/abc123")