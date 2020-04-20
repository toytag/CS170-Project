import numpy as np
size = 100
selectivity = 0.2
vertices = [i for i in range(size)]
edges = []
u = vertices.pop(np.random.randint(size))
while len(vertices) > 0:
    v = vertices.pop(np.random.randint(len(vertices)))
    length = np.random.rand()*100
    length = round(length, 3)
    edges.append([u,v])
    edges.append([v,u])
    print(u, v, length)
    u = v

for j in range(size):
    for k in range(j+1, size):
        if np.random.rand() <= selectivity and [j, k] not in edges:
            length = np.random.rand()*100
            length = round(length, 3)
            print(j, k, length)

    # u = vertices.pop(0)
    # for v in range(u+1, size):
    #     if np.random.rand() <= selectivity:
    #         length = np.random.rand()*100
    #         length = round(length, 3)
    #         print(u, v, length)
    #         vertices.remove(v)
            
    # v = vertices.pop(np.random.randint(size))
    # length = np.random.rand()*100
    # length = round(length, 3)
    # print(u, v, length)
    # u = v

# matrix = np.zeros(shape=(size,3))
#for j in range(size):
#    for k in range(j+1, size):
#        if np.random.rand() <= selectivity:
#            length = np.random.rand()*100
#            length = round(length, 3)
            # matrix[j] = ([j, k, length])
#            print(j, k, length)
