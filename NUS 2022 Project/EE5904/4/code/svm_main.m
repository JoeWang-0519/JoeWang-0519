% we choose the model that:
% 1. standardize each feature with mean 0 and variance 0.01
% 2. choose parameter as :
%       C = 2.1
%       p = 2

%----------------------------------------------------------------
% eval_data 57 * 600
% eval_label 600 * 1

load trained_SVM.mat
%----------------------------------------------------------------
% Pre-processing of eval_data
[dim_eval, num_eval] = size(eval_data);

for i = 1 : dim_eval
    eval_data_stand(i,:) = (eval_data(i,:) - mu1(i)) / s1(i);
end
eval_data_stand = eval_data_stand./10;

%----------------------------------------------------------------
% Prediction on Evaluation
eval_predicted_discriminant = prediction(alpha, bias, Method, train_data_stand, train_label, eval_data_stand, gamma);

eval_predicted = zeros(num_eval, 1);
for i = 1 : num_eval
    if eval_predicted_discriminant(i) > 0
        eval_predicted(i) = 1;
    else
        eval_predicted(i) = -1;
    end
end






