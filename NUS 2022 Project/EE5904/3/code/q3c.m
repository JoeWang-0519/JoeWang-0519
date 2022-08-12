clear all;
clc;
load Digits_modify.mat
% We only focus on:
% Test_ClassLabel, Test_Data
% Train_ClassLabel, Train_Data

X_train = Train_Data;
neur_num_1 = 10;
neur_num_2 = 10;
iteration_num = 10000;

[weight, record_weight] = SOM(X_train, neur_num_1, neur_num_2, iteration_num);

% Determine the contextual map
% Determine the winning input for each neuron
[dim, num] = size(X_train);
winner_neuron = zeros(dim, neur_num_1, neur_num_2);
output_neuron = zeros(neur_num_1, neur_num_2);
for i = 1 : neur_num_1
    for j = 1 : neur_num_2
        distance = zeros(1, num);
        for train_idx = 1 : num
            distance(train_idx) = norm(X_train(:, train_idx) - weight(:, i, j));
        end
        [~, winner_idx] = min(distance);
        winner_neuron(:, i, j) = X_train(:, winner_idx);
        output_neuron(i,j) = Train_ClassLabel(winner_idx);
    end
end

figure(1)
for i = 1 : neur_num_1
    for j = 1 : neur_num_2
        subplot(neur_num_1, neur_num_2, (i-1) * neur_num_2 + j);
        img = reshape(winner_neuron(:,i,j), 28, 28);
        imshow(img)
        title(num2str(output_neuron(i,j)))
    end
end

% testing set
[~, test_num] = size(Test_Data);
sum = 0;
correct_record = - ones(1, test_num);

for i = 1 : test_num
    distance = zeros(neur_num_1, neur_num_2);
    x_test = Test_Data(:, i);
    for l = 1 : neur_num_1
        for m = 1 : neur_num_2
            neuron = weight(:, l,  m);
            distance(l, m) = norm(x_test - neuron);
        end
    end
    [~, pre_idx] = min(distance, [], 'all');
    pre_idx_1 = mod(pre_idx, neur_num_1);
    pre_idx_2 = floor((pre_idx - 1) / neur_num_1 ) + 1;
    if pre_idx_1 == 0
        pre_idx_1 = neur_num_1;
    end
    predict = output_neuron(pre_idx_1, pre_idx_2);
    if predict == Test_ClassLabel(i)
        sum = sum + 1;
        correct_record(i) = predict;
    end
end

