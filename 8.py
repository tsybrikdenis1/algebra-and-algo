import numpy as np
from scipy.sparse import dok_matrix
from scipy.optimize import linprog
vertex_num = int(input())
vertex_weight = []
for _ in range(vertex_num): 
     vertex_weight.append(int(input()))
edges_num = int(input())
sparse_matrix = dok_matrix((edges_num, vertex_num), dtype=np.int8)
for row_num in range(edges_num): 
    i, j = map(int, input().split())
    sparse_matrix[row_num, i] = -1.
    sparse_matrix[row_num, j] = -1.
b = np.full((1, edges_num), -1)
boundaries = [(0, 1) for _ in range(vertex_num)]
res = linprog(vertex_weight, A_ub=sparse_matrix, b_ub=b, bounds=boundaries, method='interior-point', options={"sparse":True, "tol": 1e-2})
vertex_ids = np.around(res.x)
s = ''
for i in range(len(vertex_ids)): 
    if vertex_ids[i] == 1: 
        s += str(i) + ' '
print(s)