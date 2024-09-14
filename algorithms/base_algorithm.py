from abc import ABC, abstractmethod


class BaseFlowAlgorithm(ABC):
    @abstractmethod
    def solve(self, graph, demands):
        """
        Solves the flow problem and returns the solution.
        :param graph: The FlowGraph instance.
        :param demands: A list of Demand instances.
        :return: Solution object or data structure representing the result.
        """
        pass
