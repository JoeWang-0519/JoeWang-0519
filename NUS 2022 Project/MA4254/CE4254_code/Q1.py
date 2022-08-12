from pulp import *
import numpy as np


def FLP_Solver(c, dd, M, N, output=False):

    #2(A). Solve FLP(use PuLP)
    PB_FLP = LpProblem (name = 'FLP', sense = LpMinimize)

    x_FLP = [LpVariable(f'x{i,j}', lowBound = 0, upBound = 1, cat ='continuous') for i in range(1, M+1) for j in range(1, N+1)]
    y_FLP = [LpVariable(f'y{j}', cat = 'Binary') for j in range(1, N+1)]

    #objective
    PB_FLP += lpDot(x_FLP, dd) + lpDot(y_FLP, c)
    #constraints
    vector_one1 = np.ones(N)
    #equality
    for i in range(1, M+1):
        PB_FLP += (lpDot(vector_one1, x_FLP[(i-1)*N : i*N]) == 1)
    #ineuqality
    for j in range(1, N+1):
        for i in range(1, M+1):
            PB_FLP += (x_FLP[(i-1)*N + j-1] - y_FLP[j-1] <= 0)

    # solve

    PB_FLP.solve()
    if output == True:
        print("Status:", LpStatus[PB_FLP.status])
        for v in PB_FLP.variables():
            if v.varValue > 0:
                print(v.name, "=", v.varValue)

        print('=========================================================FLP=========================================================')
        print('=========================================================FLP=========================================================')
    return value(PB_FLP.objective), PB_FLP.variables()


def AFL_Solver(c, dd, M, N, output=False):
    # 2(B). Solve AFL(use PuLP)
    PB_AFL = LpProblem(name='AFL', sense=LpMinimize)

    x_AFL = [LpVariable(f'x{i, j}', lowBound=0, upBound=1, cat='continuous') for i in range(1, M+1) for j in range(1, N+1)]
    y_AFL = [LpVariable(f'y{j}', cat='Binary') for j in range(1, N+1)]

    # objective
    PB_AFL += lpDot(x_AFL, dd) + lpDot(y_AFL, c)
    # constraints
    vector_one1 = np.ones(N)
    # equality
    for i in range(1, M+1):
        PB_AFL += (lpDot(vector_one1, x_AFL[(i-1) * N: i * N]) == 1)
    # ineuqality
    for j in range(1, N+1):
        temp = 0
        for i in range(1, M+1):
            temp += x_AFL[j-1 + (i-1) * N]
        PB_AFL += (temp - M * y_AFL[j-1] <= 0)

    # solve
        
    PB_AFL.solve()
    if output==True:
        print("Status:", LpStatus[PB_AFL.status])
        for v in PB_AFL.variables():
            if v.varValue > 0:
                print(v.name, "=", v.varValue)
        
        print('=========================================================AFL=========================================================')
        print('=========================================================AFL=========================================================')
    return value(PB_AFL.objective)


def FLP_LR_Solver(c, dd, M, N, output=False):
    # 2(C). Solve FLP_LR(use PuLP)

    PB_FLP_LR = LpProblem(name='FLP_LR', sense=LpMinimize)

    x_FLP_LR = [LpVariable(f'x{i, j}', lowBound=0, upBound=1, cat='LpContinuous') for i in range(1, M+1) for j in range(1, N+1)]
    y_FLP_LR = [LpVariable(f'y{j}', lowBound=0, upBound=1, cat='LpContinuous') for j in range(1, N+1)]

    # objective
    PB_FLP_LR += lpDot(x_FLP_LR, dd) + lpDot(y_FLP_LR, c)
    # constraints
    vector_one1 = np.ones(N)
    # equality
    for i in range(1, M+1):
        PB_FLP_LR += (lpDot(vector_one1, x_FLP_LR[(i-1) * N: i * N]) == 1)
    # ineuqality
    for j in range(1, N+1):
        for i in range(1, M+1):
            PB_FLP_LR += (x_FLP_LR[(i-1) * N + j-1] - y_FLP_LR[j-1] <= 0)

    # solve

    PB_FLP_LR.solve()
    if output == True:
        print("Status:", LpStatus[PB_FLP_LR.status])
        for v in PB_FLP_LR.variables():
            if v.varValue > 0:
                    print(v.name, "=", v.varValue)

        print('=========================================================FLP_LR=========================================================')
        print('=========================================================FLP_LR=========================================================')
    return value(PB_FLP_LR.objective)


def AFL_LR_Solver(c, dd, M, N, output=False):
    # 2(D). Solve AFL_LR(use PuLP)
    PB_AFL_LR = LpProblem(name='AFL_LR', sense=LpMinimize)

    x_AFL_LR = [LpVariable(f'x{i,j}', lowBound=0, upBound=1, cat='continuous') for i in range(1, M+1) for j in range(1, N+1)]
    y_AFL_LR = [LpVariable(f'y{j}', lowBound=0, upBound=1, cat='continuous') for j in range(1, N+1)]
    # objective
    PB_AFL_LR += lpDot(x_AFL_LR, dd) + lpDot(y_AFL_LR, c)
    # constraints
    # equality
    for i in range(1, M+1):
        PB_AFL_LR += (lpSum(x_AFL_LR[(i - 1) * N: i * N]) == 1)
    # ineuqality
    for j in range(1, N+1):
        temp=0
        for i in range(1, M+1):
            temp += x_AFL_LR[j-1 + (i-1)*N]
        PB_AFL_LR += (temp - M*y_AFL_LR[j-1] <= 0)
    # solve

    PB_AFL_LR.solve()
    if output == True:
        print("Status:", LpStatus[PB_AFL_LR.status])
        for v in PB_AFL_LR.variables():
            if v.varValue > 0:
                print(v.name, "=", v.varValue)

        print('=========================================================AFL_LR=========================================================')
        print('=========================================================AFL_LR=========================================================')
    return value(PB_AFL_LR.objective)
