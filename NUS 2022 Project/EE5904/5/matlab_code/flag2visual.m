function [] = flag2visual(flag_run1_last)
% visualize the exploration or exploitation in the last trial of first run
    scatter(1 : length(flag_run1_last), flag_run1_last, 35, 'filled');
    axis([1, length(flag_run1_last),-0.5,1.5])