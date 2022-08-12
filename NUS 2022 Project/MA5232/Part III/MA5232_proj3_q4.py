import numpy as np
import itertools
import matplotlib.pyplot as plt
import random
import cvxpy as cvx

# For some reasons (I cannot find help on Google), my code cannot run in colab. Therefore, I use Pycharm instead.
def Generate_Z(m, n, r):
    U = np.random.normal(loc=0, scale=1.0, size=(m, r))
    V = np.random.normal(loc=0, scale=1.0, size=(n, r))
    Z = U @ V.T  # m * n
    return Z


def Generate_loc(m, n, k):
    candidate = list(itertools.product(range(m), range(n)))
    omega = random.sample(candidate, k)
    # Omega = np.array(omega)           # we only need tuple here
    return omega


def SDP_CompleteMat(Z, omega):
    [m, n] = Z.shape

    X = cvx.Variable((m + n, m + n), symmetric=True)
    # actually should be 1/2 * objective
    objective = cvx.Minimize(cvx.trace(X))

    constraints = [X >> 0]
    # construct constraint Matrix A[i]
    A = []
    for idx in omega:
        tmp = np.zeros((m + n, m + n))
        tmp[idx[1] + m, idx[0]] = 1
        A.append(tmp)

    constraints += [cvx.trace(A[i] @ X) == Z[omega[i]] for i in range(len(omega))]

    prob = cvx.Problem(objective, constraints)
    prob.solve()

    print('1')
    X_opt = X.value
    return X_opt


def MSE(X, Z, m, n, k, omega):
    mse = 0
    for i in range(m):
        for j in range(n):
            if (i, j) not in omega:
                mse += (X[i, j] - Z[i, j]) ** 2
    return mse / (m * n - k)

# Main function
m, n = 100, 100
r = 2
K = list(range(100, 3100, 100))
num = len(K)
# record mse for different k
mse_record = np.zeros(num)


Z = Generate_Z(m, n, r)

for idx in range(num):
    k = K[idx]
    omega = Generate_loc(m, n, k)
    X_opt = SDP_CompleteMat(Z, omega)
    X_star = X_opt[:m, m:]
    mse = MSE(X_star, Z, m, n, k, omega)
    mse_record[idx] = mse

# visualization
plt.plot(K, mse_record)
plt.xlabel('k value')
plt.ylabel('MSE')
plt.title('MSE over different k')

plt.show()