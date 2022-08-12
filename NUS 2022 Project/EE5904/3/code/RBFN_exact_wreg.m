% exact interpolation (perfect fitting) with regularization (not introduce the bias term)
function w = RBFN_exact_wreg(X_train, target_train, sigma, regularization)

% Parameter:
% X_train: training sample; dimension * number of training sample
% target_train: target of training sample; 1 * number of training sample
% sigma: we choose the Radial Basis Function As Gaussian Function with
% parameter (mean=0, variance=sigma^2);
% regularization: regularization term

% Return:
% w: weight of the second layer; 1 * number of training sample

[~, num] = size(X_train);
Phi = zeros(num, num);
for i = 1 : num
    x_i = X_train(:,i);
    for j = i : num
        x_j = X_train(:,j);
        distance = norm(x_i - x_j);
        Phi(i,j) = exp(-distance^2/(2*sigma^2));
    end
end

Diag = diag(diag(Phi)); % extract the diagonal matrix
Phi = Phi + Phi' - Diag;

weight = (Phi * Phi + diag(regularization * ones(1 , num))) \ Phi * target_train';
w = weight';

end






