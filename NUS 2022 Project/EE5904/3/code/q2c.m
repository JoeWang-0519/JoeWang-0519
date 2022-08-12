clear all;
clc;
load mnist_modify.mat

% "K-means" Method
%--------------------------------------------------
% Comment: if choose K=100, std should be around 13

% non-regularization
regularization = 0;
% appropriate width
method = 4.3;
K = 100;
%K = 100;

[weight_woreg, record_centroids, std] = RBFN_Kmeans(train_data, train_target, K, method, regularization);

TrPred_woreg = predict_wbias(train_data, weight_woreg, record_centroids, std);
TePred_woreg = predict_wbias(test_data, weight_woreg, record_centroids, std);


% Performance (without regularization)

TrAcc_woreg = zeros(1,1000);    % accuracy of training set
TeAcc_woreg = zeros(1,1000);    % accuracy of testing set
thr_woreg = zeros(1,1000);
TrN_woreg = length(train_target);   % training set size
TeN_woreg = length(test_target);    % testing set size
for i = 1:1000
    % t starts from the Minimizer of training prediction, ends at the
    % Maximizer of training prediction with equal step length 0.001
    t = (max(TrPred_woreg)-min(TrPred_woreg)) * (i-1)/1000 + min(TrPred_woreg);
    % the i-th threshold t
    thr_woreg(i) = t;
    TrAcc_woreg(i) = (sum(train_target(TrPred_woreg<t)==0) + sum(train_target(TrPred_woreg>=t)==1)) / TrN_woreg; 
    TeAcc_woreg(i) = (sum(test_target(TePred_woreg<t)==0) + sum(test_target(TePred_woreg>=t)==1)) / TeN_woreg;
end
figure(1);
plot(thr_woreg,TrAcc_woreg,'.- ',thr_woreg,TeAcc_woreg,'^-');
title(['width = ', num2str(std)])

% find the best threshold as for testing accuracy
[best_teacc, best_idx] = max(TeAcc_woreg);

disp(['Best threshold is: ', num2str(thr_woreg(best_idx))]);
disp(['Best testing accuracy is: ', num2str(best_teacc)]);
hold on;
plot(thr_woreg(best_idx), best_teacc, 'ko', LineWidth=10);
legend('train accuracy','test accuracy', 'Best Threshold');

% visualize the RBFN map
label0_pre_te = TePred_woreg(test_target==0);
label1_pre_te = TePred_woreg(test_target==1);
label0_pre_tr = TrPred_woreg(train_target==0);
label1_pre_tr = TrPred_woreg(train_target==1);

figure(2)
subplot(2,1,1);
scatter(label0_pre_te, zeros(1, length(label0_pre_te)), 'r');
hold on;
scatter(label1_pre_te, ones(1, length(label1_pre_te)), 'b');
title(['Testing set, std = ', num2str(std)]);
ones_ = ones(1, length(label1_pre_te));

num_cor_test = sum(ones_(label1_pre_te>=thr_woreg(best_idx)));
disp(['number of label 1 testing samples are predicted correctly :', num2str(num_cor_test)]);
plot([thr_woreg(best_idx), thr_woreg(best_idx)], [0,1], 'k');
legend('label 0 prediction', 'label 1 prediction','Best Threshold');

subplot(2,1,2);
scatter(label0_pre_tr, zeros(1, length(label0_pre_tr)), 'r');
hold on;
scatter(label1_pre_tr, ones(1, length(label1_pre_tr)), 'b');
title(['Training set, std = ', num2str(std)]);
ones_ = ones(1, length(label1_pre_tr));
num_cor_train = sum(ones_(label1_pre_tr>=thr_woreg(best_idx)));
plot([thr_woreg(best_idx), thr_woreg(best_idx)], [0,1], 'k');
legend('label 0 prediction', 'label 1 prediction','Best Threshold');
% 

label0_tr = train_data(:,train_target==0);
aver0 = sum(label0_tr, 2)/786;
tmp0 = reshape(aver0, 28, 28);

label1_tr = train_data(:,train_target==1);
aver1 = sum(label1_tr, 2)/214;
tmp1 = reshape(aver1, 28, 28);

center0 = record_centroids(:,1);
temp0 = reshape(center0,28,28);

center1 = record_centroids(:,2);
temp1 = reshape(center1,28,28);

figure(3)
subplot(2,2,1)
imshow(tmp0)
title('average label 0')
subplot(2,2,2)
imshow(tmp1)
title('average label 1')
subplot(2,2,3)
imshow(temp0)
title('center 1')
subplot(2,2,4)
imshow(temp1)
title('center 2')

figure(4);
for i = 1:K
    subplot(10,10,i)
    center = record_centroids(:,i);
    tmp=reshape(center,28,28);
    imshow(tmp);
end

