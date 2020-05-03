import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_network, average_pairwise_distance
import sys
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt



# def sort_append(l,n,d):
#     i = 0
#     while i < len(l):
#         if l[i][1] > d:
#             i += 1
#         else:
#             break
#     l.insert(i, (n,d))


def solve_from_src(G, src):
    T = nx.Graph()
    T.add_nodes_from(G)
    for dst, path in nx.single_source_dijkstra_path(G, source=src).items():
        if len(path) >= 2:
            for u, v in zip(path[:-1], path[1:]):
                T.add_edge(u, v, weight=G[u][v]["weight"])
    while True:
        converge = True
        d1_vs = sorted([v for v, d in T.degree() if d == 1], key=lambda v: G.degree(v))
        for v in d1_vs:
            T_tmp = T.copy()
            T_tmp.remove_node(v)
            if nx.is_dominating_set(G, T_tmp.nodes) and average_pairwise_distance(T_tmp) <= average_pairwise_distance(T):
                converge = False
                T.remove_node(v)
        if converge:
            break
    return T

def prune(G, T):
    while True:
        converge = True
        d1_vs = sorted([v for v, d in T.degree() if d == 1], key=lambda v: G.degree(v))
        for v in d1_vs:
            T_tmp = T.copy()
            T_tmp.remove_node(v)
            if nx.is_dominating_set(G, T_tmp.nodes) and average_pairwise_distance(T_tmp) <= average_pairwise_distance(T):
                converge = False
                T.remove_node(v)
        if converge:
            break
    return T


def BruteForce(G, n):
    num = G.size if n > G.size else n
    optimalT = nx.Graph()
    nodes = G.nodes.items()
    minAvgDistance = INT_MAX
    for chosen in combinations(nodes, num):
        T = nx.minimum_spanning_tree(G)
        T = prune(G, T)
        apd = average_pairwise_distance(T)
        if apd < minAvgDistance:
            minAvgDistance = apd
            optimalT = T.copy()
    
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
    sources = sorted(counter.items(), key=lambda x: x[-1], reverse=True)

    if len(sources) > 5:
        sources = sources[:5]

    Ts = []
    for src in sources:
        T = solve_from_src(G, src[0])
        Ts.append([T, average_pairwise_distance(T)])

    return min(Ts, key=lambda x: x[-1])[0]

    # ----------------------------------------------------------------

    # counter = {node: 0 for node in G.nodes()}
    # for src, dsts in nx.all_pairs_dijkstra_path(G):
    #     for dst, path in dsts.items():
    #         for node in path[1:-1]:
    #             counter[node] += 1
    # cur, cur_degree = sorted(counter.items(), key=lambda x: x[-1], reverse=True)[0]

    # T = nx.Graph()
    # T.add_nodes_from(G)
    # for dst, path in nx.single_source_dijkstra_path(G, source=cur).items():
    #     if len(path) >= 2:
    #         for u, v in zip(path[:-1], path[1:]):
    #             T.add_edge(u, v, weight=G[u][v]["weight"])

    # while True:
    #     converge = True
    #     d1_vs = [v for v, d in T.degree() if d == 1]
    #     for v in d1_vs:
    #         T_tmp = T.copy()
    #         T_tmp.remove_node(v)
    #         if is_valid_network(G, T_tmp) and average_pairwise_distance(T_tmp) <= average_pairwise_distance(T):
    #             converge = False
    #             T.remove_node(v)
    #     if converge:
    #         break
    # return T

    # ----------------------------------------------------------------
    
    # cost = 0
    # while len(reachable_node) < len(G.nodes()):
    #     for neighbor in G[cur]:
            
    # nx.single_source_dijkstra_path(G, source=)
    
    # T = nx.minimum_spanning_tree(G)
    # d1_vs = [v for v, d in T.degree() if d == 1]

    # # T.degree().sort(key=lambda x: x[-1])

    # for v in d1_vs:
    #     T_tmp = T.copy()
    #     T_tmp.remove_node(v)
    #     if average_pairwise_distance(T_tmp) <= average_pairwise_distance(T):
    #         T.remove_node(v)
    # return T

    # ----------------------------------------------------------------

    # G_1 = G
    # reachable_node = []
    # sorted_degree = []

    # # 去掉所有 degree 为 1 的点

    # for node in G.nodes():
    #     if len(G[node]) == 1:
    #         G_1.remove_node(node)

    # T = nx.minimum_spanning_tree(G_1)

    # i = 0
    # while i < T.number_of_nodes():
    #     if len(T[node]) == 1:
    #         fail = 0
    #         for neighbor in G[node]:
    #             flag = 0
    #             for adj in G[neighbor]:
    #                 if adj in T.nodes():
    #                     flag = 1
    #                     break
    #             if flag == 0:
    #                 fail = 1
    #                 break
    #         if fail == 0:
    #             T.remove_node(node)
    #             i -= 1
    #     i += 1
        
    # return T

    # ----------------------------------------------------------------

    # # 1. 不添加所有degree为1的点
    # # 2. 添加所有链接degree为1的点的点
    # for node, degree in G.degree():
    #     # print(node, degree)
    #     if degree == 1:
    #         for neighbor in G.neighbors(node):  # only one neighbor
    #             N.add_node(neighbor)
    #         for reach in G.neighbors(neighbor):
    #             reachable_node.append(reach)
    #     else:
    #         sort_append(sorted_degree, node, degree)

    # print(N.nodes())

    ### 从 degree 最大的点开始：
    # 1.找 degree 最大的
    # start = sorted_degree[0][0]
    # while len(reachable_node) < G.number_of_nodes():
    #     max_degree = 0
    #     next = None
    #     for neighbor in G[start]:
    #         reachable_node.append(neighbor)
    #         if len(G[neighbor]) > max_d"egree:
    #             max_degree = len(G[neighbor])
    #             next = neighbor
            
            

    # #while 
    # for (node, degree) in sorted_degree:

    #     if node not in reachable_node:
    #         N.add_node(node)
    #         for reach in G.neighbors(node):
    #             reachable_node.append(reach)

    # Nnodes = N.nodes()
    # print(Nnodes)
    # for (x, y) in G.edges():
    #     if x in Nnodes and y in Nnodes:
    #         N.add_edge(x, y, weight=G[x][y]['weight'])


    # return N


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
