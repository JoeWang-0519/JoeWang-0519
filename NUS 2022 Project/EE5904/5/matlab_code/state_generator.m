function [state_seq, flag] = state_generator(start, ends, policy)
% generate the state-transition sequence (column vector)
    policy_col = reshape(policy, [100, 1]);
    % flag is to show achieve goal or not
    % flag = 1 -> achieve the goal
    % flag = 0 -> not achieve the goal
    flag = 1;
    count = 1;
    state_seq(count) = start;
    cur = start;
    while (cur ~= ends)
        count = count + 1;
        action = policy_col(cur);
        next = action2state(cur, action);
        state_seq(count) = next;
        cur = next;
        if count >= 100
            flag = 0;
            break
        end
    end
    state_seq = state_seq';

