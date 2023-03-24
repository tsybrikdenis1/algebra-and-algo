import numpy as np
import sys


def matrix_split(A):
    n = A.shape[0]
    A11 = A[: n >> 1, : n >> 1]
    A12 = A[: n >> 1, n >> 1 :]
    A21 = A[n >> 1 :, : n >> 1]
    A22 = A[n >> 1 :, n >> 1 :]
    return A11, A12, A21, A22


def matrix_sum(A, B):
    rowNum, columNum = A.shape
    res = np.zeros((rowNum, columNum))
    for i in range(rowNum):
        for j in range(columNum):
            res[i][j] = A[i][j] + B[i][j]
    return res


def matrix_subtract(A, B):
    rowNum, columNum = A.shape
    res = np.zeros((rowNum, columNum))
    for i in range(rowNum):
        for j in range(columNum):
            res[i][j] = A[i][j] - B[i][j]
    return res


def strassen_multiply(A, B):
    rowNum, columNum = A.shape
    res = np.zeros((rowNum, columNum))

    if len(A) == 1 and len(B) == 1:
        return np.array([[A[0][0] * B[0][0]]])

    A11, A12, A21, A22 = matrix_split(A)
    B11, B12, B21, B22 = matrix_split(B)

    M1 = strassen_multiply(matrix_sum(A11, A22), matrix_sum(B11, B22))
    M2 = strassen_multiply(matrix_sum(A21, A22), B11)
    M3 = strassen_multiply(A11, matrix_subtract(B12, B22))
    M4 = strassen_multiply(A22, matrix_subtract(B21, B11))
    M5 = strassen_multiply(matrix_sum(A11, A12), B22)
    M6 = strassen_multiply(matrix_subtract(A21, A11), matrix_sum(B11, B12))
    M7 = strassen_multiply(matrix_subtract(A12, A22), matrix_sum(B21, B22))

    C11 = matrix_sum(matrix_subtract(matrix_sum(M1, M4), M5), M7)
    C12 = matrix_sum(M3, M5)
    C21 = matrix_sum(M2, M4)
    C22 = matrix_sum(matrix_sum(matrix_subtract(M1, M2), M3), M6)

    res[: rowNum >> 1, : columNum >> 1] = C11
    res[: rowNum >> 1, columNum >> 1 :] = C12
    res[rowNum >> 1 :, : columNum >> 1] = C21
    res[rowNum >> 1 :, columNum >> 1 :] = C22
    return res


def multiply_matrices(A, B):
    n = A.shape[0]
    if (n & (n - 1)) == 0:
        return strassen_multiply(A, B)
    else:
        m = 1
        while m < n:
            m *= 2
        tmp_A = np.zeros((m, m))
        tmp_B = np.zeros((m, m))
        tmp_A[:n, :n] = A.copy()
        tmp_B[:n, :n] = B.copy()
        return strassen_multiply(tmp_A, tmp_B)[:n, :n].astype(np.uint8)


def seidel_algo(A, G):
    Z = multiply_matrices(A, A)
    B = np.zeros((A.shape[0], A.shape[1]))
    for i in range(Z.shape[0]):
        for j in range(Z.shape[1]):
            if i != j and (A[i, j] == 1 or Z[i, j] > 0):
                B[i, j] = 1
    if all(B[i, j] for i in range(A.shape[0]) for j in range(A.shape[1]) if i != j):
        return 2 * B - A, G
    T, G = seidel_algo(B, G)
    X = multiply_matrices(T, A)
    D = np.zeros((A.shape[0], A.shape[1]))
    for u in range(A.shape[0]):
        for v in range(A.shape[1]):
            if u != v and X[u, v] >= len(G[v]) * T[u, v]:
                D[u, v] = 2 * T[u, v]
            elif u != v:
                D[u, v] = 2 * T[u, v] - 1
    return D, G


def main():
    G = {}
    for input in sys.stdin:
        v1, v2 = map(int, input.split())
        for v, u in (v1, v2), (v2, v1):
            if v not in G:
                G[v] = {u}
            else:
                G[v].add(u)
    vertices_num = max(G.keys()) + 1
    A = np.zeros((vertices_num, vertices_num), dtype=np.int8)
    for vertex in G:
        for neighbor in G[vertex]:
            A[vertex, neighbor] = 1
            A[neighbor, vertex] = 1
    result, _ = seidel_algo(A, G)
    unique_elements, counts_elements = np.unique(result, return_counts=True)
    for indx in range(1, len(unique_elements)):
        print(int(unique_elements[indx]), int(counts_elements[indx] // 2))


if __name__ == "__main__":
    main()