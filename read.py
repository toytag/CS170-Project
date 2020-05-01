import numpy as np

def read_input_lines_as_adjmat(lines):
    num_vertices = int(lines[0])
    adjmat = np.zeros((num_vertices, num_vertices))
    for line in lines[1:]:
        edge = line.split()
        if edge != []:
            u, v, d = int(edge[0]), int(edge[1]), float(edge[2])
            adjmat[u, v] = adjmat[v, u] = d
    return adjmat

def read_input_string_as_adjmat(string):
    return read_input_lines_as_adjmat(string.split('\n'))

def read_input_file_as_adjmat(f):
    return read_input_string_as_adjmat(f.read())
