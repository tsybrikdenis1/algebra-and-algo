def main():
    n = int(input())
    gates = [i for i in range(15 * n + 1)]
    outs = [i for i in range(2 * n + 2)]
    for d, i in zip(range(n),range(3 * n, 3 * n + 12 * n + 1, 12)) : 
        print("GATE", gates[i], "NOT",
              gates[d])
        print("GATE", gates[i + 1], "AND",
              gates[n + d], gates[2 * n + d])
        print("GATE", gates[i + 2], "NOT",
              gates[i + 1])
        print("GATE", gates[i + 3], "OR",
              gates[n + d], gates[2 * n + d])
        print("GATE", gates[i + 4], "AND",
              gates[i + 2], gates[i + 3])
        print("GATE", gates[i + 5], "AND",
              gates[i], gates[i + 4])
        print("GATE", gates[i + 6], "NOT",
              gates[i + 3])
        print("GATE", gates[i + 7], "OR",
              gates[i + 1], gates[i + 6])
        print("GATE", gates[i + 8], "AND",
              gates[d], gates[i + 7])
        print("GATE", gates[i + 9], "OR",
              gates[i + 5], gates[i + 8])
        print("GATE", gates[i + 10], "AND",
              gates[d], gates[i + 4])
        print("GATE", gates[i + 11], "OR",
              gates[i + 1], gates[i + 10])
        outs[d] = i + 9 
        outs[d + n + 2] = i + 11 
        
    print("GATE", gates[i + 12], "AND",
                  gates[0], gates[3 * n])
    outs[n] = i + 12
    outs[n + 1] = i + 12
    for i in range(2 * n + 2): 
        print("OUTPUT", i, outs[i])
                
if __name__ == '__main__':
    main()