clear all;
clc;
load mnist_modify.mat

% Exact Interpolation Method
std = 4.3;
%std = 100;

% train_data: 784 * 1000;
% train_target: 1* 1000; Binary classifcation; 
% digit 0 & 7 -> 1
% digit 1, 2, 3, 4, 5, 6, 8, 9 -> 0
% 
weight_woreg = RBFN_exact_woreg(train_data, train_target, std); % 1 * 1000 vector

TrPred_woreg = predict_wobias(train_data, weight_woreg, train_data, std);
TePred_woreg = predict_wobias(test_data, weight_woreg, train_data, std);

TrAcc_woreg = zeros(1,1000);    % accuracy of training set
TeAcc_woreg = zeros(1,1000);    % accuracy of testing set
thr_woreg = zeros(1,1000);      % threshold record
TrN_woreg = length(train_target);   % training set size
TeN_woreg = length(test_target);    % testing set size

% 
% %--------------------------------------------------------------------
% % without regularization visualization of performance
% for i = 1:1000
%     %t starts from the Minimizer of training prediction, ends at the
%     % Maximizer of training prediction with equal step length 0.001
%     t = (max(TrPred_woreg)-min(TrPred_woreg)) * (i-1)/1000 + min(TrPred_woreg);
%     % the i-th threshold t
%     thr_woreg(i) = t;
%     TrAcc_woreg(i) = (sum(train_target(TrPred_woreg<t)==0) + sum(train_target(TrPred_woreg>=t)==1)) / TrN_woreg; 
%     TeAcc_woreg(i) = (sum(test_target(TePred_woreg<t)==0) + sum(test_target(TePred_woreg>=t)==1)) / TeN_woreg;
% end
% 
% plot(thr_woreg,TrAcc_woreg,'.- ',thr_woreg,TeAcc_woreg,'^-');
% title(['width = ', num2str(std)])
% 
% % find the best threshold as for testing accuracy
% [best_teacc, best_idx] = max(TeAcc_woreg);
% 
% disp(['Best threshold is: ', num2str(thr_woreg(best_idx))]);
% disp(['Best testing accuracy is: ', num2str(best_teacc)]);
% hold on;
% plot(thr_woreg(best_idx), best_teacc, 'ko', LineWidth=10);
% legend('train accuracy','test accuracy', 'Best Threshold');
% 
% %----------------------------------------------------------------------------
% % visualize the RBFN map
% label0_pre_te = TePred_woreg(test_target==0);
% label1_pre_te = TePred_woreg(test_target==1);
% label0_pre_tr = TrPred_woreg(train_target==0);
% label1_pre_tr = TrPred_woreg(train_target==1);
% 
% figure(2)
% subplot(2,1,1);
% scatter(label0_pre_te, zeros(1, length(label0_pre_te)), 'r');
% hold on;
% scatter(label1_pre_te, ones(1, length(label1_pre_te)), 'b');
% title(['Testing set, std = ', num2str(std)]);
% ones_ = ones(1, length(label1_pre_te));
% num_cor_test = sum(ones_(label1_pre_te>=thr_woreg(best_idx)));
% disp(['number of label 1 testing samples are predicted correctly :', num2str(num_cor_test)]);
% plot([thr_woreg(best_idx), thr_woreg(best_idx)], [0,1], 'k');
% legend('label 0 prediction', 'label 1 prediction','Best Threshold');
% 
% subplot(2,1,2);
% scatter(label0_pre_tr, zeros(1, length(label0_pre_tr)), 'r');
% hold on;
% scatter(label1_pre_tr, ones(1, length(label1_pre_tr)), 'b');
% title(['Training set, std = ', num2str(std)]);
% ones_ = ones(1, length(label1_pre_tr));
% num_cor_train = sum(ones_(label1_pre_tr>=thr_woreg(best_idx)));
% plot([thr_woreg(best_idx), thr_woreg(best_idx)], [0,1], 'k');
% legend('label 0 prediction', 'label 1 prediction','Best Threshold');
% %----------------------------------------------------------------------------

%--------------------------------------------------------------------

% Regularization case

%REG = [0, 0.001, 0.01, 0.05, 0.1, 0.2, 0.4];
REG = [0.01];
best_test_acc = zeros(1, length(REG));
for index = 1: length(REG)
    reg = REG(index);
    weight_wreg = RBFN_exact_wreg(train_data, train_target, std, reg); % 1 * 1000 vector
    
    TrPred_wreg = predict_wobias(train_data, weight_wreg, train_data, std);
    TePred_wreg = predict_wobias(test_data, weight_wreg, train_data, std);
   
    figure(index);
    
    % Performance (with regularization)
    
    TrAcc_wreg = zeros(1,1000);    % accuracy of training set
    TeAcc_wreg = zeros(1,1000);    % accuracy of testing set
    thr_wreg = zeros(1,1000);
    TrN_wreg = length(train_target);   % training set size
    TeN_wreg = length(test_target);    % testing set size
    for i = 1:1000
        % t starts from the Minimizer of training prediction, ends at the
        % Maximizer of training prediction with equal step length 0.001
        t = (max(TrPred_wreg)-min(TrPred_wreg)) * (i-1)/1000 + min(TrPred_wreg);
        % the i-th threshold t
        thr_wreg(i) = t;
        TrAcc_wreg(i) = (sum(train_target(TrPred_wreg<t)==0) + sum(train_target(TrPred_wreg>=t)==1)) / TrN_wreg; 
        TeAcc_wreg(i) = (sum(test_target(TePred_wreg<t)==0) + sum(test_target(TePred_wreg>=t)==1)) / TeN_wreg;
    end
    hold on;
    plot(thr_wreg,TrAcc_wreg,'.-b ',thr_wreg,TeAcc_wreg,'^-r');
    % find the best threshold as for testing accuracy
    [best_teacc, best_idx] = max(TeAcc_wreg);
    best_threshold = thr_wreg(best_idx);

    disp(['Best threshold is: ', num2str(best_threshold)]);
    disp(['Best testing accuracy is: ', num2str(best_teacc)]);
    best_test_acc(index) = best_teacc;
    hold on;
    plot(best_threshold, best_teacc, 'ko', LineWidth=10);
    legend('train accuracy','test accuracy', 'Best Threshold');
    title(['width = ', num2str(std), ', regularization = ', num2str(reg)]);
end

% visualize the RBFN map
label0_pre_te_reg = TePred_wreg(test_target==0);
label1_pre_te_reg = TePred_wreg(test_target==1);
label0_pre_tr_reg = TrPred_wreg(train_target==0);
label1_pre_tr_reg = TrPred_wreg(train_target==1);

figure(9)
subplot(2,1,1);
scatter(label0_pre_te_reg, zeros(1, length(label0_pre_te_reg)), 'r');
hold on;
scatter(label1_pre_te_reg, ones(1, length(label1_pre_te_reg)), 'b');
title(['Testing set, std = ', num2str(std)]);
ones_ = ones(1, length(label1_pre_te_reg));

num_cor_test = sum(ones_(label1_pre_te_reg>=best_threshold));
disp(['number of label 1 testing samples are predicted correctly :', num2str(num_cor_test)]);
plot([best_threshold, best_threshold], [0,1], 'k');
legend('label 0 prediction', 'label 1 prediction','Best Threshold');

subplot(2,1,2);
scatter(label0_pre_tr_reg, zeros(1, length(label0_pre_tr_reg)), 'r');
hold on;
scatter(label1_pre_tr_reg, ones(1, length(label1_pre_tr_reg)), 'b');
title(['Training set, std = ', num2str(std)]);
ones_ = ones(1, length(label1_pre_tr_reg));
num_cor_train = sum(ones_(label1_pre_tr_reg>=best_threshold));
plot([best_threshold, best_threshold], [0,1], 'k');
legend('label 0 prediction', 'label 1 prediction','Best Threshold');

figure(10)
plot(1:length(REG), best_test_acc, '-^b');
title('Different Regularization')
xlabel('regularization factor');
ylabel('accuracy')
set(gca,'XTick', 1:length(REG));
set(gca,'XTickLabel', REG);
% %----------------------------------------------------------------------------
% 
% 
