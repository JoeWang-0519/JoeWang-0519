
% %----------------------------------------------------------------------
% visualization
% Q_table = Q_optimal(:,:,1);
% figure(1)
% optimal_policy = Q_table2policy(Q_table);
% total_reward = reward_generator(reward, start_state, end_state, optimal_policy, discount);
% title(['discount=0.9, method=4, reward=',num2str(total_reward)]);
% 
% figure(2)
% visit2visual(visit_run1);
% title('number of visits to each state during one run')
% xlabel('state')
% ylabel('number of visits');
% 
% figure(3)
% step2visual(step_run1);
% title('number of steps for each trial during one run')
% xlabel('trial')
% ylabel('number of steps');
% 
% figure(4)
% flag2visual(flag_run1_last)
% title('exploration or exploitation in the last trial of first run')
% xlabel('step')
% yticks([0 1]);
% yticklabels({'exploitation', 'exploration'});
% 
% %----------------------------------------------------------------------
% visualization codes
figure(1)
for num = 1 : 8
    if num <= 4
        method = num;
        dis = 0.5;
    else
        method = num - 4;
        dis = 0.9;
    end
    filename = ['result_', 'dis', num2str(dis), '_learn', num2str(method), '.mat'];
    load(filename);
    subplot(2,4,num);
    Q_table = Q_optimal(:,:,1);
    optimal_policy = Q_table2policy(Q_table);
    total_reward = reward_generator(reward, start_state, end_state, optimal_policy, discount);
    title(['discount=',num2str(dis),',method=',num2str(method)])
end





