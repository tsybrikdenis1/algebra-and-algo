import numpy as np

n, m = map(int, input().split())
clauses = []
for _ in range(m):
    clauses.append(list(map(int, input().split())))
k = int(np.ceil(np.log2(n)) + 1)
matrix = np.zeros((k, 2 ** (k - 1)), dtype=np.int8)
matrix[
    0,
] = 1
for j in range(2 ** (k - 1)):
    binary_record = list(map(int, bin(j)[2:].rjust(k - 1, "0")))
    for i, l in zip(range(k - 1, 0, -1), range(k - 1)):
        matrix[i, j] = binary_record[l]
matrix = matrix[:, :n]
result = []
for var_values in matrix:
    counter = 0
    for clause in clauses:
        x = (
            lambda ind: var_values[ind - 1]
            if ind > 0
            else not (var_values[abs(ind) - 1])
        )
        counter += x(clause[0]) or x(clause[1]) or x(clause[2])
    result.append(counter)
treshhold = 7 / 8 * m
for val_indx in range(len(result)):
    if result[val_indx] > treshhold:
        print(*matrix[val_indx], sep="")
        break