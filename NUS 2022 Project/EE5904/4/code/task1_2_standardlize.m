clear all;
clc;
load train.mat
load test.mat

% Pre-processing: Standardize
% apply Standardization to each feature (each row)
[dim, ~] = size(train_data);
mu1 = mean(train_data, 2);
s1 = std(train_data, 0, 2);
for i = 1 : dim
    train_data_stand(i,:) = (train_data(i,:) - mu1(i)) / s1(i);
    test_data_stand(i,:) = (test_data(i,:) - mu1(i)) / s1(i);
end

% the logic here: Since we will try polynomial kernel, i.e., 4-oreder,
% 5-oreder kernel, then it Kernel Matrix, (1 + <xi, xj>)^p will be very big
% because the dataset is not sparse. Therefore, in order to make our Kernel
% Matrix not to be ill-conditioning, we should shrink our dataset for some
% scale. Here, we shrink each sample for scale 10.

% if we pre-process the dataset with norm=1, then our dataset is still
% sparse. Therefore, we do not need to shrink by some scale.

train_data_stand = train_data_stand./10;
test_data_stand = test_data_stand./10;

% 
% threshold1 = 1e-4;
% threshold2 = 1e-4;
% C = 100;
% Method = inf;
% gamma = 0.4;
% [bias, alpha, flag, K] = SVM_soft(train_data_stand, train_label, C, Method, gamma, threshold1, threshold2);
% 
% predict_test = prediction(alpha, bias, Method, train_data_stand, train_label, test_data_stand, gamma);
% predict_train = prediction(alpha, bias, Method, train_data_stand, train_label, train_data_stand, gamma);
% acc_test = accuracy(test_label, predict_test);
% acc_train = accuracy(train_label, predict_train);
%     
% For RBF Kernel, GOOD parameter (C=10000, gama=0.0003)


% %---------------------------------------------------------------------------
% Record of the table
test_accuracy_hard = zeros(1,5);    % j-th represents order j
train_accuracy_hard = zeros(1,5);
test_accuracy_soft = zeros(4,5);    % (i, j)-th represents i-th penalty, j-th order
train_accuracy_soft = zeros(4,5);

% Record of admissiblity of Kernel
flag_kernel = zeros(1,5);

% order of kernel
P = [1, 2, 3, 4, 5];
% penalty C
C_candidate = [0.1, 0.6, 1.1, 2.1, 1e4];
gamma = 1;
threshold1 = 1e-4;
threshold2 = 1e-4;

for Method = P
    C = C_candidate(5);
    [bias, alpha, flag, K] = SVM_soft(train_data_stand, train_label, C, Method, gamma, threshold1, threshold2);
    
    flag_kernel(Method) = flag;
    
    predict_test = prediction(alpha, bias, Method, train_data_stand, train_label, test_data_stand, gamma);
    predict_train = prediction(alpha, bias, Method, train_data_stand, train_label, train_data_stand, gamma);
    acc_test = accuracy(test_label, predict_test);
    acc_train = accuracy(train_label, predict_train);
    
    test_accuracy_hard(Method) = acc_test;
    train_accuracy_hard(Method) = acc_train;
end

for Method = P
    for C_idx = 1:4
        C = C_candidate(C_idx);
     
        [bias, alpha, flag, K] = SVM_soft(train_data_stand, train_label, C, Method, gamma, threshold1, threshold2);
        
        predict_test = prediction(alpha, bias, Method, train_data_stand, train_label, test_data_stand, gamma);
        predict_train = prediction(alpha, bias, Method, train_data_stand, train_label, train_data_stand, gamma);
        acc_test = accuracy(test_label, predict_test);
        acc_train = accuracy(train_label, predict_train);
        
        test_accuracy_soft(C_idx, Method) = acc_test;
        train_accuracy_soft(C_idx, Method) = acc_train;
    end
end

    
            



%---------------------------------------------------------------------------
% % For Task 3, Select the best RBF Kernel SVM
% % 
% % Record of admissiblity of Kernel
% 
% % order of kernel
% P = [inf];
% % penalty C
% C_candidate = [0.1, 1, 2, 4, 6, 8, 10, 20, 40, 60, 100, 200, 500, 1e4];
% gamma = 0.1;
% threshold1 = 1e-4;
% threshold2 = 1e-4;
% 
% % Record of the table
% test_accuracy_RBF = zeros(1,length(C_candidate));   
% train_accuracy_RBF = zeros(1,length(C_candidate));
% for Method = P
%     for C_idx = 1 : length(C_candidate)
%         C = C_candidate(C_idx);
%      
%         [bias, alpha, flag, K] = SVM_soft(train_data_stand, train_label, C, Method, gamma, threshold1, threshold2);
%         
%         predict_test = prediction(alpha, bias, Method, train_data_stand, train_label, test_data_stand, gamma);
%         predict_train = prediction(alpha, bias, Method, train_data_stand, train_label, train_data_stand, gamma);
%         acc_test = accuracy(test_label, predict_test);
%         acc_train = accuracy(train_label, predict_train);
%         
%         test_accuracy_RBF(1, C_idx) = acc_test;
%         train_accuracy_RBF(1, C_idx) = acc_train;
%     end
% end
% 
% % visualization
% x_axis = 1:length(C_candidate);
% figure(1)
% hold on;
% grid on;
% plot(x_axis, train_accuracy_RBF, '-*r');
% plot(x_axis, test_accuracy_RBF, '-*b');
% legend('training accuracy','test accuracy')
% set(gca,'XTick',x_axis);
% set(gca, 'XTickLabel', C_candidate)
% xlabel('C');
% ylabel('accuracy')
% title('gamma = 0.1')