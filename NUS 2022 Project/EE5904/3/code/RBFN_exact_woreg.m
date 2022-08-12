% exact interpolation (perfect fitting) without regularization (not introduce the bias term)
function w = RBFN_exact_woreg(X_train, target_train, sigma)

% Parameter:
% X_train: training sample; dimension * number of training sample
% target_train: target of training sample; 1 * number of training sample
% sigma: we choose the Radial Basis Function As Gaussian Function with
% parameter (mean=0, variance=sigma^2);

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

weight = Phi \ target_train';
w = weight';

end






