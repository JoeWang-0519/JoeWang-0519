% visualization for task 2
clear all;
clc;
discount_cand = [0.5, 0.6, 0.7, 0.8, 0.9, 0.95];
len = length(discount_cand);
hold on;
for number = 1 : len
    dis = discount_cand(number);
    filename = ['result_', 'dis', num2str(dis), '_learn2.mat'];
    load(filename);
    scatter(number, aver_execu_time, 'filled');
end
xticks(1:len);
xticklabels({'0.5', '0.6', '0.7', '0.8', '0.9', '0.95'});
xlabel('discount rate');
ylabel('average execution time')
grid on;
title('Average execution time for different choices of discount rate')
