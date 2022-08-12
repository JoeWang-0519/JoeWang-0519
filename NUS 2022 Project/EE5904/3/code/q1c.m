clear all;
clc;
%Function Approximation

x_train = [-1.6: 0.08: 1.6];
x_test = [-1.6: 0.01: 1.6];
% training set with random noise
%record_randn = 0.3 * randn(1, 41);
%y_train = 1.2 * sin(pi * x_train) - cos(2.4 * pi * x_train) + record_randn;
y_train = [0.311577393770675	0.378112952625106	0.658486707908682	1.66110315090113	2.11320575488674	1.73034110860957	1.12270819679774	-0.0352918346975698	-0.684772043278092	-1.87208303985565	-1.90195246347018	-1.82683957595898	-1.04273018139262	-0.712288786438255	-0.656154435786554	-0.152010593069156	-0.474195526467749	-0.784967276171051	-0.675271461285771	-1.08793463135819	-0.880491146150202	-0.259913765960200	0.275769838404923	1.22321188075539	1.96402393886018	2.48456511887934	2.22852669911097	2.07311843897311	0.979718623378620	0.253669312511928	0.247159537904824	-0.649897908262488	-0.428029311188398	0.112994203781400	0.160068773056403	0.645914216840377	0.360147443326543	-0.322988568206957	-1.27426397168327	-1.47600646094217	-2.43236084744215];
record_randn = y_train -(1.2 * sin(pi * x_train) - cos(2.4 * pi * x_train));

y_test = 1.2 * sin(pi * x_test) - cos(2.4 * pi * x_test);

% visualization
plot(x_train, y_train, '--r')
hold on;
plot(x_test, y_test, 'b');

%----------------------------------------------------------
% q1c
% Regularization on Exact Interpolation Method
sigma = 0.1;
regularization = 0.5;
X_train = x_train;
target_train = y_train;
w = RBFN_exact_wreg(X_train, target_train, sigma, regularization);
predict_test = predict_wobias(x_test, w, X_train, sigma);
predict_train = predict_wobias(x_train, w, X_train, sigma);
hold on;
plot(x_test, predict_test, 'k', LineWidth = 1);
legend('training set with random noise', 'testing set', 'prediction');
title('The Result of RBFN with regularization')

err_train = predict_train - y_train;
err_test = predict_test - y_test;
MSE_train = 0.5 * (norm(err_train))^2,
MSE_test = 0.5 * (norm(err_test))^2,

%----------------------------------------------------------
% Part 2: Comparision
Reg = [0, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.8, 0.9, 1, 1.1, 1.2, 2];
MSE_Train_reg = zeros(1, length(Reg));
MSE_Test_reg = zeros(1, length(Reg));

for i = 1 : length(Reg)
    regularization = Reg(i);
    w = RBFN_exact_wreg(X_train, target_train, sigma, regularization);
    predict_test = predict_wobias(x_test, w, X_train, sigma);
    predict_train = predict_wobias(x_train, w, X_train, sigma);
    err_train = predict_train - y_train;
    err_test = predict_test - y_test;
    MSE_Train_reg(i) = 0.5 * (norm(err_train))^2;
    MSE_Test_reg(i) = 0.5 * (norm(err_test))^2;
end

figure(2);
plot(1:length(Reg), MSE_Train_reg,'-*k');
hold on;
plot(1:length(Reg), MSE_Test_reg,'-^b');
set(gca,'XTick', 1:length(Reg));
set(gca,'XTickLabel', Reg);
set(gca,'XLim', [1,length(Reg)])
legend('MSE in training set', 'MSE in testing set');
title('The Performance of training and testing set');
xlabel('regularization');
ylabel('MSE')
