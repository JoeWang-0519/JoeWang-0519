% we choose the model that:
% 1. standardize each feature with mean 0 and variance 0.01
% 2. choose parameter as :
%       C = 2.1
%       p = 2

% load training set to train our SVM
load train.mat

%----------------------------------------------------------------
% Step 1: Pre-processing
[dim, ~] = size(train_data);

mu1 = mean(train_data, 2);
s1 = std(train_data, 0, 2);
for i = 1 : dim
    train_data_stand(i,:) = (train_data(i,:) - mu1(i)) / s1(i);
end

train_data_stand = train_data_stand./10;

%----------------------------------------------------------------
% Step 2: Train SVM
threshold1 = 1e-4;
threshold2 = 1e-4;
C = 2.1;
Method = 2;
gamma = 2;

[bias, alpha, flag, K] = SVM_soft(train_data_stand, train_label, C, Method, gamma, threshold1, threshold2);

save trained_SVM.mat

%----------------------------------------------------------------
% In this .mat file, we still restore mu1 and std1 for
% standardization process


