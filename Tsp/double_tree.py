import networkx as nx
import itertools

class DoubleTree():
    def __init__(self, graph, n):
        self.graph = graph
        self.mst = nx.minimum_spanning_tree(graph)
        self.used = [False for _ in range(n)]
    
    def _dfs(self, v, result):
        result.append(v)
        self.used[v] = True
        for to in self.mst[v]:
            if not self.used[to]:
                self._dfs(to, result)
    
    def exec(self):
        tour = []
        self._dfs(0, tour)
        tour.append(tour[0])
        return tour