from abc import ABC, abstractmethod

from models.flow_result import FlowResult


class BaseFlowAlgorithm(ABC):
    def __init__(self, params: dict):
        pass

    @abstractmethod
    def solve(self, graph) -> FlowResult | None:
        """
        Solves the flow problem and returns the solution.
        :param graph: The FlowGraph instance.
        :return: Solution object or data structure representing the result.
        """
        pass
