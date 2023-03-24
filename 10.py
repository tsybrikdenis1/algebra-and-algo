import numpy as np 
from numpy import linalg as LA
edgesNum = int(input())
G = {} 
for _ in range(edgesNum): 
    v1, v2 = map(int, input().split())
    for v, u in (v1, v2), (v2, v1): 
        if v not in G: 
            G[v] = {u}
        else: 
            G[v].add(u)
laplacian_matrix = np.zeros((max(G.keys()) + 1, max(G.keys()) + 1))
for v_i in G: 
    for v_j in G[v_i]: 
        laplacian_matrix[v_i, v_i] = len(G[v_i])
        laplacian_matrix[v_i, v_j] = -1 
        laplacian_matrix[v_j, v_i] = -1 
w, v = LA.eigh(laplacian_matrix)
indxs_eigen_vector = np.argsort(v[:,1])[::-1]
candidate_split = []
candidate_split_weights = []
for k in range(1, max(G.keys()) + 1):
    A = indxs_eigen_vector[:k]
    B = indxs_eigen_vector[k:]
    if len(A) < len(B): 
        candidate_split.append(sorted(A))
    else: 
        candidate_split.append(sorted(B)) 
    counter = 0 
    for v1 in A: 
        for v2 in G[v1]: 
            if v2 in B: 
                counter += 1
    candidate_split_weights.append(counter)         
split_indxs = np.argsort(candidate_split_weights)
minimal_splits_count = candidate_split_weights.count(candidate_split_weights[split_indxs[0]])
if minimal_splits_count > 1: 
    tmp = []
    for i in range(minimal_splits_count):
        tmp.append(candidate_split[split_indxs[i]])
    print(*min(tmp, key=max))
else:
    print(*candidate_split[split_indxs[0]])