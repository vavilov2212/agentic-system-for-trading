class Collector:
    def __init__(self, source, sink, retry):
        self.source = source
        self.sink = sink
        self.retry = retry

    def collect(self, symbol):
        snapshot = self.retry.call(lambda: self.source.fetch_snapshot(symbol))
        self.sink.save(snapshot)
