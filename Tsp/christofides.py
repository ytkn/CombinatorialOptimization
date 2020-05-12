import networkx as nx
import itertools

class Christofides():
    def __init__(self, graph, n):
        self.n = n
        self.graph = graph
        self.mst = nx.minimum_spanning_tree(graph)
        self.eulerian_graph = nx.Graph()
        self.used = [False for _ in range(n)]
    
    def _odd_degree_vertices(self):
        result = []
        for i in range(self.n):
            if len(self.mst[i])%2 == 1:
                result.append(i)
        return result

    def _odd_complete_greph(self):
        odd_degree_vertices = self._odd_degree_vertices()
        result = nx.Graph()
        for i, j in itertools.combinations(odd_degree_vertices, 2):
            result.add_edge(i, j, weight = -self.graph[i][j]['weight'])
        return result
    
    def _make_eulerian_graph(self):
        odd_complete_graph = self._odd_complete_greph()
        matching = nx.max_weight_matching(odd_complete_graph, maxcardinality=True)
        self.eulerian_graph = self.mst
        for i, j in matching:
            self.eulerian_graph.add_edge(i, j, weight = self.graph[i][j]['weight'])
    
    def _dfs(self, v, result):
        result.append(v)
        self.used[v] = True
        for to in self.eulerian_graph[v]:
            if not self.used[to]:
                self._dfs(to, result)
    
    def exec(self):
        self._make_eulerian_graph()
        tour = []
        self._dfs(0, tour)
        tour.append(tour[0])
        return tour