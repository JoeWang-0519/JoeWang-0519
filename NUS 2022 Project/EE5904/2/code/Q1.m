clear all;
clc;
% PART 0
% the figure of Rosenbrock' valley function

%x1 = [-4, 4];
%y1 = [-4, 4];

[x1, y1] = meshgrid(-1:.05:1, -1:.05:1);
z1 = (1-x1).^2 + 100*(y1-x1.^2).^2;
mesh(x1,y1,z1)

% PART 1
% b) Gradient Descent(Steepest Descent)
syms x1 x2;
f = (1-x1)^2+100*(x2-x1^2)^2;
% test function
f_test = (x1-2)^2 + 2*(x2-1)^2;

%x = unifrnd(-1,1,2,1);
%x= [0.264718492450819;-0.804919190001181];
%x = [0.531033576298005;0.590399802274126];
x=[0.2, -0.5]';
epi_grad = 1e-05;
epi_hess = 1e-06;
epi_fv = 1e-09;
max_iter = 15000;
eta1 = 0.001;
eta2 = 1.0;

%[iter, result, record_x, record_f] = steepestdes1(f, x, epi_grad, epi_fv, max_iter, eta1);
%[iter, result, record_x, record_f] = steepestdes2(f, x, epi_grad, epi_fv, max_iter);
[iter, result, record_x, record_f] = newton(f, x, epi_hess, epi_fv, max_iter);

%plot the trajacotry
hold on
figure(1)
p = plot3(record_x(1,:), record_x(2,:), record_f, 'k');
p.LineWidth = 2;

figure(2)
scatter(x(1), x(2));
hold on
plot(record_x(1,:), record_x(2,:),'k');
grid on;
