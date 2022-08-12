import numpy as np
import math
import Q2
import matplotlib.pyplot as plt

# generate n cities in [0,1]*[0,1]
n1=10
n2=50
n=50

x_city = np.random.rand(n)
y_city = np.random.rand(n)

x_city1 = np.random.rand(n1)
y_city1 = np.random.rand(n1)

x_city2 = np.random.rand(n2)
y_city2 = np.random.rand(n2)

#iter times
N_iter1=50000
N_iter11=14000
N_iter111=10000
N_iter2=200

#eta
eta1=0.99
eta2=0.9

distance=np.zeros((n, n))
distance1=np.zeros((n1,n1))
distance2=np.zeros((n2,n2))
for i in range(n):
    for j in range(n):
        distance[i,j] = math.sqrt((x_city[i]-x_city[j])**2+(y_city[i]-y_city[j])**2)

for l in range(n1):
    for m in range(n1):
        distance1[l,m] = math.sqrt((x_city1[l]-x_city1[m])**2+(y_city1[l]-y_city1[m])**2)

for i in range(n2):
    for j in range(n2):
        distance2[i,j] = math.sqrt((x_city2[i]-x_city2[j])**2+(y_city2[i]-y_city2[j])**2)


t01=Q2.initial_temp(N=n,distance=distance,eta=eta1)
t02=Q2.initial_temp(N=n,distance=distance,eta=eta2)

sol1, all_distance1, all_len1, len1 = Q2.SA(N=n,distance=distance, eta=eta1, N_iteration=N_iter1, T=t01, Method=4)
sol11, all_distance11 = Q2.SA_modify(N=n,distance=distance, eta=eta2, N_iteration=N_iter2, T=t01)
#sol111, all_distance11, all_len111, len111 = Q2.SA(N=n,distance=distance, eta=eta1, N_iteration=N_iter111, T=t01, Method=4)
#t1=500
#t2=1000
#t3=5000
#sol1, all_distance1, all_len1, len1 = Q2.SA(N=n,distance=distance, eta=eta1, N_iteration=N_iter11, T=t1, Method=1)
#sol11, all_distance11, all_len11, len11 = Q2.SA(N=n,distance=distance, eta=eta1, N_iteration=N_iter11, T=t2, Method=1)
#sol111, all_distance111, all_len111, len111 = Q2.SA(N=n,distance=distance, eta=eta1, N_iteration=N_iter11, T=t3, Method=1)
#sol2, all_distance2= Q2.SA_modify(N=n,distance=distance,eta=eta2,N_iteration=N_iter2, T=t02)

'''
count=0
method_basic=[]
method_combined=[]
x_axis=list(range(1,101))
for _ in range(100):
    x_city = np.random.rand(n)
    y_city = np.random.rand(n)
    for i in range(n):
        for j in range(n):
            distance[i, j] = math.sqrt((x_city[i] - x_city[j]) ** 2 + (y_city[i] - y_city[j]) ** 2)
    sol1, all_distance1, all_len1, len1 = Q2.SA(N=n, distance=distance, eta=eta1, N_iteration=N_iter11, T=t01, Method=1)
    sol11, all_distance11, all_len11, len11 = Q2.SA(N=n, distance=distance, eta=eta1, N_iteration=N_iter11, T=t01,Method=4)
    method_combined.append(len11)
    method_basic.append(len1)
    if(len11<=len1):
        count+=1
print(count)


plt.figure(1)
plt.plot(x_axis, method_basic, color='g', label='basic method shortest distance')
plt.plot(x_axis, method_combined, color='b', label='combined method shortest distance')
plt.title('Comparison between two proposal rules')
plt.legend()
'''
#print(sol1)
#print(distance)

## check iteration\temperature

plt.figure(1)
plt.subplot(221)
Q2.plot_scatter(x_city=x_city, y_city=y_city)
Q2.plot_route(N=n, x_city=x_city, y_city=y_city, sol=sol1)
plt.title('Primal SA')
plt.xlim(0,1)
plt.ylim(0,1)

plt.subplot(222)
Q2.plot_scatter(x_city=x_city, y_city=y_city)
Q2.plot_route(N=n, x_city=x_city, y_city=y_city, sol=sol11)
plt.title('Modified SA')
plt.xlim(0,1)
plt.ylim(0,1)

'''
plt.subplot(133)
Q2.plot_scatter(x_city=x_city, y_city=y_city)
Q2.plot_route(N=n, x_city=x_city, y_city=y_city, sol=sol111)
plt.title('N=100')
plt.xlim(0,1)
plt.ylim(0,1)
'''
#check iteration\temperature

#plt.figure(2)
#Q2.plot_iter(iter=N_iter1, all_dist=all_distance1)
plt.figure(1)
plt.subplot(223)
Q2.plot_iter(iter=N_iter1, all_dist=all_len1)
plt.title('Primal SA')
plt.subplot(224)
Q2.plot_iter(iter=N_iter2, all_dist=all_distance11)
plt.title('Modified SA')
#plt.subplot(233)
#Q2.plot_iter(iter=N_iter11, all_dist=all_len111)
#plt.title('T=2000')

#check initial temperature


'''

plt.figure(4)
Q2.plot_scatter(x_city=x_city, y_city=y_city)
Q2.plot_route(N=n, x_city=x_city, y_city=y_city, sol=sol2)
plt.xlim(0,1)
plt.ylim(0,1)

plt.figure(5)
Q2.plot_iter(iter=N_iter2, all_dist=all_distance2)

'''
#plt.figure(6)
#Q2.plot_scatter(x_city=x_city, y_city=y_city)
#plt.title('The diagram of generated cities')




plt.show()
