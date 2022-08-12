% select the optimal hyper-parameters discount rate
% we fix learning rate at the second type 100/(100+k)
clear all; 
clc;
%----------------------------------------------------------------------
% load reward
load task1.mat
%----------------------------------------------------------------------
% parameter
run = 10;
trial = 3000;
discount_all = [0.6, 0.7, 0.8, 0.95];
start_state = 1;
end_state = 100;

% learning rate and exploration probability
load learning_rate.mat

learning_rate = learning_rate2;
explore_prob = learning_rate;
%----------------------------------------------------------------------
% Main function
for i = 1 : length(discount_all)
    discount = discount_all(i);
    [Q_optimal, goal_reach, goal_reach_bool, aver_execu_time, execu_time, step_run1, state_run1_last, flag_run1_last, visit_run1] = Q_learning(reward, run, trial, discount, learning_rate, explore_prob);
    filename = ['result_', 'dis', num2str(discount), '_learn2.mat'];
    save(filename);
end
