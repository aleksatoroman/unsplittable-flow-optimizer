from abc import ABC, abstractmethod

from models.flow_result import FlowResult


class BaseFlowAlgorithm(ABC):
    def __init__(self, params: dict):
        self.artifacts_root = params.get('artifacts_root', None)
        self.max_time = params.get('max_time', 60)
        self.no_improvement_threshold = params.get('no_improvement_threshold', 200)
        pass

    @abstractmethod
    def solve(self, graph) -> FlowResult | None:
        """
        Solves the flow problem and returns the solution.
        :param graph: The FlowGraph instance.
        :return: Solution object or data structure representing the result.
        """
        pass

