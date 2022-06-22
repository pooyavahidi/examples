from locust import HttpUser, task, between


class TestUser(HttpUser):
    # Set the pacing of each request to a random number from 1 to 5 seconds.
    # wait_time = between(1, 5)

    @task
    def post_sleep_process(self):
        self.client.post("/processes", json={"args": ["sleep", "2"]})

    # @task
    # def get_root(self):
    #     self.client.get("/")
