clear all;
clc;
x = linspace(-pi,pi,400);
trainX = [x; sinc(x)]; % 2x400 matrix


% parameter setting
iteration_num = 500;
neur_num_1 = 1;
neur_num_2 = 60;
X_train = trainX;

[weight, record_weight] = SOM(X_train, neur_num_1, neur_num_2, iteration_num);
% subplot(1,2,1)
% record = reshape(weight, 2, 60);
% plot(record(1, :), record(2, :),'--ob',LineWidth=1.5);
% hold on;
% plot(trainX(1,:),trainX(2,:),'+r'); % axis equal
% title('total iteration = 500')
% 
% iteration_num = 20000;
% [weight, record_weight] = SOM(X_train, neur_num_1, neur_num_2, iteration_num);
% subplot(1,2,2);
% record = reshape(weight, 2, 60);
% plot(record(1, :), record(2, :),'--ob',LineWidth=1.5);
% hold on;
% plot(trainX(1,:),trainX(2,:),'+r'); % axis equal
% title('total iteration = 20000 (500 epochs)')





%visualization dynamically

for graph = 1 : 20: 1000 
    record = reshape(record_weight(graph, :, :), 2, 60);

    plot(record(1, :), record(2, :),'--ob',LineWidth=1.5)
    hold on;
    plot(trainX(1,:),trainX(2,:),'+r'); % axis equal
    axis([-pi,pi,-pi,pi]);
    hold off;
    pause(0.3)
end


