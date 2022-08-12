function [] = visit2visual(visit_run1)  
    % in one run, the number of visits to each state
    x_axis = 1 : length(visit_run1);
    plot(x_axis, visit_run1, LineWidth = 1.5)