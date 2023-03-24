import numpy as np
import math
n = int(input())
gates = []
gates.append([i for i in range(n)])
depth = math.ceil(np.log2(n))
for lvl in range(depth):
    last = gates[-1][-1]
    tmp = [last + i for i in range(1, n - 2 ** lvl + 1)]
    gates.append([gates[-1][j] for j in range(n - len(tmp))] + tmp)
gates = np.array(gates)
complexity = math.ceil(n * np.log2(n)) + 1
for d in range(1, gates.shape[0]):
    for i in range(2 ** (d-1), n):
        print("GATE", gates[d, i], "OR",
              gates[d - 1, i - 2 ** (d-1)], gates[d-1, i])
for i in range(n):
    print("OUTPUT", i, gates[-1, i])