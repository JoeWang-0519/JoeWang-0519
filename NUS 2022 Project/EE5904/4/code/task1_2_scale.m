clear all;
clc;
load train.mat
load test.mat

% Pre-processing: Standardize
% Scale
%
for i = 1 : 2000
    train_data_scale(:,i) = train_data(:,i) / norm(train_data(:,i));
end
for i = 1 : 1536
    test_data_scale(:,i) = test_data(:,i) / norm(test_data(:,i));
end

% 
% threshold1 = 1e-4;
% threshold2 = 1e-4;
% C = 50;    %500
% Method = inf;
% gamma = 50;
% [bias, alpha, flag, K] = SVM_soft(train_data_scale, train_label, C, Method, gamma, threshold1, threshold2);
% 
% predict_test = prediction(alpha, bias, Method, train_data_scale, train_label, test_data_scale, gamma);
% predict_train = prediction(alpha, bias, Method, train_data_scale, train_label, train_data_scale, gamma);
% acc_test = accuracy(test_label, predict_test);
% acc_train = accuracy(train_label, predict_train);
    


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
C_candidate = [0.1, 0.6, 1.1, 2.1, 1e5];
gamma = 1;
threshold1 = 1e-4;
threshold2 = 1e-4;

for Method = P
    C = C_candidate(5);
    [bias, alpha, flag, K] = SVM_soft(train_data_scale, train_label, C, Method, gamma, threshold1, threshold2);
    
    flag_kernel(Method) = flag;
    
    predict_test = prediction(alpha, bias, Method, train_data_scale, train_label, test_data_scale, gamma);
    predict_train = prediction(alpha, bias, Method, train_data_scale, train_label, train_data_scale, gamma);
    acc_test = accuracy(test_label, predict_test);
    acc_train = accuracy(train_label, predict_train);
    
    test_accuracy_hard(Method) = acc_test;
    train_accuracy_hard(Method) = acc_train;
end

for Method = P
    for C_idx = 1:4
        C = C_candidate(C_idx);
     
        [bias, alpha, flag, K] = SVM_soft(train_data_scale, train_label, C, Method, gamma, threshold1, threshold2);
        
        predict_test = prediction(alpha, bias, Method, train_data_scale, train_label, test_data_scale, gamma);
        predict_train = prediction(alpha, bias, Method, train_data_scale, train_label, train_data_scale, gamma);
        acc_test = accuracy(test_label, predict_test);
        acc_train = accuracy(train_label, predict_train);
        
        test_accuracy_soft(C_idx, Method) = acc_test;
        train_accuracy_soft(C_idx, Method) = acc_train;
    end
end

    
            
