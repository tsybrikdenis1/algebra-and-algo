import numpy as np 
n = int(input())
p = n - 1
legendre = dict.fromkeys([_ for _ in range(p)])
legendre[0] = 0
for a in range(1, p // 2 + 1):
    legendre[a ** 2 % p] = 1
for key in legendre:
    if legendre[key] == None:
        legendre[key] = -1 
smallMatrix = np.full((p, p), -1)
for i in range(p): 
    for j in range(p): 
        if i != j: 
            smallMatrix[i, j] = legendre[(j - i) % p]
H = np.ones((n, n))
H[1:, 1:] = smallMatrix
hadamard = np.vstack([H, -H])
for row in hadamard: 
    s = '' 
    for elem in row: 
        if elem == 1: 
            s += '1'
        else: 
            s += '0'
    print(s)