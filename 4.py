import numpy as np
import sys


def matrix_print(A):
    for row in A:
        print(' '.join([str(x) for x in row]))


def matrix_split(A): 
    n = A.shape[0]
    A11 = A[:n >> 1, :n >> 1]
    A12 = A[:n >> 1, n >> 1:]
    A21 = A[n >> 1:, :n >> 1]
    A22 = A[n >> 1:, n >> 1:]
    return A11, A12, A21, A22


def matrix_sum(A, B):
    rowNum, columNum = A.shape
    res = np.zeros((rowNum, columNum))
    for i in range(rowNum):
        for j in range(columNum): 
            res[i][j] = (A[i][j] + B[i][j]) % 9
    return res


def matrix_subtract(A, B):
    rowNum, columNum = A.shape
    res = np.zeros((rowNum, columNum))
    for i in range(rowNum):
        for j in range(columNum): 
            res[i][j] = (A[i][j] - B[i][j]) % 9
    return res


def strassen_multiply(A, B):
    rowNum, columNum = A.shape
    res = np.zeros((rowNum, columNum))
    
    if len(A) == 1 and len(B) == 1: 
        return np.array([[(A[0][0] * B[0][0]) % 9]])
    
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
    
    res[:rowNum >> 1, :columNum >> 1] = C11
    res[:rowNum >> 1, columNum >> 1:] = C12
    res[rowNum >> 1:, :columNum >> 1] = C21
    res[rowNum >> 1:, columNum >> 1:] = C22
    return res


def bin_pow(A, n, m): 
    if n == 0: 
        return np.eye(m)
    elif n % 2 == 1: 
        return strassen_multiply(bin_pow(A, n - 1, m), A)
    else: 
        tmp = bin_pow(A, n // 2, m)
        return strassen_multiply(tmp, tmp)


def main():
    matrix = []
    for line in sys.stdin:
        matrix.append([int(x) for x in line.split()])
    n = len(matrix)
    if (n & (n - 1)) == 0:
        matrix_print(bin_pow(matrix, n, n).astype(np.uint8))
    else:
        m = 1
        while m < n:
            m *= 2
        newMatrix = np.zeros((m, m))
        newMatrix[:n, :n] = matrix.copy()
        tmpRes = bin_pow(newMatrix, n, m)
        matrix_print(tmpRes[:n, :n].astype(np.uint8))
  
    
if __name__ == '__main__':
    main()