import sys
import random
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast


NUM_SAMPLE = 3


def minimum_spanning_tree_solution(G):
    T = nx.minimum_spanning_tree(G)

    Ts = []
    for _ in range(NUM_SAMPLE):
        Ts.append(expand(G, prune(G, T.copy())))

    return min(Ts, key=lambda T: average_pairwise_distance_fast(T))


def single_source_dijkstra_path_tree_solution(G, src):
    T = nx.Graph()
    T.add_nodes_from(G)
    for dst, path in nx.single_source_dijkstra_path(G, source=src).items():
        if len(path) >= 2:
            for u, v in zip(path[:-1], path[1:]):
                T.add_edge(u, v, weight=G[u][v]["weight"])

    Ts = []
    for _ in range(NUM_SAMPLE):
        Ts.append(expand(G, prune(G, T.copy(), src)))

    return min(Ts, key=lambda T: average_pairwise_distance_fast(T))


def single_source_random_tree_solution(G, src):
    G_tmp = G.copy()
    for u, v in G_tmp.edges:
        G_tmp[u][v]['random'] = random.uniform(0, 1)
    T = nx.minimum_spanning_tree(G_tmp, weight='random')

    Ts = []
    for _ in range(NUM_SAMPLE):
        Ts.append(expand(G, prune(G, T.copy(), src)))

    return min(Ts, key=lambda T: average_pairwise_distance_fast(T))


def prune(G, T, src=None):
    closed = set([src])
    while True:
        d1_vs = set([v for v, d in T.degree() if d == 1])
        if len(d1_vs) == 0 or d1_vs.issubset(closed):
            break
        v = random.sample(d1_vs.difference(closed), 1)[0]
        T_tmp = T.copy()
        T_tmp.remove_node(v)
        if is_valid_network(G, T_tmp):
            T.remove_node(v)
        closed.add(v)
    return T


def expand(G, T, src=None):
    closed = set()
    baseline = average_pairwise_distance_fast(T)
    while True:
        tree_nodes = set(T.nodes)
        if tree_nodes.issubset(closed):
            break
        u = random.sample(tree_nodes.difference(closed), 1)[0]
        neighbors = list(nx.all_neighbors(G, u))
        random.shuffle(neighbors)
        for v in neighbors:
            if v not in T:
                T_tmp = T.copy()
                T_tmp.add_edge(u, v, weight=G[u][v]["weight"])
                new_baseline = average_pairwise_distance_fast(T_tmp)
                if new_baseline < baseline:
                    T.add_edge(u, v, weight=G[u][v]["weight"])
                    baseline = new_baseline
        closed.add(u)
    return T


def BFprune(G, T):
    closed = set()
    baseline = average_pairwise_distance_fast(T)
    while True:
        d1_vs = set([v for v, d in T.degree() if d == 1])
        if len(d1_vs) == 0 or d1_vs.issubset(closed):
            break
        v = random.sample(d1_vs.difference(closed), 1)[0]
        # print(v)
        T_tmp = T.copy()
        T_tmp.remove_node(v)
        new_baseline = average_pairwise_distance_fast(T_tmp)
        if nx.is_dominating_set(G, T_tmp.nodes) and new_baseline < baseline:
            T.remove_node(v)
            baseline = new_baseline
        closed.add(v)
    return T


def BruteForce(G, n, graph_name=None):
    if n >= len(G.nodes):
        if len(G.nodes) > 25:
            num = len(G.nodes) - 8
        elif (len(G.nodes) <= 5):
            num = 1
        else:
            num = len(G.nodes) - 5
    else:
        num = n
    optimalT = nx.Graph()
    nodes = G.nodes
    minAvgDistance = float('inf')
    counter = 0
    for chosen in combinations(nodes, num):
        copyG = G.copy()
        # print(copyG.nodes)
        for node in nodes:
            if node not in chosen:
                copyG.remove_node(node)

        for i in range(1):
            T = nx.minimum_spanning_tree(copyG)
            # T = randomMST(copyG)
            if ((nx.is_empty(T)) or (not nx.is_tree(T)) or (not nx.is_connected(T)) or (not is_valid_network(G, T))):
                continue

            T = BFprune(G, T)

            if ((nx.is_empty(T)) or (not nx.is_tree(T)) or (not nx.is_connected(T)) or (not is_valid_network(G, T))):
                continue
            # print(T.nodes)
            apd = average_pairwise_distance_fast(T)
            if apd < minAvgDistance:
                minAvgDistance = apd
                optimalT = T.copy()
                if minAvgDistance == 0:
                    break

    return optimalT


def solve(G):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    counter = {node: 0 for node in G.nodes()}
    for src, dsts in nx.all_pairs_dijkstra_path(G):
        for dst, path in dsts.items():
            for node in path[1:-1]:
                counter[node] += 1
    transbays = sorted(counter.keys(), key=lambda v: counter[v], reverse=True)
    maxDegrees = sorted(G.nodes, key=lambda v: G.degree(v), reverse=True)

    transbays = transbays[:5] if len(transbays) > 5 else transbays
    maxDegrees = maxDegrees[:5] if len(maxDegrees) > 5 else maxDegrees
    sources = set(transbays + maxDegrees)

    Ts = [minimum_spanning_tree_solution(G)]
    for src in sources:
        Ts.append(single_source_dijkstra_path_tree_solution(G, src))
        for _ in range(NUM_SAMPLE):
            Ts.append(single_source_random_tree_solution(G, src))

# -------------- if you feel like you don't have enough computing power, you can comment code block below --------------
    if len(G.nodes()) <= 25:
        bfT = BruteForce(G, 20)
        if ((not nx.is_empty(bfT)) and (nx.is_tree(bfT)) and (nx.is_connected(bfT)) and (is_valid_network(G, bfT))):
            Ts.append(bfT)
# ----------------------------------------------------------------------------------------------------------------------

    return min(Ts, key=lambda T: average_pairwise_distance_fast(T))


# Here's an example of how to run your solver.
# Usage: python3 solver.py test.in
if __name__ == '__main__':
    assert len(sys.argv) == 2
    path = sys.argv[1]
    G = read_input_file(path)
    T = solve(G)
    assert is_valid_network(G, T)
    print("Average pairwise distance: {}".format(average_pairwise_distance(T)))
    write_output_file(T, 'test.out')
