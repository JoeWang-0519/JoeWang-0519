% sequential mode of MLP training
clear all;
clc;

load datasample.mat

% since the activation function is logistic function, we set the target as follows:
% 0.2->0 (manmade objects)
% 0.8->1 (dog)

% target is the 0-1 target
target = target_all;
% target all is the 0.2-0.8 target
target_all = [0.2*ones(1,500), 0.8*ones(1,500)];


% split the training and validation set
train_image = image_all(:, [1:450, 501:950]);
val_image = image_all(:, [451:500, 951:1000]);

train_target = target_all([1:450, 501:950]);
val_target = target_all([451:500, 951:1000]);

t_target = target([1:450, 501:950]);
v_target = target([451:500, 951:1000]);

% we apply the normalization on the row vector
mu1 = mean(train_image, 2);
s1 = std(train_image, 0, 2);
for i = 1:1024
    train_image_norm1(i,:) = (train_image(i,:) - mu1(i)) / s1(i);
    val_image_norm1(i,:) = (val_image(i,:) - mu1(i)) / s1(i);
end


epochs = 60;
train_num = 700;

[net, accu_trainep, accu_valep, A_train, P_train, R_train, A_val, P_val, R_val] = train_prseq(100, train_image_norm1, val_image_norm1, train_target, t_target, v_target, train_num, epochs);
 

figure(1);
xaxis = 1:epochs;
plot(xaxis, A_val, '--^k');
hold on;
plot(xaxis, A_train, 'm')
subtitle('Accuracy');
%set(gca,'xtick', [1, 5:5:55]);
%set(gca,'xticklabel', [5, 25, 50, 75, 100, 150, 200, 250, 300, 350, 400, 800]);
xlabel('number of epochs');
ylabel('Accuracy');
legend('testing accuracy', 'training accuracy');
hold on;
plot([25,25], [0.6, 1], 'k', 'linewidth', 2);
grid on;