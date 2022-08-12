function mat = CalcSqDistance(X_train, Kmu)

% Parameter:
% X_train: training sample; dimension * number of training sample
% Kmu: centroid matrix; dimension * number of centroids

% Return:
% mat: Square distance Matrix; number of centroids * number of training
% samples

N = size(X_train, 2);
K = size(Kmu, 2);
Data_sq = diag(X_train' * X_train)'; % 1 * N 
Kmu_sq = diag(Kmu' * Kmu); % K * 1
trans = 2 * Kmu' * X_train; 
mat = repmat(Data_sq, K, 1) - trans + repmat(Kmu_sq, 1, N);

end
