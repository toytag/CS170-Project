import os
import read

# ----------------------------------------------------------------
# input_dir = "./inputs"
# for file_name in os.listdir(input_dir):
#     with open(os.path.join(input_dir, file_name), 'r') as f:
#         adjmat = read.read_input_lines_as_adjmat(f.readlines())
#     print(adjmat)
# ----------------------------------------------------------------

# ---------------------------- test ------------------------------
# with open("/home/project/CS170-Project/25.in") as f:
#     adjmat = read_input_file_as_adjmat(f)
# for i in range(25):
#     for j in range(i):
#         assert adjmat[i, j] == adjmat[j, i]
# ---------------------------- test ------------------------------

# ---------------------------- test ------------------------------
import networkx as nx
import matplotlib.pyplot as plt

with open("./our_inputs/25.in", 'r') as f:
    adjmat = read.read_input_file_as_adjmat(f)

G = nx.from_numpy_matrix(adjmat)
nx.draw_circular(G)
plt.savefig("graph.png")
plt.cla()

T = nx.minimum_spanning_tree(G)
nx.draw_circular(T)
plt.savefig("tree.png")
# ---------------------------- test ------------------------------