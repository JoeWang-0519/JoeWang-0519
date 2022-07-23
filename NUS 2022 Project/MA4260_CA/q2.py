import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
# Passenger and Bus Model

# PASSENGER
scale1 = 1; # the reciprocal of lambda
num1 = 100000;
x_passenger = np.random.exponential(scale1, num1);
y_passenger = [0] * num1;
y_passenger[0] = x_passenger[0];
for idx in range(1, num1):
    y_passenger[idx] = x_passenger[idx] + y_passenger[idx-1];

# BUS
scale2 = 15;
num2 = 10000;
x_bus = np.random.exponential(scale2, num2);
y_bus = [0] * num2;
y_bus[0] = x_bus[0];
for idx in range(1, num2):
    y_bus[idx] = x_bus[idx] + y_bus[idx-1];

# T_waiting: Waiting time for k-th Passenger (k=1,2,...,100000)
# NumOfPeople_bus: Number of people for i-th Bus (i=1,2,...,10000)
T_waiting = [0] * num1;
NumOfPeople_bus = [0] * num2;

start_time = 0;
start_passenger = 0;

for bus_idx in range(num2):
    # we want to calculate the number of passengers in the interval ( start_time, end_time ];
    end_time = y_bus[bus_idx];
    count = 0;
    for i in range(start_passenger, num1):
        if y_passenger[i] > end_time:
            break;
        elif start_time < y_passenger[i] <= end_time:
            count += 1;

    T_waiting[start_passenger : i] = [end_time - passenger_time for passenger_time in y_passenger[start_passenger : i]];
    NumOfPeople_bus[bus_idx] = count;

    start_passenger = i;
    start_time = end_time;

# Since In those buses, it may happen that starting from one car, all cars afterwards do not have any passengers.
# Therefore, we should kick out those cars to attain the TRUE distribution for number of passengers in one bus

for idx in range(num2):
    if sum(NumOfPeople_bus[:idx])==100000:
        idx_0 = idx;
        break;

NumOfPeople_bus_wonull = NumOfPeople_bus[:idx_0];
mean_bus = np.mean(NumOfPeople_bus_wonull);
mean_T = np.mean(T_waiting);

var_bus = np.var(NumOfPeople_bus_wonull);
var_T = np.var(T_waiting);

plt.figure(1)
plt.subplot(1,2,1);
sns.kdeplot(T_waiting)
plt.plot([mean_T, mean_T], [0, 0.06], linewidth=3);
plt.xlabel('waiting time')
plt.ylabel('probability')
plt.title('kernel density estimation')


plt.subplot(1,2,2)
plt.hist(T_waiting, bins=30, density=True)
plt.xlabel('waiting time')
plt.ylabel('probability')
plt.title('histogram of waiting time for a random passenger')
plt.plot([mean_T, mean_T], [0, 0.06], linewidth=3);
plt.legend(['mean waiting time'])

plt.figure(2)
plt.subplot(1,2,1);
sns.kdeplot(NumOfPeople_bus_wonull)
plt.xlabel('number of passengers')
plt.ylabel('probability')
plt.title('kernel density estimation')
plt.plot([mean_bus, mean_bus], [0, 0.06], linewidth=3);

plt.subplot(1,2,2)
plt.hist(NumOfPeople_bus_wonull, bins=30, density=True)
plt.xlabel('number of passengers')
plt.ylabel('probability')
plt.title('histogram of number of passengers in one bus')
plt.plot([mean_bus, mean_bus], [0, 0.06], linewidth=3);
plt.legend(['mean passengers'])
plt.show()


plt.show()



