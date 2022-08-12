% For Task 2, here, as discussed in the report, we set the hyper-parameters
% as follows:
% 1. learning rate = 100/(100+k)
% 2. discount rate = 0.8

%------------------------------------------------------------------------
% qevalreward -> 100 * 4

%------------------------------------------------------------------------
load learning_rate.mat
learning_rate = learning_rate2;
explore_prob = learning_rate;

run = 10;
trial = 3000;
discount = 0.8;
start_state = 1;
end_state = 100;
reward = qevalreward;       % 100*4 matrix

% Q_optimal is the optimal Q-table for 10-runs
[Q_optimal, goal_reach, goal_reach_bool, aver_execu_time, execu_time, step_run1, state_run1_last, flag_run1_last, visit_run1] = Q_learning(reward, run, trial, discount, learning_rate, explore_prob);

% Q_table is one of the optimal table
Q_table = Q_optimal(:,:,1);

% generate state sequence
optimal_policy = Q_table2policy(Q_table);
[total_reward, flag1] = reward_generator(reward, start_state, end_state, optimal_policy, discount);
title(['Total reward is: ', num2str(total_reward)]);
[qevalstates, flag2] = state_generator(start_state, end_state, optimal_policy);

