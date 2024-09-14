class Demand:
    def __init__(self, source: int, sink: int, flow: int) -> None:
        self.source: int = source
        self.sink: int = sink
        self.flow: int = flow
