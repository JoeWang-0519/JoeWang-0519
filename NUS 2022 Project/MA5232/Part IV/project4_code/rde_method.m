clear all;
clc;
tic
% Use Question 2(b) to solve for P(t)
% CASE 1: a(t)=t^2;
lambda = 1;
% 1. Discretization
time_seg = 51;
t = linspace(0, 1, time_seg);
delta_t = 1 / (time_seg - 1);
X = zeros(2, 2, time_seg);
Y = zeros(2, 2, time_seg);
% 2. Initialization
X(:, :, time_seg) = [1, 0;
    0, 1];
Y(:, :, time_seg) = [-2, 0;
    0, 0];
% 3. Iteration
for idx = time_seg : -1 : 2
    time = t(idx);
    A_time = [0, 1;
        0, - sin(10 * time)];
    tmp = [0, 0;
        0, 1]/(2 * lambda);
    derivative = [A_time, tmp;
        zeros(2,2), -A_time'] * [X(:, :, idx); Y(:, :, idx)];
    X(:, :, idx - 1) = X(:, :, idx) - derivative(1:2, :) * delta_t;
    Y(:, :, idx - 1) = Y(:, :, idx) - derivative(3:4, :) * delta_t;
end

P = zeros(2, 2, time_seg);
for idx = 1 : time_seg
    X_tmp = X(:, :, idx);
    Y_tmp = Y(:, :, idx);
    P(:, :, idx) = - 0.5 * Y_tmp * inv(X_tmp);
end

% 4. Solve for state s_t = [x_t; v_t];
S = zeros(2, time_seg);
S(:, 1) = [1; 0];
for idx = 1 : time_seg - 1
    time = t(idx);
    A_time = [0, 1;
        0, - sin(10 * time)];
    P_time = P(:, :, idx);
    tmp = [0, 0; 0, 1] / lambda;
    derivative = (A_time - tmp * P_time)  * S(:, idx);
    S(:, idx + 1) = S(:, idx) + derivative * delta_t;
end

U = zeros(1, time_seg);

for idx = 1 : time_seg
    U(idx) = - [0, 1] * P(:, :, idx) * S(:, idx) / lambda;
end
t1=toc;

figure(2);
subplot(2, 1, 1);
grid on;
hold on;
plot(t, S(1, :));
plot(t, S(2, :));
legend('position curve', 'velocity curve')
title(['RDE Method, ', 'lambda = ',num2str(lambda)])
subplot(2,1,2);
plot(t, U, Color='red');
title('control curve');
grid on;

S


