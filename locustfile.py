from locust import HttpUser, task, between

class MainPageUser(HttpUser):
    # Define how long the user waits between requests (in seconds)
    wait_time = between(1, 2)

    @task
    def test_main_endpoint(self):
        self.client.get("/")
