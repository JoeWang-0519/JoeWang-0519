import math
import matplotlib.pyplot as plt

def exp_test(t, k, alpha = 0.5):
    # t: test data
    # k: number of bins
    # alhpa: the threshold

    num = len(t);
    estimator_lambda = num / sum(t);

    # construct the bins for equal probability
    beta = [0] * k;
    for i in range(k):
        beta[i] = - math.log(1 - i / k) / estimator_lambda

    O = [0] * k;
    for test_data in t:
        for i in range(k-1):
            if beta[i] <= test_data < beta[i+1]:
                O[i] += 1;
                break;

    O[k-1] = num - sum(O);
    chi_sq = sum([((i - num / k)**2) / (num / k) for i in O]);
    return chi_sq

t = [0.01, 0.07, 0.03, 0.08, 0.04,
0.10, 0.05, 0.10, 0.11, 0.17,
1.50, 0.93, 0.54, 0.19, 0.22,
0.36, 0.27, 0.46, 0.51, 0.11,
0.56, 0.72, 0.29, 0.04, 0.73];

# we choose k from [3, 4, 5, ..., 22];
K = list(range(3,23));
chi_sq_record = [0] * len(K);

count = 0;

for k in K:
    chi_sq = exp_test(t, k);
    chi_sq_record[count] = chi_sq;
    count += 1;

print(chi_sq_record);

# since we choose alpha = 0.5
# the threshold is X_{k-2}^2(0.5)
thresh_chi_sq = [0.455, 1.386, 2.366, 3.357, 4.351,
                 5.348, 6.346, 7.344, 8.343, 9.342,
                 10.341, 11.340, 12.340, 13.339, 14.339,
                 15.338, 16.338, 17.338, 18.338, 19.337];
plt.plot(K, chi_sq_record, '-*b');
plt.plot(K, thresh_chi_sq, '-or');
plt.legend(['chi_sq_(k)','chi_sq_{k-2}(0.5)'])
plt.xlabel('choice of k')
plt.xlim(2,23)
new_ticks = list(range(2,24));
plt.xticks(new_ticks)
plt.grid(linestyle=":", color="k")
plt.title('Comparison between Threshold and Chi_square')
plt.show();

