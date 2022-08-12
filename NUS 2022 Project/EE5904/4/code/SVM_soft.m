function [bias, alpha, flag, K] = SVM_soft(X, d, C, Method, gamma, threshold1, threshold2)

% Parameter: 
% X: feature vector;    size: dimension * number
% d: label vector:      size: number * 1
% C: penalty coefficient;   set C=10e6 to force soft-margin SVM to hard-margin SVM
% Method: form of Kernel;   candidate {1,2,3,4,5,inf}
%                           i: i-order polynomial Kernel
%                           inf: rbf Kernel
% gamma: parameter for rbf kernel
% threshold1: threshold for Mercer's thm (check whether is a valid Kernel)
% threshold2: threshold for SV
%
%
% Output:
% bias: the bias term in discriminant function  note: other terms can be
% determined from alpha, d and Kernel
%
% alpha: optimal solution for dual problem;     size: number * 1
% flag: judge Kernel is valid or not

% Firstly, determine the Kernel Matrix according to the choice of method
[~, num] = size(X);

innerproduct_mat = X'*X;

if Method == 1
    K = innerproduct_mat;
end

for m = 2 : 5
    if Method == m
        K = (innerproduct_mat + 1).^m;
        break;
    end
end

if Method == inf
    tmp = sum(X.^2);
    X1 = repmat(tmp, num, 1);
    K = exp(-gamma*(X1 + X1' - 2 * innerproduct_mat));
end

%----------------------------------------------------------------
% Second step: check eigenvalue of K to show whether it is a valid Kernel
eigenvalue = eig(K);
smallest_eig = min(eigenvalue);
if smallest_eig >= -threshold1
    flag = 1;
else
    flag = 0;
end


%----------------------------------------------------------------
% Third step: using quadprog to solve Dual SVM
D = diag(d);

% Matrix Parameter for Quadprog solver
H = D * K * D;
f = -ones(num, 1);
A = [];
b = [];
Aeq = d';
beq = 0;
lb = zeros(num, 1);
ub = C * ones(num, 1);
options = optimset('LargeScale','off','MaxIter',1000);
x0 = zeros(num, 1);

alpha = quadprog(H, f, A, b, Aeq, beq, lb, ub, x0, options);
%----------------------------------------------------------------
% Fourth Step: recover discriminant function
% select SV and assign 0 to those non-SV alpha
for i = 1: num
    if alpha(i) < threshold2
        alpha(i) = 0;
    end
end

% calculate bias term (other term can be derived from alpha, d and Kernel)
% using Matrix Computation to calculate weight, which is faster
Alpha_D = alpha .* d;

bias_all = zeros(1, num);
count = 0;
for i = 1 : num
    if 0 < alpha(i) && alpha(i) < C - threshold2
        bias_all(i) = 1/d(i) - K(i,:) * Alpha_D;
        count = count + 1;
    end
end

bias = sum(bias_all) / count;








    

    
        
   


