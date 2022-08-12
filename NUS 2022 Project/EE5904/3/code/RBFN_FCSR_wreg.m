% Fixed Center with Selected Randomly with regularization (introduce the bias term)
function [w, record_random_centroid, record_centroid_idx, std] = RBFN_FCSR_wreg(X_train, target_train, center_num, regularization)

% Parameter:
% X_train: training sample; dimension * number of training sample
% target_train: target of training sample; 1 * number of training sample
% center_num: number of centroids
% regularization: regularization term

% Return:
% w: weight of the second layer; 1 * number of training sample
% record_random_centroid: Record the vector of centroids; dimension *
% number of centroids
% record_centroid_idx: Record the center index; 1 * number of centroids

[~, num] = size(X_train);
M = center_num;

disorder = randperm(num);
% index of centroid
centroid_idx = disorder(1 : M);
record_centroid_idx = centroid_idx;

record_random_centroid = X_train(: , centroid_idx);

% calculate the appropriate sigma
% find the maximum distance between chosen centres
distance_matrix = zeros(M, M);
for i = 1 : M - 1
    center_i = record_random_centroid(:, i);
    for j = (i+1) : M
        center_j = record_random_centroid(:, j);
        distance_matrix(j,i) = norm(center_i - center_j);
    end
end
d_max = max(max(distance_matrix));
% the appropriate sigma
sigma = d_max / sqrt(2 * M);
std = sigma;

Phi = ones(num, M+1);
for i = 2 : M+1
    center_i = record_random_centroid(: , i-1);
    for j = 1 : num
        x_j = X_train(: , j);
        distance = norm(center_i - x_j);
        Phi(j,i) = exp(-distance^2/(2*sigma^2));
    end
end

weight = (Phi' * Phi + diag(regularization*ones(1,M+1))) \ Phi' * target_train';
w = weight';

end




