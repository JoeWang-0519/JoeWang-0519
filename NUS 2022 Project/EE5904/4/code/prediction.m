function predict = prediction(alpha, bias, Method, X_train, d, X_test, gamma)
% Parameter: 
% alpha: the dual variable obtained by SVM      size: num_train * 1
% bias: the bias term
% X_train: feature vector;      size: dimension * num_train
% d: label vector:              size: num_train * 1
% X_test: feature vector;       size: dimension * num_test
% Method: form of Kernel;   candidate {1,2,3,4,5,inf}
%                           i: i-order polynomial Kernel
%                           inf: rbf Kernel
% gamma: the paramter for RBF Kernel
%
% Output:
% predict: the prediction result of X_test;     size: num_test * 1;

%----------------------------------------------------------------
% Step 1: calculate the Kernel Matrix with respect to train data and test
% data

[~, num_train] = size(X_train);
[~, num_test] = size(X_test);

% Construct the kernel matrix with respect to different Method
innerproduct_mat = X_test' * X_train;

if Method == 1
    K = innerproduct_mat;
end

for m = 2 : 5
    if Method == m
        K = (innerproduct_mat + 1).^m;
        break;
    end
end

if Method == inf
    tmp1 = sum(X_train.^2);
    tmp2 = sum(X_test.^2);
    X1 = repmat(tmp1, num_test, 1);
    X2 = repmat(tmp2', 1, num_train);
    K = exp(-gamma * (X1 + X2 - 2 * innerproduct_mat));
end

%----------------------------------------------------------------
% Step 2: calculate the prediction with matrix computation
Alpha_D = alpha .* d;

predict = K * Alpha_D + bias;


