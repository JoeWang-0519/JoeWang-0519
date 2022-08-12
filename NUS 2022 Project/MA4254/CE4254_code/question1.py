import Q1
import numpy.random
import numpy as np
import matplotlib.pyplot as plt
import math
import re

#Repeat times=100
iter = 100
n, m = 15, 20
#record the opt
opt_val_FLP = np.zeros(iter)
opt_val_AFL = np.zeros(iter)
opt_val_FLP_LR = np.zeros(iter)
opt_val_AFL_LR = np.zeros(iter)

for k in range(iter):
    # 1. generate the COEFFICIENT
    # step 1: generate N facility locations and M  customer locations uniformly
    fac_x = numpy.random.rand(n)
    fac_y = numpy.random.rand(n)

    cust_x = numpy.random.rand(m)
    cust_y = numpy.random.rand(m)

    # step 2: use the generated location to calculate distance d_{i,j}
    d = np.zeros((m, n))
    for i in range(m):
        for j in range(n):
            d[i,j] = math.sqrt((cust_x[i] - fac_x[j]) ** 2 + (cust_y[i] - fac_y[j]) ** 2)

    #adjust to the objective
    distance = d.flatten()

    # step 3: generate the cost c_{j} from uniformly distribution
    cost = numpy.random.rand(n)

    opt_val_FLP[k], variables = Q1.FLP_Solver(c=cost, dd=distance, M=m, N=n)
    opt_val_FLP_LR[k] = Q1.FLP_LR_Solver(c=cost, dd=distance, M=m, N=n)
    opt_val_AFL[k] = Q1.AFL_Solver(c=cost, dd=distance, M=m, N=n)
    opt_val_AFL_LR[k] = Q1.AFL_LR_Solver(c=cost, dd=distance, M=m, N=n)

    if k==-1:
        #visualize
        arr_index_cus=[]
        arr_index_fac=[]
        arr_customer_x=[]
        arr_facility_x=[]
        arr_customer_y=[]
        arr_facility_y=[]

        plt.figure(1)
        plt.subplot(121)
        colors1 = '#00CED1'
        colors2 = '#DC143C'
        plt.scatter(fac_x, fac_y, c=colors1, label='facility')
        plt.scatter(cust_x, cust_y, c=colors2, label='customer')
        plt.legend()
        plt.subplot(122)
        colors1 = '#00CED1'
        colors2 = '#DC143C'
        plt.scatter(fac_x, fac_y, c=colors1, label='facility')
        plt.scatter(cust_x, cust_y, c=colors2, label='customer')
        plt.legend()
        for v in variables:
            if v.varValue>0:
                matchObj = re.match(r'x.(\d{1,2}),_(\d{1,2})',v.name)
                if matchObj:
                    arr_index_cus.append(int(matchObj.group(1)))
                    arr_index_fac.append(int(matchObj.group(2)))
        for item in arr_index_cus:
            arr_customer_x.append(cust_x[item-1])
            arr_customer_y.append(cust_y[item-1])
        for item in arr_index_fac:
            arr_facility_x.append(fac_x[item-1])
            arr_facility_y.append(fac_y[item-1])
        for i in range(m):
            plt.arrow(arr_customer_x[i],arr_customer_y[i],arr_facility_x[i]-arr_customer_x[i],arr_facility_y[i]-arr_customer_y[i])



# calculate FLP-LR tightness
count_FLP = 0
for i in range(iter):
    if opt_val_FLP[i] == opt_val_FLP_LR[i]:
        count_FLP+=1

# calculate AFL-LR tightness
count_AFL = 0
for i in range(iter):
    if opt_val_AFL[i] == opt_val_AFL_LR[i]:
        count_AFL+=1

print("Among 100 generated data, the number that FLP-Val equal to FLP-LR-Val:", count_FLP)
print("Among 100 generated data, the number that AFL-Val equal to AFL-LR-Val:", count_AFL)

print(opt_val_FLP_LR)
'''
# visualize the generated data(only one time)
if i == 1:
    colors1 = '#00CED1'
    colors2 = '#DC143C'
    plt.scatter(fac_x, fac_y, c=colors1, label='facility')
    plt.scatter(cust_x, cust_y, c=colors2, label='customer')
    plt.legend()
'''
x_axis=list(range(1,iter+1))
plt.figure(2)
plt.subplot(121)
plt.plot(x_axis, opt_val_FLP, 'b', label='FLP')
plt.plot(x_axis, opt_val_FLP_LR, 'g', label='FLP-LR')
plt.title('FLP vs FLP-LR')
plt.legend()
plt.subplot(122)
plt.plot(x_axis, opt_val_AFL, 'b', label='AFL')
plt.plot(x_axis, opt_val_AFL_LR, 'g', label='AFL-LR')
plt.title('AFL vs AFL-LR')
plt.legend()
plt.show()