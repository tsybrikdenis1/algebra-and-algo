import numpy as np 
import random
base = 9973
iterationNum = 20

def gcd(a: int, b: int): 
    if a == 0: 
        return 0, 1
    tmpx, tmpy = gcd(b % a, a)
    return tmpy - (b // a) * tmpx, tmpx

def find_reverse_in_field(number: int, m: int = base):
    x, y = gcd(number, m)
    return (x % m + m) % m

def find_triangle_view(array: np.array, m: int = base): 
    matrix = np.copy(array)
    n = matrix.shape[0]
    for i in range(1, n): 
        col = i - 1
        row = None 
        for indx in range(col, n):
            if matrix[indx, col] != 0: 
                row = indx
                break
        if row is None: 
            continue 
        if row != col: 
            matrix[[col, row]] = matrix[[row, col]]
        row = col 
        a = matrix[row, col]
        aReversed = find_reverse_in_field(a)
        for j in range(row + 1, n): 
            b = matrix[j, col]
            if b == 0: 
                continue 
            k = (b * aReversed) % m
            resRow = []
            for x, y in zip(matrix[row], matrix[j]):
                z = (y - k * x) % m
                resRow.append(z if z>=0 else z + n)
            matrix[j] = resRow
    return matrix 

def main():
    edgesNum = int(input()) 
    G = {} 
    for _ in range(edgesNum): 
        v1, v2 = map(int, input().split())
        if v1 not in G: 
            G[v1] = {v2}
        else: 
            G[v1].add(v2)
    numVert = len(G)
    for _ in range(iterationNum):
        m = np.zeros((numVert, numVert))
        for indx in range(numVert): 
            for v in G[indx]:
                m[indx, v] = random.randint(1, base - 1)
        triangle =  find_triangle_view(m)
        if len(np.nonzero(np.diagonal(triangle))[0]) == numVert: 
            print('yes')
            return 
    print('no')

if __name__ == '__main__':
    main()