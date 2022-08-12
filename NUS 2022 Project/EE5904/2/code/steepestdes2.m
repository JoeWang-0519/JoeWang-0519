% EXACT MINIMIZER FORM (ADAPTIVE LEARNING RATE)
function [iter, result, record_x, record_f] = steepestdes2(f, x, epi_grad, epi_fv, max_iter)

% f: the function f(x)
% x: initial point of algorithm
% epi_grad: the tolerated error bound of gradient
% epi_fv: the tolerated error bound of function value decrease
% max_iter: the maxima number of iteration

% iter: the number of iteration
% result: the terminal point of algorithm
% record_x: the trajactory of x
% record_f: the trajactory of function value

% m is learning rate
syms x1 x2 m;
% negative gradient
dir = -[diff(f,x1); diff(f,x2)];
flag = 1;
iter = 0;

% calculate the last function value
f_last = double(subs(f, [x1,x2], x'));

record_x = [x];
record_f = [f_last];
while (flag && (iter<max_iter))
    dir_update = double(subs(dir, [x1,x2], x'));
    nor = norm(dir_update);
    if (nor>=epi_grad)
        % update weight
        % search for the best learning rate
        x_update = x + m * dir_update;
        f_temp = subs(f, [x1,x2], x_update');
        % search m s.t gradient_m=0
        h = diff(f_temp, m);
        m_update = solve(h);
        x = x + double(m_update(1)) * dir_update;
        % the new function value
        f_new = double(subs(f, [x1,x2], x'));
        iter = iter + 1;
        record_x = [record_x, x];
        record_f = [record_f, f_new];
        
        if (abs(f_new-f_last)<=epi_fv)
            flag = 0;
        else
            f_last = f_new;
        end
    else
        flag = 0;
    end
end
result = double(x);
end
        
        
        

