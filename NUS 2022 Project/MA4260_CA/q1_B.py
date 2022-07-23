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

# total weeks
week = 1000000;
# threshold inventory quantity
Q = [i+1 for i in range(100)];
# parameter
p = 20;
c = 1;
h = 0.1;
# record for average cost
record_aver = [0] * len(Q);

count = 0;

for q in Q:
    aver_T = TCPW(q, p, c, h, week);
    record_aver[count] = aver_T;
    count += 1;

idx_opt = record_aver.index(min(record_aver));
quantity_opt = Q[idx_opt];
print('the optimal quantity is: ', quantity_opt);
print('the minimum average cost (per week) is: ', min(record_aver));

fig = plt.figure();
ax = fig.add_subplot(1,1,1);
ax.plot(Q, record_aver);
plt.title('Total Cost Per Week of each estimator q');
plt.xlabel('quantity');
plt.ylabel('Total Cost Per Week')
plt.show()

