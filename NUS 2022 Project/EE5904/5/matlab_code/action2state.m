function next_state = action2state(cur_state, action)
% generate next state from current state and action
    switch action
        case 1
            next_state = cur_state - 1;
        case 2
            next_state = cur_state + 10;
        case 3
            next_state = cur_state + 1;
        case 4
            next_state = cur_state - 10;
    end
    
