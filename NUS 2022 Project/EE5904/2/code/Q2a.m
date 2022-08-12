clear all;
clc;

%Function Approximation


x_train = [-1.6: 0.05: 1.6];
x_test = [-1.6: 0.01: 1.6];
y_train = 1.2 * sin(pi * x_train) - cos(2.4 * pi * x_train);
y_test = 1.2 * sin(pi * x_test) - cos(2.4 * pi * x_test);
temp = [-3, 3];
truey_out = 1.2 * sin(pi * temp) - cos(2.4 * pi * temp);
% number of hidden neuron
n = [20, 30, 40];
%n = [50, 100];
epochs = 500;

%since we need to make full use of the whole interval
train_num = length(x_train);
val_num = 0;

%training
%a) sequential training
%
%Here, we do not add regularization, in order to show the REAL behaviour
%for different number of hidden neurons
%
%the optimzation method is GRADIENT DESCENT(BP)
%
%perform function is MSE
num = length(n);
test_error = zeros(1,num);
train_error = zeros(1,num);
y_out = zeros(2,num);
for i = 1:num
    [net, accu_train1, accu_val1] = train_fitseq(n(i), x_train, y_train, train_num, val_num, epochs);
    Y_train(i,:) = net(x_train);
    Y_test(i,:) = net(x_test);
    y_out(1,i) = net(-3);
    y_out(2,i) = net(3);
    train_error(i) = perform(net, y_train, Y_train(i,:));
    test_error(i) = perform(net, y_test, Y_test(i,:));
end

% plot test samples
figure(1)
for i = 1:6
    subplot(2,3,i);
    plot(x_test, Y_test(i,:),'r');
    hold on;
    plot(x_test, y_test, '--b');
    subtitle(['hidden neuron: ', num2str(n(i))]);
end
legend('output (prediction)', 'target')

figure(2)
for i = 1:7
    subplot(2,4,i);
    plot(x_test, Y_test(i+6,:),'r');
    hold on;
    plot(x_test, y_test, '--b');
    subtitle(['hidden neuron: ', num2str(n(i+6))])   
end
legend('output (prediction)', 'target')

figure(3)
plot(1:num, train_error, '--r*');
hold on;
plot(1:num, test_error, '-bd');
title('Testing error and Training error');
xlabel('number of hidden neurons');
ylabel('MSE (performance)')
legend('training error', 'testing error');
set(gca,'xtick',1:num);
set(gca,'xticklabel',n);

figure(4)
%-3
scatter(1:13, truey_out(1) * ones(1,13), [], 'red', 'filled', 'o');
hold on;
scatter(1:13, y_out(1,:), [], 'magenta', 'filled', 'o');
hold on;
%3
scatter(1:13, truey_out(2) * ones(1,13), [], 'filled', "blue", 'd');
hold on;
scatter(1:13, y_out(2,:), [], "black", 'filled', 'd');
grid on;
axis([1 13 -4 4]);
legend('true value of x=-3', 'prediction of x=-3', 'true value of x=3', 'prediction of x=3')
set(gca,'xtick',1:13);
set(gca,'xticklabel',n);
xlabel('number of hidden neurons');
ylabel('function value')
