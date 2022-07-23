import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy

def LLS(X, D):
    w=np.dot(np.dot(np.linalg.inv(np.dot(X.transpose(), X)), X.transpose()), D)
    return w

def LMS_iter(X, D, eta=0.01, max_iteration=100, initial_theta=None):
    # record the number of iteration
    count = 0
    # record all the weights during the update process
    all_theta=[]
    # initialization

    theta = np.random.random(2)
    if initial_theta is not None:
        theta = initial_theta
    print("initial weight is:", theta)

    theta_new = copy.copy(theta)
    all_theta.append(theta_new)
    while (count < max_iteration):
        for x,d in zip(X, D):
            if (count < max_iteration):
                error_signal = d - np.dot(theta, x)
                theta += eta * error_signal * x
                # update the number of iteration
                count += 1
                # record the new theta
                theta_new = copy.copy(theta)
                all_theta.append(theta_new)
            else:
                break
    return theta, all_theta, count

def LMS_epoch(X, D, eta=0.01, max_epoch=100, initial_theta=None):
    # record the number of epochs
    epoch = 0
    # record all the weights during the update process
    all_theta=[]
    # initialization

    theta = np.random.random(2)
    if initial_theta is not None:
        theta = initial_theta
    print("initial weight is:", theta)

    theta_new = copy.copy(theta)
    all_theta.append(theta_new)
    while (epoch < max_epoch):
        for x,d in zip(X, D):
            error_signal = d - np.dot(theta, x)
            theta += eta * error_signal * x
            # record the new theta
            theta_new = copy.copy(theta)
            all_theta.append(theta_new)
        epoch+=1
    return theta, all_theta, epoch

def plot_sample(X,D):
    # color setting
    colors1 = '#00CED1'
    # size of point setting
    area = np.pi * 4 ** 2

    plt.scatter(X[:,1], D, s=area, c=colors1, alpha=0.4)

def plot_curve(theta, color='red', alpha=1, label='LMS'):
    x1=[0, 5]
    x2=[theta[0], theta[0]+5*theta[1]]
    plt.plot(x1, x2, c=color, alpha=alpha, label=label)

X=np.array([[1,0],[1,0.8],[1,1.6],[1,3],[1,4],[1,5]])
D=np.array([0.5,1,4,5,6,8])
# LLS Method
theta_LLS=LLS(X, D)
# LMS method
theta_LMS, all_theta, epoch=LMS_epoch(X, D, eta=0.01, max_epoch=100, initial_theta=np.array([0.2240071, 0.56472398]))
# LLS fitting curve
#plt.figure(1)
#plot_sample(X,D)
#plot_curve(theta_LLS)
#plt.show()
# LMS fitting curve

plt.figure(2)
plot_sample(X,D)
for w in all_theta:
    plot_curve(w, color='green', alpha=0.1)
plot_curve(theta_LMS)
plt.show()
print(theta_LLS)
print(theta_LMS, epoch)
'''
plt.figure(3)
plot_curve(theta_LMS, color='red', label='LMS')
plot_curve(theta_LLS, color='green', label='LLS')
plt.legend()
'''
#plt.show()
