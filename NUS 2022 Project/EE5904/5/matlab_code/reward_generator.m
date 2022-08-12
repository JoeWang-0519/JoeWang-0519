function [total_reward, flag] = reward_generator(reward_table, start, ends, policy, discount)
% generate total reward from reward_table and policy and plot!
    total_reward = 0;
    % flag is to show achieve goal or not
    % flag = 1 -> achieve the goal
    % flag = 0 -> not achieve the goal
    flag = 1;
    kmax = 100;
    k = 0;
    start_state = start;
    end_state = ends;
    hold on;
    while (k < kmax) && (start_state ~= end_state)
        action = policy(start_state);
        total_reward = total_reward + discount ^ k * reward_table(start_state, action);
        k = k + 1;
        next_state = action2state(start_state, action);
        x_s = floor((start_state - 1)/10) + 1;
        y_s = 11 - mod(start_state, 10);
        x_n = floor((next_state - 1)/10) + 1;
        y_n = 11 - mod(next_state, 10);
        if y_s == 11
            y_s = 1;
        end
        if y_n == 11
            y_n = 1;
        end

        plot([x_s, x_n], [y_s, y_n], 'k', LineWidth = 1);
        start_state = next_state;
    end

% 
%     if k == kmax
%         flag = 0;
%         total_reward = 0;
%     end
