clear all;
clc;
%----------------------------------------------------------------------
% load reward
load task1.mat
%----------------------------------------------------------------------
% parameter
run = 10;
trial = 3000;
discount_all = [0.5, 0.9];
start_state = 1;
end_state = 100;

% learning rate and exploration probability
load learning_rate.mat

%----------------------------------------------------------------------
% Main function
% step_run1 is set to check the convergence for one single run
for i = 1 : 4
    for j = 1 : 2
        switch i
            case 1
                learning_rate = learning_rate1;
                explore_prob = learning_rate;
            case 2
                learning_rate = learning_rate2;
                explore_prob = learning_rate;
            case 3
                learning_rate = learning_rate3;
                explore_prob = learning_rate;
            case 4
                learning_rate = learning_rate4;
                explore_prob = learning_rate;
        end

        discount = discount_all(j);

        [Q_optimal, goal_reach, goal_reach_bool, aver_execu_time, execu_time, step_run1, state_run1_last, flag_run1_last, visit_run1] = Q_learning(reward, run, trial, discount, learning_rate, explore_prob);
        filename = ['result_', 'dis', num2str(discount), '_learn', num2str(i), '.mat'];
        save(filename);
    end
end
