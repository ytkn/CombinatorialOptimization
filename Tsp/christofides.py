import networkx as nx
import itertools

class Christofides():
    def __init__(self, graph, n):
        self.n = n
        self.graph = graph
        self.mst = nx.minimum_spanning_tree(graph)
        self.eulerian_graph = nx.MultiGraph()
    
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

        for v, to in self.mst.edges():
            self.eulerian_graph.add_edge(v, to, self.mst[v][to]["weight"])
            
        for i, j in matching:
            self.eulerian_graph.add_edge(i, j, weight = self.graph[i][j]['weight'])
    
    def exec(self):
        used = [False for _ in range(self.n)]
        self._make_eulerian_graph()
        eulerian_circuit = nx.eulerian_circuit(self.eulerian_graph)
        tour = []
        for s, t in eulerian_circuit:
            if len(tour) == 0:
                tour.append(s)
                used[s] = True
            if not used[t]:
                tour.append(t)
                used[t] = True
        return tour