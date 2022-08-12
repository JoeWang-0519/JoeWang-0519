clear all;
clc;
X = randn(800,2);
s2 = sum(X.^2,2);
trainX = (X.*repmat(1*(gammainc(s2/2,1).^(1/2))./sqrt(s2),1,2))'; % 2x800 matrix


% parameter setting
iteration_num = 500;
neur_num_1 = 8;
neur_num_2 = 8;
X_train = trainX;

[weight, record_weight] = SOM(X_train, neur_num_1, neur_num_2, iteration_num);

subplot(1,2,1)
hold on;
weight1 = reshape(weight, 2, 8, 8);
for hori = 1 : neur_num_1
    x = reshape(weight1(1, hori, :), 1, neur_num_2);
    y = reshape(weight1(2, hori, :), 1, neur_num_2);
    plot(x,y, 'k');
end
for vert = 1 : neur_num_2
    x = reshape(weight1(1, :, vert), neur_num_1, 1);
    y = reshape(weight1(2, :, vert), neur_num_1, 1);
    plot(x,y, 'b');
end
plot(trainX(1,:),trainX(2,:),'+r');
title('total iteration = 500')

iteration_num = 40000; % 500 epochs
[weight, record_weight] = SOM(X_train, neur_num_1, neur_num_2, iteration_num);
subplot(1,2,2)
hold on;
weight1 = reshape(weight, 2, 8, 8);
for hori = 1 : neur_num_1
    x = reshape(weight1(1, hori, :), 1, neur_num_2);
    y = reshape(weight1(2, hori, :), 1, neur_num_2);
    plot(x,y, 'k');
end
for vert = 1 : neur_num_2
    x = reshape(weight1(1, :, vert), neur_num_1, 1);
    y = reshape(weight1(2, :, vert), neur_num_1, 1);
    plot(x,y, 'b');
end
plot(trainX(1,:),trainX(2,:),'+r');
title('total iteration = 40000 (500 epochs)')


% visualization dynamically
%
%
% for graph = 1:20:iteration_num
%     weight1 = reshape(record_weight(graph, :, :), 2, 8, 8);
%     hold off;
%     for hori = 1 : neur_num_1
%         x = reshape(weight1(1, hori, :), 1, neur_num_2);
%         y = reshape(weight1(2, hori, :), 1, neur_num_2);
%         plot(x,y, 'k');
%         hold on;
%     end
%     for vert = 1 : neur_num_2
%         x = reshape(weight1(1, :, vert), neur_num_1, 1);
%         y = reshape(weight1(2, :, vert), neur_num_1, 1);
%         plot(x,y, 'b');
%     end
%     plot(trainX(1,:),trainX(2,:),'+r');
%     pause(0.3)
%     
% end
%     
% 
