from parse import *
import networkx as nx
import os
from solver import solve
import multiprocessing

if __name__ == "__main__":
    output_dir = "outputs"
    input_dir = "inputs"
    cnt = 1
    for input_path in os.listdir(input_dir):
        graph_name = input_path.split(".")[0]
        print(cnt, graph_name, f"\t{cnt/1006*100 : .2f}%", end="\r")
        cnt += 1
        G = read_input_file(f"{input_dir}/{input_path}")
        T = solve(G)
        write_output_file(T, f"{output_dir}/{graph_name}.out")
