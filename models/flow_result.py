class FlowResult:
    def __init__(self, paths, demands, edges):
        self.paths = paths
        self.demands = demands
        self.edges = edges

    def validate(self):
        edge_flows = {edge: 0 for edge in self.edges}

        for sink, path in self.paths.items():
            demand_flow = self.demands[sink].flow
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                edge = (u, v)
                if edge in edge_flows:
                    edge_flows[edge] += demand_flow

        valid = True
        for edge, flow in edge_flows.items():
            capacity = self.edges[edge]
            if flow <= capacity:
                print(f"Edge {edge} carries {flow} flow (max capacity: {capacity}) - OK")
            else:
                print(f"Edge {edge} carries {flow} flow (max capacity: {capacity}) - VIOLATION")
                valid = False

        if valid:
            print("All constraints satisfied.")
        else:
            print("There are constraint violations.")

        return valid
