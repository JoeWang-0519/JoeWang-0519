clear all;
clc;

%Function Approximation
%Here we use Batch mode with trainbr algorithm

x_train = [-1.6: 0.05: 1.6];
x_test = [-1.6: 0.01: 1.6];
y_train = 1.2 * sin(pi * x_train) - cos(2.4 * pi * x_train);
y_test = 1.2 * sin(pi * x_test) - cos(2.4 * pi * x_test);
temp = [-3, 3];
truey_out = .2 * sin(pi * temp) - cos(2.4 * pi * temp);
% number of hidden neuron
n = [1:10, 20, 50, 100];
epochs = 100;



test_error = zeros(1,13);
train_error = zeros(1,13);
y_out = zeros(2,13);
% record the epoch number for different neurons
epoch_record=zeros(1,13);
for i = 1:13
    net = fitnet(n(i));
    net.trainFcn = 'trainbr';
    net.trainParam.epochs = epochs;
    net.divideFcn = 'dividetrain'; 
    net.performParam.regularization = 0;
    % now we set regularization = 0 so that we can compare the difference
    % between different algorithms and learning modes
    %
    % Later we will check the power of regularization
    %
    % Since we just want to learn the model, and we want use other samples 
    % to check its performance
    % If we use other methods, then we may attain early stop and achieve the
    % performance by the inner method
    [net, tr] = train(net, x_train, y_train);
    epoch_record(i) = tr.epoch(end);
    
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
plot(1:13, train_error, '--r*');
hold on;
plot(1:13, test_error, '-bd');
title('Testing error and Training error');
xlabel('number of hidden neurons');
ylabel('MSE (performance)')
legend('training error', 'testing error');
set(gca,'xtick',1:13);
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
