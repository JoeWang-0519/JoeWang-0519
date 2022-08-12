clear all;
clc;

% MSA method is solved by iteration
% CASE 1: a(t)=t^2;
lambda = 1;
max_iter = 100;
eta = 2;
tic
% 1. Discretization
time_seg = 51;
t = linspace(0, 1, time_seg);
delta_t = 1 / (time_seg - 1);

% 2. Initialization of u(t) = t
U = zeros(1, time_seg);

for idx = 1 : time_seg
   U(idx) = t(idx);
end

S = zeros(2, time_seg);
S(:, 1) = [1; 0];
P = zeros(2, time_seg);
M = [1, 0; 0, 0];
B_time = [0; 1];

% 3. Iteration
for iter = 1 : max_iter
    % Solve for s(t)    Forward
    for idx = 1 : time_seg - 1
        time = t(idx);
        A_time = [0, 1;
        0, - time ^ 2];
        S_time = S(:, idx);
        U_time = U(idx);
        derivative = A_time * S_time + B_time *  U_time;
        S(:, idx + 1) = S(:, idx) + derivative * delta_t;
    end

    % Solve for p(t)    Backward
    P(:, time_seg) = -2 * M * S(:, time_seg);
    for idx = time_seg : -1 : 2
        time = t(idx);
        A_time = [0, 1;
        0, - time ^ 2];
        P_time = P(:, idx);
        derivative = - A_time' * P_time;
        P(:, idx - 1) = P(:, idx) - derivative * delta_t;
    end

    % Calculate U(t)    Closed-form
    for idx = 1 : time_seg
        % Standard MSA Method (cannot guarantee convergence for small lambda)
        %U(idx) = B_time' * P(:, idx) / (2 * lambda);
        U(idx) = U(idx) + eta * (B_time' * P(:, idx) - 2 * lambda * U(idx));
    end
end
t2=toc;

figure(1);
subplot(2, 1, 1);
grid on;
hold on;
plot(t, S(1, :));
plot(t, S(2, :));
legend('position curve', 'velocity curve')
title('MSA Method')
subplot(2,1,2);
plot(t, U, Color='red');
title('control curve');
grid on;
S

