clear all;
clc;
load mnist_modify.mat

% "Fixed Centers Selected at Random" Method
%----------------------------------------------------------------
% Firstly, choose appropriate width (std)

center_num = 100;
% choose appropriate width
method = 3.8;
[weight_woreg, record_random_centroid, record_centroid_idx, std] = RBFN_FCSR_woreg(train_data, train_target, center_num, method);

TrPred_woreg = predict_wbias(train_data, weight_woreg, record_random_centroid, std);
TePred_woreg = predict_wbias(test_data, weight_woreg, record_random_centroid, std);

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

% %----------------------------------------------------------------------------
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
% %----------------------------------------------------------------------------


% %----------------------------------------------------------------
% % Then, try different std
% % Comments: 
% % large std => result in these data are almost the same => Phi nearly singular 
% % small std => make these data looks more different => Phi non-singular 
% STD = [0.1, 0.5, 1, 3.8, 4.3, 5, 10, 100, 1000, 10000];
% best_test_acc = zeros(1, length(STD));
% for index = 1 : length(STD)
%     std = STD(index);
%     method = std;
%     [weight_woreg, record_random_centroid, record_centroid_idx, std] = RBFN_FCSR_woreg(train_data, train_target, center_num, method);
%     
%     TrPred_woreg = predict_wbias(train_data, weight_woreg, record_random_centroid, std);
%     TePred_woreg = predict_wbias(test_data, weight_woreg, record_random_centroid, std);
%     
%     % Performance (without regularization)
%     
%     TrAcc_woreg = zeros(1,1000);    % accuracy of training set
%     TeAcc_woreg = zeros(1,1000);    % accuracy of testing set
%     thr_woreg = zeros(1,1000);
%     TrN_woreg = length(train_target);   % training set size
%     TeN_woreg = length(test_target);    % testing set size
%     for i = 1:1000
%         % t starts from the Minimizer of training prediction, ends at the
%         % Maximizer of training prediction with equal step length 0.001
%         t = (max(TrPred_woreg)-min(TrPred_woreg)) * (i-1)/1000 + min(TrPred_woreg);
%         % the i-th threshold t
%         thr_woreg(i) = t;
%         TrAcc_woreg(i) = (sum(train_target(TrPred_woreg<t)==0) + sum(train_target(TrPred_woreg>=t)==1)) / TrN_woreg; 
%         TeAcc_woreg(i) = (sum(test_target(TePred_woreg<t)==0) + sum(test_target(TePred_woreg>=t)==1)) / TeN_woreg;
%     end
%     figure(index);
%     hold on;
%     plot(thr_woreg,TrAcc_woreg,'.-b ',thr_woreg,TeAcc_woreg,'^-r');
%     % find the best threshold as for testing accuracy
%     [best_teacc, best_idx] = max(TeAcc_woreg);
%     best_threshold = thr_woreg(best_idx);
% 
%     disp(['Best threshold is: ', num2str(best_threshold)]);
%     disp(['Best testing accuracy is: ', num2str(best_teacc)]);
%     best_test_acc(index) = best_teacc;
%     hold on;
%     plot(best_threshold, best_teacc, 'ko', LineWidth=10);
%     legend('train accuracy','test accuracy', 'Best Threshold');
%     title(['width = ', num2str(std)]);
% end
% figure(11)
% plot(1:length(STD), best_test_acc, '-^b');
% title('Different width')
% xlabel('width');
% ylabel('accuracy')
% set(gca,'XTick', 1:length(STD));
% set(gca,'XTickLabel', STD);

