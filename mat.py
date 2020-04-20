import numpy as np

mat = np.random.uniform(0, 1, size=(25, 25))
adjMat = np.round(mat.T @ mat, decimals=2)

for i in range(25):
    for j in range(i):
        print(i, j, adjMat[i, j])