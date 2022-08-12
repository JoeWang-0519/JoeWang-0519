function optimal_policy = Q_table2policy(Q_optimal)
% transfom optimal Q-table to optimal policy and achieve visualization
    [~, optimal_policy] = max(Q_optimal, [], 2);
    optimal_policy = reshape(optimal_policy, [10, 10]);
    hold on;
    for i = 1 : 10
        for j = 1 : 10
            action = optimal_policy(i, j);
            x = j;
            y = 11 - i;
            switch action
                case 1
                    plot(x,y, '^b', 'LineWidth', 1);
                case 2
                    plot(x,y,'>k', 'LineWidth', 1);
                case 3
                    plot(x,y,'vr', 'LineWidth', 1);
                case 4
                    plot(x,y,'<g', 'LineWidth', 1);
            end
        end
    end

    for i = 1 : 11
        plot([0.5, 10.5],[i - 0.5, i - 0.5], 'b', 'LineWidth', 1);
    end

    for i = 1 : 11
        plot([i - 0.5, i - 0.5], [0.5, 10.5], 'b', 'LineWidth', 1);
    end
    axis([0 11 0 11]);
    
    