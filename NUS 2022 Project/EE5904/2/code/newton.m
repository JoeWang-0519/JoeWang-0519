%Newton Method
function [iter, result, record_x, record_f] = newton(f, x, epi_hess, epi_fv, max_iter)

% f: the function f(x)
% x: initial point of algorithm
% epi_update: the tolerated error bound of update
% epi_fv: the tolerated error bound of function value decrease
% max_iter: the maxima number of iteration

% iter: the number of iteration
% result: the terminal point of algorithm
% record_x: the trajactory of x
% record_f: the trajactory of function value

syms x1 x2;

fx = diff(f, x1);
fy = diff(f, x2);
fxx = diff(fx, x1);
fxy = diff(fx, x2);
fyx = diff(fy, x1);
fyy = diff(fy, x2);

% gradient
grad = [fx; fy];
% Hessian
Hess = [fxx, fxy;
    fyx, fyy];

flag = 1;
iter = 0;

% function value at initial point
f_last = double(subs(f, [x1,x2], x'));

record_x = [x];
record_f = [f_last];

while (flag && (iter<max_iter))
    grad_update = double(subs(grad, [x1,x2], x'));
    Hess_update = double(subs(Hess, [x1,x2], x'));
    dir_update = - Hess_update\ grad_update;
    
    nor = norm(dir_update);
    if (nor>=epi_hess)
        % update weight
        % fix learning rate
        x = x + dir_update;
        % the new function value
        f_new = double(subs(f, [x1,x2], x'));
        record_x = [record_x, x];
        record_f = [record_f, f_new];
        iter = iter + 1;
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



