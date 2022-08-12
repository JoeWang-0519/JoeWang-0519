function [action, flag] = generate_action(Q, start_state, epsi_k)
% generate action from Q function and start_state, exploration rate
    % If exploration, flag = 1;
    % If exploitation, flag = 0;
    flag = 0;
    candidate_action = [1, 2, 3, 4];

    if start_state <= 10
        candidate_action(4) = 0;
    end
    if start_state >= 91
        candidate_action(2) = 0;
    end
    if mod(start_state, 10) == 1
        candidate_action(1) = 0;
    end
    if mod(start_state, 10) == 0
        candidate_action(3) = 0;
    end

    zero_idx = candidate_action == 0;
    candidate_action(zero_idx) = [];
    
    % find the Q-value for current state and all candidate actions
    Q_cur = Q(start_state, candidate_action);
    [~, argmax_Q] = max(Q_cur);
    rnd = unifrnd(0, 1);
    if (rnd >= epsi_k)
        % exploitation
        action = candidate_action(argmax_Q);
    else
        % exploration
        % rule out the best action at this state
        candidate_action(argmax_Q) = [];
        [~, len] = size(candidate_action);
        idx = randperm(len);
        action = candidate_action(idx(1));
        flag = 1;
    end
  
        
