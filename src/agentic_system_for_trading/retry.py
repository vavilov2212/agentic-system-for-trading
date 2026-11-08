class RetryPolicy:
    def __init__(
        self,
        max_attempts: int = 3,
        base_delay_s: float = 1.0,
        retry_on: tuple = (ConnectionError, TimeoutError),
        sleep: list | None = None,
    ):
        if sleep is None:
            sleep = []
        self.sleep = sleep
        self.max_attempts = max_attempts
        self.base_delay_s = base_delay_s
        self.retry_on = retry_on

    def call(self, callback):
        print("call")

        while self.attempts <= self.max_attempts:
            try:
                callback()

                return "ok"
            except self.retry_on:
                self.sleep()

        return "error"
