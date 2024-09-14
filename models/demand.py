class Demand:
    def __init__(self, source, sink, flow):
        """
        Represents a flow demand from the source to the sink.
        :param source: The source node for the demand.
        :param sink: The sink node for the demand.
        :param flow: The flow required from source to sink.
        """
        self.source = source
        self.sink = sink
        self.flow = flow
