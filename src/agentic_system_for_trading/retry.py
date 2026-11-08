import time


class RetryPolicy:
    def __init__(
        self,
        max_attempts: int = 3,
        base_delay_s: float = 1.0,
        retry_on: tuple = (ConnectionError, TimeoutError),
        sleep=time.sleep,
    ):
        self.sleep = sleep
        self.max_attempts = max_attempts
        self.base_delay_s = base_delay_s
        self.retry_on = retry_on

    def call(self, callback):
        for attempt in range(1, self.max_attempts + 1):
            try:
                return callback()
            except self.retry_on:
                self.sleep(self.base_delay_s)

        return "error"
