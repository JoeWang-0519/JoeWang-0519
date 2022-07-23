import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy

def perceptron_algo(X, D, dim, N_iters, initial_weights=None, eta=1):
    """ run the perceptron algorithm
    :param X: the input
    :param D: desired response
    :param dim: dimension
    :param N_iters: number of iterations to run
    :param initial_weights: the initial theta(if None, choose randonmly)
    :param eta: learning rate
    :return theta: the result w for y = step(wx)
    """
    # store all the update theta

    all_theta=[]
    # initialization
    theta = np.random.random(dim)

    if initial_weights is not None:
        theta = initial_weights
    print("initial weight is:", theta)
    theta_new=copy.copy(theta)
    all_theta.append(theta_new)


    # count the total number of updates
    count = 0
    # complete signal (control whether need to iterate more)
    complete_signal = 1

    for _ in range(N_iters):
        # if all the dataset makes no mistakes, terminate
        if (complete_signal == 0):
            break
        # reset signal
        complete_signal = 0

        for x, d in zip(X, D):
            induced_random_field = np.dot(theta, x)
            mistake = induced_random_field * (2*d - 1) <= 0

            if mistake:
                # calculate the actual response y
                if induced_random_field >= 0:
                    y=1
                else:
                    y=0

                # update when there is a mistake
                update = eta* (d-y) * np.array(x)
                theta += update
                theta_new= copy.copy(theta)
                all_theta.append(theta_new)
                # count the total number of updates
                count += 1
                complete_signal += 1

    print("all iteration time is: ", count)
    return theta, all_theta, count

def plot_sample3(X, D):
    # extract x
    X1=X[:,1]
    X2=X[:,2]
    # split the dataset into 2 class
    class0=[]
    class1=[]
    for i in range(len(D)):
        if D[i] == 0:
            class0.append(i)
        else:
            class1.append(i)

    # color setting
    colors1 = '#00CED1'
    colors2 = '#DC143C'

    # size of point setting
    area = np.pi * 4 ** 2

    plt.scatter(X1[class0], X2[class0], s=area, c=colors1, alpha=0.4, label='class_0')
    plt.scatter(X1[class1], X2[class1], s=area, c=colors2, alpha=0.4, label='class_1')


def decision_boundary3(theta, color='green', alpha=0.2):
    x1 = [-0.5, 2]
    x2 = [ -(theta[0] - .5*theta[1]) / theta[2], -(theta[0] + 2*theta[1]) / theta[2]]
    plt.plot(x1, x2, c=color, alpha=alpha)

def decision_boundary2(theta, color='green', alpha=0.2):
    plt.scatter(-theta[0]/theta[1], 0, c=color, alpha=alpha)


# main function
X=np.array([[1, 0, 0], [1, 1, 0], [1, 0, 1], [1, 1, 1]])
D=np.array([0,0,0,1])

# change the learning rate(.1, .2, .3, .5, 1, 3) and record
record_n1=[]
record_n2=[]
record_n3=[]
record_n4=[]
record_n5=[]
record_n6=[]
for i in range(100):
    theta, all_theta, n = perceptron_algo(X[:,[0,1]], D, eta=.1, dim=2, N_iters=100)
    record_n1.append(n)

for i in range(100):
    theta, all_theta, n = perceptron_algo(X[:,[0,1]], D, eta=.2, dim=2, N_iters=100)
    record_n2.append(n)

for i in range(100):
    theta, all_theta, n = perceptron_algo(X[:,[0,1]], D, eta=.3, dim=2, N_iters=100)
    record_n3.append(n)

for i in range(100):
    theta, all_theta, n = perceptron_algo(X[:,[0,1]], D, eta=1, dim=2, N_iters=100)
    record_n4.append(n)

for i in range(100):
    theta, all_theta, n = perceptron_algo(X[:,[0,1]], D, eta=3, dim=2, N_iters=100)
    record_n5.append(n)

for i in range(100):
    theta, all_theta, n = perceptron_algo(X[:,[0,1]], D, eta=10, dim=2, N_iters=100)
    record_n6.append(n)

# draw all the data sample
plot_sample3(X,D)
plt.legend()
theta, all_theta, n = perceptron_algo(X, D, eta=.2, dim=3, N_iters=100)
# draw all the decision bounday during the update process
for w in all_theta:
    decision_boundary3(w)

decision_boundary3(theta, color='yellow', alpha=1)
print(theta)

plt.xlim(-.5, 2)
plt.ylim(-.5, 2)
plt.figure(1)
plt.show()


print("learning rate=.1 : ", np.mean(record_n1))
print("learning rate=.2 : ", np.mean(record_n2))
print("learning rate=.3 : ", np.mean(record_n3))
print("learning rate=1 : ", np.mean(record_n4))
print("learning rate=3 : ", np.mean(record_n5))
print("learning rate=10 : ", np.mean(record_n6))
