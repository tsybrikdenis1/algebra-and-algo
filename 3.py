import math 
from itertools import combinations
n = int(input())
if n == 1: 
    print('GATE 1 NOT 0')
    print('GATE 2 AND 0 1')
    print('GATE 3 OR 0 1')
    print('OUTPUT 0 0')
    print('OUTPUT 1 1')
    print('OUTPUT 2 2')
    print('OUTPUT 3 3')
else:
    inputs = dict.fromkeys([x for x in range(n)])
    invertion = {x + n: x for x in inputs.keys()}
    gatesToCombine = [x for x in range(2 * n)]
    lastGateNumber = 2 * n
    conjunction = []
    for level in range(n - 1): 
        allCombinations = list(combinations(gatesToCombine, level + 2))
        correctCombinations = []
        for combination in allCombinations: 
            flag = True
            for i in range(len(combination) - 1):
                for j in range(i + 1, len(combination)):
                    if combination[j] == combination[i] + n:
                        flag = False
                        break 
            if flag: 
                correctCombinations.append(combination)
        if not conjunction: 
            tmpDict = {x + lastGateNumber: correctCombinations[x] for x in range(len(correctCombinations))}
            lastGateNumber = list(tmpDict.keys())[-1] + 1
            conjunction.append(tmpDict)
            lastLevelRawDict = tmpDict 
        else: 
            lastLevelRawDict = {x + lastGateNumber: correctCombinations[x] for x in range(len(correctCombinations))}       
            for indx in range(len(conjunction)): 
                replacemenedCombination = []
                for key in conjunction[indx]:
                    for combination in correctCombinations: 
                        if combination[slice(2)] == conjunction[indx][key]:
                            replacemenedCombination.append(tuple([key] + list(combination[slice(2, len(combination))])))
                correctCombinations = replacemenedCombination.copy()      
            tmpDict = {x + lastGateNumber: replacemenedCombination[x] for x in range(len(replacemenedCombination))}
            lastGateNumber = list(tmpDict.keys())[-1] + 1
            conjunction.append(tmpDict)
    def convertCombinationToBool(comb):
        res = [None] * n 
        for element in comb: 
            for i in range(n):
                if element == i or element - n == i:
                    if element > n - 1:
                        res[i] = 1
                    else: 
                        res[i] = 0
        return tuple(res)
    def converBoolToCombination(comb): 
        res = []
        for i in range(len(comb)): 
            if comb[i] == 1: 
                res.append(i + n)
            else: 
                res.append(i)
        return tuple(sorted(res))
    rawDisjunction = []
    rawCombinations = list(lastLevelRawDict.values())
    booleanCombinations = []
    for combination in rawCombinations: 
        booleanCombinations.append(convertCombinationToBool(combination))
    for level in range(2 ** n - 1): 
        allBooleanCombinations = list(combinations(booleanCombinations, level + 2))
        if ((level + 2) & (level + 1)) == 0 and level + 2 <= (n + 1): 
            correctBooleanCombinations = []
            if level + 2 == 2: 
                for indx in range(len(allBooleanCombinations)):
                #     если как минимум в двух позициях у наборов стоят разные значения
                    if sum(list(set1 ^ set2 for set1, set2 in zip(allBooleanCombinations[indx][0], allBooleanCombinations[indx][1]))) > 1:
                        correctBooleanCombinations.append([allBooleanCombinations[indx][0], allBooleanCombinations[indx][1]])
            if level + 2 == 4: 
                for indx in range(len(allBooleanCombinations)):
                    a =sum(list(set1 ^ set2 for set1, set2 in zip(allBooleanCombinations[indx][0], allBooleanCombinations[indx][1])))
                    b = sum(list(set1 ^ set3 for set1, set3 in zip(allBooleanCombinations[indx][0], allBooleanCombinations[indx][2])))
                    c = sum(list(set1 ^ set4 for set1, set4 in zip(allBooleanCombinations[indx][0], allBooleanCombinations[indx][3])))
                    d = sum(list(set2 ^ set3 for set2, set3 in zip(allBooleanCombinations[indx][1], allBooleanCombinations[indx][2])))
                    e = sum(list(set2 ^ set4 for set2, set4 in zip(allBooleanCombinations[indx][1], allBooleanCombinations[indx][3])))
                    f = sum(list(set3 ^ set4 for set3, set4 in zip(allBooleanCombinations[indx][2], allBooleanCombinations[indx][3])))
                    if sum([a, b, c, d, e, f]) > 8:
                        correctBooleanCombinations.append([allBooleanCombinations[indx][0], allBooleanCombinations[indx][1], allBooleanCombinations[indx][2], allBooleanCombinations[indx][3]])
        else: 
            correctBooleanCombinations = allBooleanCombinations
        rawCorrectCombinations = []
        for listElement in correctBooleanCombinations: 
            tmp = []
            for combination in listElement: 
                rawCombination = converBoolToCombination(combination)
                tmp.append(rawCombination)
            rawCorrectCombinations.append(tmp)
        rawDisjunction.append(rawCorrectCombinations)
    disjunction = []
    for layer in rawDisjunction:
        for gate in layer: 
            for indx in range(len(gate)): 
                for key in lastLevelRawDict: 
                    if gate[indx] == lastLevelRawDict[key]:
                        gate[indx] = key
                        break 
    tmpDict = {x + lastGateNumber: rawDisjunction[0][x] for x in range(len(rawDisjunction[0]))}
    lastGateNumber = list(tmpDict.keys())[-1] + 1
    disjunction.append(tmpDict)
    lastLevelRawDict = tmpDict
    for level in range(1, 2 ** n - 1): 
        for layer in rawDisjunction[level:]:
            for gateIndex in range(len(layer)): 
                for key in lastLevelRawDict:
                    set1 = set(lastLevelRawDict[key])
                    set2 = set(layer[gateIndex])
                    if set1.issubset(set2):
                        tmp = list(set2.difference(set1))
                        tmp.append(key)
                        layer[gateIndex] = tmp
                        break
        tmpDict = {x + lastGateNumber: rawDisjunction[level][x] for x in range(len(rawDisjunction[level]))}
        lastGateNumber = list(tmpDict.keys())[-1] + 1
        disjunction.append(tmpDict)
        lastLevelRawDict = tmpDict             
    for key in invertion: 
        print("GATE", key, "NOT",
                  invertion[key])
    for indx in range(len(conjunction)): 
        for key in conjunction[indx]: 
            print("GATE", key, "AND",
                      *conjunction[indx][key])
    for indx in range(len(disjunction)): 
        for key in disjunction[indx]: 
            print("GATE", key, "OR",
                      *disjunction[indx][key])
    print("GATE", 2 ** 2 ** n - 1, "AND",
                      0, 0 + n)
    for indx in range(2 ** 2 ** n): 
        print("OUTPUT", indx, indx)