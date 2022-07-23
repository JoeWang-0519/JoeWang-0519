import random
import matplotlib.pyplot as plt
import numpy as np

def TCPW(q, p, c, h, week):
    # initialization
    x_inv = q;  # inventory level
    x_dis = 0;  # remaining failure days
    T = 0;  # total cost
    PURCHASEPERMITTED = True;

    # update process
    for iter in range(week):
        if x_dis > 0:
            x_dis -= 1;
            PURCHASEPERMITTED = False;
        else:
            PURCHASEPERMITTED = True;

        if x_inv > 0:
            x_inv -= 1;
        else:
            T += p;

        if PURCHASEPERMITTED == True:
            u = random.uniform(0, 1);
            if u < 0.95:
                if x_inv <= q - 2:
                    x_inv += 2;
                    T += 2 * c;
                elif x_inv == q - 1:
                    x_inv += 1;
                    T += c;
            else:
                x_dis = 19;
        T += h * x_inv
    return T/week;

# factory produce equipment Model
# aim: determine the optimal inventory quantity threshold q

#-------------------------------------------------------------------------
#-------------------------------------------------------------------------

# total repeat times
repeat = 100;
# total weeks
week = 10000;
# threshold inventory quantity
Q = [i+1 for i in range(50)];
# parameter
p = 10;
c = 1;
h = 0.1;
# record for average cost
record_aver_each = np.zeros((repeat, len(Q)));


for rep in range(repeat):
    count = 0;
    for q in Q:
        aver_T = TCPW(q, p, c, h, week);
        record_aver_each[rep, count] = aver_T;
        count += 1;

# calculate mean, variance
record_mean = np.mean(record_aver_each, axis = 0); # calculate the mean for each column
record_variance = np.var(record_aver_each, axis = 0); # calculate the variance for each column

idx_opt = np.argmin(record_mean);
quantity_opt = Q[idx_opt];
tcpw_opt = np.min(record_mean)

print('the optimal quantity is: ', quantity_opt);
print('the minimum average cost (per week) is: ', tcpw_opt);

# visualization of record_mean
fig = plt.figure(1);
ax = fig.add_subplot(1,1,1);
ax.plot(Q, record_mean);
plt.title('Mean (Total Cost Per Week) of each estimator q');
plt.xlabel('quantity');
plt.ylabel('mean')
plt.show()

# visualization of record_variance
fig = plt.figure(2);
ax = fig.add_subplot(2,1,2);
ax.plot(Q, record_variance);
plt.title('Variance (Total Cost Per Week) of each estimator q');
plt.xlabel('quantity');
plt.ylabel('variance')
plt.show()


# visualization of all 100 repeats (10000 weeks each)
ax = fig.add_subplot(2,1,1);
for rep in range(repeat):
    ax.plot(Q, record_aver_each[rep,:], linewidth = .2);
ax.plot(Q, record_mean, linewidth = 3, color='b');
plt.title('Visualization of 100 repeats and its mean');
plt.ylabel('Total Cost Per Week')
plt.show()

# visualization of optimal choice of quantity q^{*}
optimal_record = record_aver_each[:, idx_opt];
plt.figure(4);
plt.title('Histogram for optimal quantity q=23');
plt.xlabel('Total Cost Per Week');
plt.ylabel('Number of experiments')
plt.hist(optimal_record, bins=20);

