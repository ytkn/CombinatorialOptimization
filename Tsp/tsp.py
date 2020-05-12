import math
import itertools
import networkx as nx
import matplotlib.pyplot as plt

from christofides import Christofides
from double_tree import DoubleTree

def deg2rad(x):
    return math.pi*x/180.0

def dist(x1, x2, y1, y2):
    return int(math.sqrt((x2-x1)**2+(y2-y1)**2))

def read_file():
    r = 0.65*10000
    f = open('hokkaido.txt', 'r')
    line = f.readline()
    lat = []
    longt = []
    while line:
        row = line.split(' ')
        lat.append(float(row[1]))
        longt.append(float(row[2].replace('\n', '')))
        line = f.readline()
    f.close()

    ave_lat = sum(lat)/len(lat)
    ave_longt = sum(longt)/len(longt)
    r_longt = r*math.cos(math.pi*ave_lat/180)

    x = [deg2rad(l-ave_longt)*r_longt for l in longt]
    y = [deg2rad(l-ave_lat)*r for l in lat]
    n = len(x)
    return x, y, n

def plot_graph(adjacent_list, x, y):
    n = len(adjacent_list)
    for v in range(n):
        for to in adjacent_list[v]:
            if v < to:
                plt.plot([x[v], x[to]], [y[v], y[to]], marker='o', c='red', linestyle="solid")
    plt.show()
    return

def plot_tour(tour, x, y):
    n = len(tour)-1
    for i in range(n):
        v = tour[i]
        to = tour[i+1]
        plt.plot([x[v], x[to]], [y[v], y[to]], marker='o', c='red', linestyle="solid")
    plt.show()
    return

def calc_dist(tour, x, y):
    total_dist = 0.0
    n = len(tour)-1
    for i in range(n):
        v = tour[i]
        to = tour[i+1]
        total_dist += dist(x[v], x[to], y[v], y[to])
    return total_dist

def calc_expected_dist(x, y):
    n = len(x)
    comb = (n*(n-1))/2
    result = 0.0
    for i, j in itertools.combinations(range(n), 2):
        result += dist(x[i], x[j], y[i], y[j])*n/comb
    return result

def euclidean_graph(x, y):
    n = len(x)
    result = nx.Graph()
    for i, j in itertools.product(range(n), range(n)):
        result.add_edge(i, j, weight = dist(x[i], x[j], y[i], y[j]))
    return result

if __name__ == "__main__":
    x, y, n = read_file()
    graph =  euclidean_graph(x, y)
    double_tree = DoubleTree(graph, n).exec()
    christofides = Christofides(graph, n).exec()

    plot_tour(double_tree, x, y)
    plot_tour(christofides, x, y)

    print("distance by double tree  : {:.1f} [km]".format(calc_dist(double_tree, x, y)))
    print("distance by christofides : {:.1f} [km]".format(calc_dist(christofides, x, y)))
    print("distance by random trip  : {:.1f} [km]".format(calc_expected_dist(x, y)))