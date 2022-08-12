clear all;
clc;

%Function Approximation

x_train = [-1.6: 0.08: 1.6];
x_test = [-1.6: 0.01: 1.6];
% training set with random noise
%record_randn = 0.3 * randn(1, 41);
%y_train = 1.2 * sin(pi * x_train) - cos(2.4 * pi * x_train) + record_randn;
% we use this to write the report
y_train = [0.311577393770675	0.378112952625106	0.658486707908682	1.66110315090113	2.11320575488674	1.73034110860957	1.12270819679774	-0.0352918346975698	-0.684772043278092	-1.87208303985565	-1.90195246347018	-1.82683957595898	-1.04273018139262	-0.712288786438255	-0.656154435786554	-0.152010593069156	-0.474195526467749	-0.784967276171051	-0.675271461285771	-1.08793463135819	-0.880491146150202	-0.259913765960200	0.275769838404923	1.22321188075539	1.96402393886018	2.48456511887934	2.22852669911097	2.07311843897311	0.979718623378620	0.253669312511928	0.247159537904824	-0.649897908262488	-0.428029311188398	0.112994203781400	0.160068773056403	0.645914216840377	0.360147443326543	-0.322988568206957	-1.27426397168327	-1.47600646094217	-2.43236084744215];
y_test = 1.2 * sin(pi * x_test) - cos(2.4 * pi * x_test);
record_randn = y_train -(1.2 * sin(pi * x_train) - cos(2.4 * pi * x_train));

% visualization
plot(x_train, y_train, '--r')
hold on;
plot(x_test, y_test, 'b');

% Fixed Center Selected Randomly

% Appropriate std(width)
method = -1;
% 20 centroids
center_num = 20;

X_train = x_train;
target_train = y_train;

%------------------------------------------------------------------
% q1c without regularization case

[w, record_random_centroid, record_centroid_idx, sigma] = RBFN_FCSR_woreg(X_train, target_train, center_num, method);
predict_test = predict_wbias(x_test, w, record_random_centroid, sigma);
predict_train = predict_wbias(x_train, w, record_random_centroid, sigma);
hold on;
plot(x_test, predict_test, 'k', LineWidth = 1);
legend('training set with random noise', 'testing set', 'prediction');
title('The Result of RBFN without regularization')

% MSE
err_train = predict_train - y_train;
err_test = predict_test - y_test;
MSE_train = 0.5 * (norm(err_train))^2,
MSE_test = 0.5 * (norm(err_test))^2,


figure(2);
subplot(3,1,1);
bar(x_test, err_test);
title('Error in testing set');
legend('Error = Predict - Target')
subplot(3,1,2);
bar(x_train, err_train);
title('Error in training set');
legend('Error = Predict - Target')
subplot(3,1,3);
bar(x_train, record_randn,'FaceColor',[0 .5 .5]);
title('Random noise of training set')
legend('Random Noise')

%------------------------------------------------------------------
% EXTRA:
% regularization case
regularization = 0.00001;
% Here we use the previous recorded centroid
centroid_idx = record_centroid_idx;

figure(3);
subplot(2,1,1)
plot(x_train, y_train, '--r')
hold on;
plot(x_test, y_test, 'b');
hold on;
plot(x_test, predict_test, 'k', LineWidth = 1);
legend('training set with random noise', 'testing set', 'prediction');
title('The Result of RBFN without regularization')

[w, record_random_centroid, sigma] = RBFN_FCSR_wreg_fix(X_train, target_train, center_num, regularization, centroid_idx);
predict_test = predict_wbias(x_test, w, record_random_centroid, sigma);
predict_train = predict_wbias(x_train, w, record_random_centroid, sigma);


figure(3);
subplot(2,1,2)
plot(x_train, y_train, '--r')
hold on;
plot(x_test, y_test, 'b');
hold on;
plot(x_test, predict_test, 'k', LineWidth = 1);
legend('training set with random noise', 'testing set', 'prediction');
title('The Result of RBFN with regularization')

% MSE
err_train = predict_train - y_train;
err_test = predict_test - y_test;
MSE_train = 0.5 * (norm(err_train))^2,
MSE_test = 0.5 * (norm(err_test))^2,


figure(4);
subplot(3,1,1);
bar(x_test, err_test);
title('Error in testing set');
legend('Error = Predict - Target')
subplot(3,1,2);
bar(x_train, err_train);
title('Error in training set');
legend('Error = Predict - Target')
subplot(3,1,3);
bar(x_train, record_randn,'FaceColor',[0 .5 .5]);
title('Random noise of training set')
legend('Random Noise')
%------------------------------------------------------------------
Reg = [1, 0.0001, 0.00001, 0.000001, 0.0000001, 0];
MSE_Train_reg = zeros(1, length(Reg));
MSE_Test_reg = zeros(1, length(Reg));

for i = 1 : length(Reg)
    regularization = Reg(i);
    [w, record_random_centroid, sigma] = RBFN_FCSR_wreg_fix(X_train, target_train, center_num, regularization, centroid_idx);
    predict_test = predict_wbias(x_test, w, record_random_centroid, sigma);
    predict_train = predict_wbias(x_train, w, record_random_centroid, sigma);
    err_train = predict_train - y_train;
    err_test = predict_test - y_test;
    MSE_Train_reg(i) = 0.5 * (norm(err_train))^2;
    MSE_Test_reg(i) = 0.5 * (norm(err_test))^2;
end

figure(5);
plot(1:length(Reg), MSE_Train_reg,'-*k');
hold on;
plot(1:length(Reg), MSE_Test_reg,'-^b');
set(gca,'XTick', 1:length(Reg));
set(gca,'XTickLabel', Reg);
legend('MSE in training set', 'MSE in testing set');


%------------------------------------------------------------------
% EXTRA:
% Find the Influence of Centroids Number (without regularization)
% CENTER = [5, 8, 10, 20, 30, 40];
% MSE_Train = zeros(1,length(CENTER));
% MSE_Test = zeros(1,length(CENTER));
% for i = 1 : length(CENTER)
%     center_num = CENTER(i);
%     [w, record_random_centroid, record_centroid_idx, sigma] = RBFN_FCSR_woreg(X_train, target_train, center_num, method);
%     predict_test = predict_wbias(x_test, w, record_random_centroid, sigma);
%     predict_train = predict_wbias(x_train, w, record_random_centroid, sigma);
%     err_train = predict_train - y_train;
%     err_test = predict_test - y_test;
%     MSE_Train(i) = 0.5 * (norm(err_train))^2;
%     MSE_Test(i) = 0.5 * (norm(err_test))^2;
% end
% figure(3)
% plot(1:6, MSE_Train,'-*k');
% hold on;
% plot(1:6, MSE_Test,'-^b');
% set(gca,'XTick', 1:6);
% set(gca,'XTickLabel', CENTER);
% legend('MSE in training set', 'MSE in testing set');
