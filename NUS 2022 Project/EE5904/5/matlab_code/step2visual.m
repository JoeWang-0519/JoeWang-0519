function [] = step2visual(step_run1)  
    % in one run, the number of steps in each trial
    x_axis = 1 : length(step_run1);
    plot(x_axis, step_run1)