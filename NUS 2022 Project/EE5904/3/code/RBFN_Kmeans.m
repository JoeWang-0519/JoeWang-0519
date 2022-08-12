% Fixed Center with Kmeans without regularization (introduce the bias term)
function [w, record_centroids, std] = RBFN_Kmeans(X_train, target_train, K, method, regularization)

% Parameter:
% X_train: training sample; dimension * number of training sample
% target_train: target of training sample; 1 * number of training sample
% K: number of centroids
% method:   -1 -> appropriate sigma
%           positive number -> fixed sigma
% regularization: regular term

% Return:
% w: weight of the second layer; 1 * number of training sample
% record_centroids: the centroids of Kmeans algorithm; dimension * number
% of centroids
% std: width of RBF

[~, num] = size(X_train);
record_centroids = Kmeans(X_train, K); % D * K matrix

if method < 0
    distance_matrix = zeros(K, K);
    for i = 1 : K - 1
        center_i = record_centroids(:, i);
        for j = (i+1) : K
            center_j = record_centroids(:, j);
            distance_matrix(i,j) = norm(center_i - center_j);
        end
    end
    d_max = max(max(distance_matrix));
    % the appropriate sigma
    sigma = d_max / sqrt(2 * K);
    std = sigma;
else
    sigma = method;
    std = sigma;
end


Phi = ones(num, K+1);
for i = 2 : K+1
    center_i = record_centroids(: , i-1);
    for j = 1 : num
        x_j = X_train(: , j);
        distance = norm(center_i - x_j);
        Phi(j,i) = exp(-distance^2 / (2*sigma^2));
    end
end

weight = (Phi' * Phi + diag(regularization * ones(1,K+1))) \ Phi' * target_train';
w = weight';
