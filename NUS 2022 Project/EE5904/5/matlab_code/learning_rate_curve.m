clear all;
clc;
% This file is to visualize the learning rate curve
k = 1;
while (1+5*log(k))/k >= 0.005
    learning_rate4(k) = (1+5*log(k))/k;
    k = k + 1;
end
k = 1;
while (1+log(k))/k >= 0.005
    learning_rate3(k) = (1+log(k))/k;
    k = k + 1;
end
k = 1;
while 100/(100+k) >= 0.005
    learning_rate2(k) = 100/(100+k);
    k = k + 1;
end
k = 1;
while 1/k >= 0.005
    learning_rate1(k) = 1/k;
    k = k + 1;
end
figure(1)
hold on;
plot(1:length(learning_rate1), learning_rate1, LineWidth = 1.5);
plot(1:length(learning_rate2), learning_rate2, LineWidth = 1.5);
plot(1:length(learning_rate3), learning_rate3, LineWidth = 1.5);
plot(1:length(learning_rate4), learning_rate4, LineWidth = 1.5);
legend('1/k','100/(100+k)','(1+log(k))/k','(1+5log(k))/k')
xlabel('number of steps')

save learning_rate.mat
