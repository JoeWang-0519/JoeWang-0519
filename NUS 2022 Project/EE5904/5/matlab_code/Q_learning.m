function [Q_optimal, goal_reach, goal_reach_bool, aver_execu_time, execu_time, step_run1, state_run1_last, flag_run1_last, visit_run1] = Q_learning(reward, run, trial, discount, learning_rate, explore_prob)
% Q-learning algorithm
% Parameter:
% reward:       reward function;                            state * action
% run:          number of total runs;                       by default: 10
% trial:        in each run, the total number of trails;    by default: 3000
% discount:     the discount rate for future reward;        
% learning_rate:alpha_k to adjust the Q-function;           1 * k_max
% explore_prob: the exploring probability;                  1 * k_max

% Output:
% opt_policy:   the optimal policy through gready algorithm to converged
% Q-function
% goal_reach:   number of goal-reaching runs within total runs
% aver_execu_time:   the average execuation time of goal-reaching runs

% --------------------------------------------------------------------
% Here, we apply termination condition that alpha_k < 0.005;
%
% To achieve this, we restrict the parameter learning_rate is a 1 * k_max
% list such that learning_rate(k_max) >= 0.05 and k_max is the maxima
% number to achieve this! 

[~, k_max] = size(learning_rate);
[num_state, num_action] = size(reward);

% For record data:
% for each run, record the optimal Q-table
Q_optimal = zeros(num_state, num_action, run);  % Q_optimal(:, :, run)
% for each run, record optimal Q-table whether reaches goal
goal_reach_bool = zeros(1, run);
% for each run, record the execution time for all trials
execu_time = zeros(1, run);
% for 1-st run, record all trials the required number of steps
step_run1 = zeros(1, trial);
% record states for the last trial in 1-st run
% state_run1_last
% record exploration or exploitation for the last trial in 1-st run
% flag_run1_last
% record number of visits for each state in 1-st run
visit_run1 = zeros(1, num_state);

% --------------------------------------------------------------------
% Main function:
for i = 1 : run
    % initialize Q-table
    Q = zeros(num_state, num_action);
    % start counting time;
    tic;
    for j = 1 : trial
        start_state = 1;
        end_state = 100;
        % k represents the k-th step in each trial
        k = 1;
        % termination condition for each trial
        while (start_state ~= end_state) && (k <= k_max)
            % setting the parameter
            alpha_k = learning_rate(k);
            epsi_k = explore_prob(k);
            % selecting action (exploitation and exploration)
            [action, flag] = generate_action(Q, start_state, epsi_k);
            next_state = action2state(start_state, action);
            % update Q-table
            Q(start_state, action) = Q(start_state, action) + alpha_k * (reward(start_state, action) + discount * max(Q(next_state, :)) - Q(start_state, action));
            if (i == 1) && (j == trial)
                state_run1_last(k) = next_state;
                flag_run1_last(k) = flag;
            end
            if i == 1
                visit_run1(start_state) = visit_run1(start_state) + 1;
            end
            k = k + 1;
            start_state = next_state;
        end
        % record the required steps
        if i == 1
            step_run1(j) = k;
            visit_run1(start_state) = visit_run1(start_state) + 1;
        end
    end
    % the total time for all trials in one run
    total_time = toc;
    execu_time(i) = total_time;
    Q_optimal(:,:,i) = Q;
    
    % check the greedy policy of optimal Q-table whether can lead to goal
    if start_state == end_state
        % 1 indicates that, in i-th run, we reaches goal
        goal_reach_bool(i) = 1;
    end
end

goal_reach = sum(goal_reach_bool);
reach_idx = goal_reach_bool==1;
effective_execu_time = execu_time(reach_idx);
aver_execu_time = sum(effective_execu_time) / length(effective_execu_time);



