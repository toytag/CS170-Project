import numpy as np
import networkx as nx

def avg_pairwise_cost(adjmat, nxGraph):
    n = 0
    cost = 0
    pairwise_paths = nx.shortest_path(nxGraph)
    for u, targets in pairwise_paths.items():
        for v, path in targets.items():
            if u != v:
                n += 1
                cost += path_cost(adjmat, path)
    return cost / n

def path_cost(adjmat, path):
    cost = 0
    for u, v in zip(path[:-1], path[1:]):
        cost += adjmat[u, v]
    return cost