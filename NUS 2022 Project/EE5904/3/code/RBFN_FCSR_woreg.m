% Fixed Center with Selected Randomly without regularization (introduce the bias term)
function [w, record_random_centroid, record_centroid_idx, std] = RBFN_FCSR_woreg(X_train, target_train, center_num, method)

% Parameter:
% X_train: training sample; dimension * number of training sample
% target_train: target of training sample; 1 * number of training sample
% center_num: number of centroids
% method:   -1 -> appropriate sigma
%           positive number -> fixed sigma

% Return:
% w: weight of the second layer; 1 * number of centroid + 1
% record_random_centroid: Record the vector of centroids; dimension *
% number of centroids
% std: the width of RBF

[~, num] = size(X_train);
M = center_num;

disorder = randperm(num);
% index of centroid
centroid_idx = disorder(1 : M);
record_centroid_idx = centroid_idx;

record_random_centroid = X_train(: , centroid_idx); % D * K

% calculate the appropriate sigma
% find the maximum distance between chosen centres
if method < 0
    distance_matrix = zeros(M, M);
    for i = 1 : M - 1
        center_i = record_random_centroid(:, i);
        for j = (i+1) : M
            center_j = record_random_centroid(:, j);
            distance_matrix(i,j) = norm(center_i - center_j);
        end
    end
    d_max = max(max(distance_matrix));
    % the appropriate sigma
    sigma = d_max / sqrt(2 * M);
    std = sigma;
else
    sigma = method;
    std = sigma;
end

Phi = ones(num, M+1);
for i = 2 : M+1
    center_i = record_random_centroid(: , i-1);
    for j = 1 : num
        x_j = X_train(: , j);
        distance = norm(center_i - x_j);
        Phi(j,i) = exp(-distance^2/(2*sigma^2));
    end
end

weight = (Phi' * Phi) \ Phi' * target_train';
w = weight';

end




