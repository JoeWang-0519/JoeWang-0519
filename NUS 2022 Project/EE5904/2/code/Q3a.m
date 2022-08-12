clear all;
clc;

% datasample_256.mat is the data that in [0, 255]
%load datasample_256.mat

% datasample.mat is the data that in [0, 1]
load datasample.mat

% split the training and validation set
train_image = image_all(:, [1:450, 501:950]);
val_image = image_all(:, [451:500, 951:1000]);

train_target = target_all([1:450, 501:950]);
val_target = target_all([451:500, 951:1000]);

% a) perceptron
net = perceptron('hardlim', 'learnp');
net.divideFcn = 'dividetrain';
net = configure(net, train_image, train_target);

image_c = num2cell(train_image, 1);
target_c = num2cell(train_target, 1);

train_num = length(train_target);
epochs = 100;

% Accuracy
accu_train = zeros(epochs, 1);
accu_val = zeros(epochs, 1);


% Another performance measure
% dog - positive class
% manmade objects - negative calss

recall_train = zeros(epochs, 1);
recall_val = zeros(epochs, 1);

precision_train = zeros(epochs, 1);
precision_val = zeros(epochs, 1);


for i = 1 : epochs
    display(['Epoch: ', num2str(i)]);
    idx = randperm(train_num);
    net = adapt(net, image_c(: , idx), target_c(: , idx));

    pred_train = round(net(train_image));
    pred_val = round(net(val_image));

    % record the performance
    [recall_train(i), precision_train(i), accu_train(i)] = perf_meas(pred_train, train_target);
    [recall_val(i), precision_val(i), accu_val(i)] = perf_meas(pred_val, val_target);
end


figure(1)
subplot(1,3,1)
plot(1:epochs, accu_train, 'b');
hold on;
plot(1:epochs, accu_val, 'r');
legend('accuracy of training set', 'accuracy of validation set');
xlabel('epochs');
ylabel('accuracy');
title('Accuracy');
grid on;

subplot(1,3,2)
plot(1:epochs, recall_train, 'b');
hold on;
plot(1:epochs, recall_val, 'r');
legend('recall of training set', 'recall of validation set');
xlabel('epochs');
ylabel('recall');
title('Recall');
grid on;

subplot(1,3,3)
plot(1:epochs, precision_train, 'b');
hold on;
plot(1:epochs, precision_val, 'r');
legend('precision of training set', 'precision of validation set');
xlabel('epochs');
ylabel('precision');
title('Precision');
grid on;







